# -*- coding: utf-8 -*-

"""
Spark价格分析作业
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, max as max_, min as min_, 
    stddev, count, sum as sum_, 
    when, lit, row_number, desc
)
from pyspark.sql.window import Window


class PriceAnalysisJob:
    """价格分析作业"""
    
    def __init__(self, app_name="PriceAnalysisJob"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .enableHiveSupport() \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
    
    def run_daily_summary(self, date):
        """执行每日价格汇总"""
        print(f"Running daily summary for date: {date}")
        
        # 读取明细数据
        df = self.spark.sql(f"""
            SELECT * FROM dwd_agri_price_detail
            WHERE trade_date = '{date}'
        """)
        
        if df.count() == 0:
            print(f"No data found for date: {date}")
            return
        
        # 按产品和地区汇总
        summary_df = df.groupBy("product_id", "region_id") \
            .agg(
                avg("avg_price").alias("avg_price"),
                max_("avg_price").alias("max_price"),
                min_("avg_price").alias("min_price"),
                stddev("avg_price").alias("price_std"),
                sum_("trade_volume").alias("total_volume"),
                count("*").alias("market_count")
            ) \
            .withColumn("summary_date", lit(date))
        
        # 计算价格趋势
        summary_df = self._calculate_price_trend(summary_df)
        
        # 写入汇总表
        year = date[:4]
        month = date[5:7]
        summary_df.write \
            .mode("overwrite") \
            .partitionBy("year", "month") \
            .format("orc") \
            .saveAsTable("dws_price_daily_summary")
        
        print(f"Daily summary completed for date: {date}")
    
    def run_monthly_summary(self, year, month):
        """执行每月价格汇总"""
        print(f"Running monthly summary for {year}-{month}")
        
        # 读取每日汇总数据
        df = self.spark.sql(f"""
            SELECT * FROM dws_price_daily_summary
            WHERE year = '{year}' AND month = '{month}'
        """)
        
        if df.count() == 0:
            print(f"No data found for {year}-{month}")
            return
        
        # 按产品和地区汇总
        summary_df = df.groupBy("product_id", "region_id") \
            .agg(
                avg("avg_price").alias("month_avg_price"),
                max_("max_price").alias("month_max_price"),
                min_("min_price").alias("month_min_price"),
                sum_("total_volume").alias("total_volume")
            )
        
        # 计算月初和月末价格
        window_spec = Window.partitionBy("product_id", "region_id") \
            .orderBy("summary_date")
        
        summary_df = summary_df.withColumn(
            "row_num", row_number().over(window_spec)
        )
        
        # 月初价格
        start_price_df = summary_df.filter(col("row_num") == 1) \
            .select("product_id", "region_id", col("avg_price").alias("month_start_price"))
        
        # 月末价格
        window_spec_desc = Window.partitionBy("product_id", "region_id") \
            .orderBy(desc("summary_date"))
        summary_df = summary_df.withColumn(
            "row_num_desc", row_number().over(window_spec_desc)
        )
        end_price_df = summary_df.filter(col("row_num_desc") == 1) \
            .select("product_id", "region_id", col("avg_price").alias("month_end_price"))
        
        # 合并结果
        summary_df = summary_df.join(start_price_df, ["product_id", "region_id"], "left") \
            .join(end_price_df, ["product_id", "region_id"], "left") \
            .drop("row_num", "row_num_desc")
        
        # 计算月变化率
        summary_df = summary_df.withColumn(
            "month_change_rate",
            when(col("month_start_price") > 0,
                  (col("month_end_price") - col("month_start_price")) / col("month_start_price") * 100)
            .otherwise(None)
        )
        
        # 添加年份和月份
        summary_df = summary_df \
            .withColumn("summary_year", lit(int(year))) \
            .withColumn("summary_month", lit(int(month)))
        
        # 写入汇总表
        summary_df.select(
            "summary_year", "summary_month", "product_id", "region_id",
            "month_avg_price", "month_max_price", "month_min_price",
            "month_start_price", "month_end_price", "month_change_rate",
            "total_volume"
        ).write \
            .mode("overwrite") \
            .partitionBy("year") \
            .format("orc") \
            .saveAsTable("dws_price_monthly_summary")
        
        print(f"Monthly summary completed for {year}-{month}")
    
    def run_trend_analysis(self, date):
        """执行价格趋势分析"""
        print(f"Running trend analysis for date: {date}")
        
        # 获取历史数据（最近30天）
        df = self.spark.sql(f"""
            SELECT * FROM dwd_agri_price_detail
            WHERE trade_date >= DATE_SUB('{date}', 30)
            ORDER BY trade_date
        """)
        
        if df.count() == 0:
            print(f"No data found for trend analysis")
            return
        
        # 计算移动平均
        window_spec = Window.partitionBy("product_id", "region_id") \
            .orderBy("trade_date") \
            .rowsBetween(-6, 0)  # 7日窗口
        
        df = df.withColumn("ma_7day", avg("avg_price").over(window_spec))
        
        window_spec_30 = Window.partitionBy("product_id", "region_id") \
            .orderBy("trade_date") \
            .rowsBetween(-29, 0)  # 30日窗口
        
        df = df.withColumn("ma_30day", avg("avg_price").over(window_spec_30))
        
        # 筛选当日数据
        current_df = df.filter(col("trade_date") == date)
        
        # 计算价格位置
        current_df = current_df.withColumn(
            "price_position",
            when(col("avg_price") > col("ma_30day") * 1.1, "高位")
            .when(col("avg_price") < col("ma_30day") * 0.9, "低位")
            .otherwise("中位")
        )
        
        # 计算趋势方向
        current_df = current_df.withColumn(
            "trend_direction",
            when(col("ma_7day") > col("ma_30day"), "上升")
            .when(col("ma_7day") < col("ma_30day"), "下降")
            .otherwise("震荡")
        )
        
        # 计算趋势强度
        current_df = current_df.withColumn(
            "trend_strength",
            when(col("ma_30day") > 0,
                  abs(col("ma_7day") - col("ma_30day")) / col("ma_30day") * 100)
            .otherwise(0)
        )
        
        # 写入分析表
        current_df.select(
            "product_id", "region_id", col("trade_date").alias("analysis_date"),
            "ma_7day", "ma_30day", "avg_price".alias("current_price"),
            "price_position", "trend_direction", "trend_strength"
        ).write \
            .mode("overwrite") \
            .partitionBy("region_id") \
            .format("orc") \
            .saveAsTable("ads_price_trend_analysis")
        
        print(f"Trend analysis completed for date: {date}")
    
    def _calculate_price_trend(self, df):
        """计算价格趋势"""
        # 简单实现：根据最高价和最低价判断趋势
        df = df.withColumn(
            "price_trend",
            when(col("max_price") > col("avg_price") * 1.2, "上涨")
            .when(col("min_price") < col("avg_price") * 0.8, "下跌")
            .otherwise("平稳")
        )
        return df
    
    def stop(self):
        """停止Spark会话"""
        self.spark.stop()


if __name__ == "__main__":
    import sys
    
    job = PriceAnalysisJob()
    
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "daily":
                date = sys.argv[2] if len(sys.argv) > 2 else "2026-02-07"
                job.run_daily_summary(date)
            
            elif command == "monthly":
                year = sys.argv[2] if len(sys.argv) > 2 else "2026"
                month = sys.argv[3] if len(sys.argv) > 3 else "02"
                job.run_monthly_summary(year, month)
            
            elif command == "trend":
                date = sys.argv[2] if len(sys.argv) > 2 else "2026-02-07"
                job.run_trend_analysis(date)
            
            else:
                print(f"Unknown command: {command}")
        else:
            print("Usage: python price_analysis.py <daily|monthly|trend> [date] [year] [month]")
    finally:
        job.stop()
