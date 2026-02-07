# -*- coding: utf-8 -*-

"""
Spark价格预警检测作业
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lit, when, abs, stddev, avg as avg_,
    row_number, desc
)
from pyspark.sql.window import Window
from datetime import datetime
import uuid


class AlertDetectionJob:
    """价格预警检测作业"""
    
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("AlertDetectionJob") \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .enableHiveSupport() \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
        # 预警阈值配置
        self.alert_thresholds = {
            'level1': 0.50,  # 一级预警：偏离度50%
            'level2': 0.30,  # 二级预警：偏离度30%
            'level3': 0.15,  # 三级预警：偏离度15%
        }
    
    def run_alert_detection(self, date):
        """执行价格预警检测"""
        print(f"Running alert detection for date: {date}")
        
        # 获取当日价格数据
        current_df = self.spark.sql(f"""
(f"            SELECT * FROM dwd_agri_price_detail
            WHERE trade_date = '{date}'
        """)
        
        if current_df.count() == 0:
            print(f"No data found for date: {date}")
            return
        
        # 获取历史价格数据（最近30天）
        history_df = self.spark.sql(f"""
            SELECT product_id, region_id, avg_price
            FROM dwd_agri_price_detail
            WHERE trade_date >= DATE_SUB('{date}', 30)
              AND trade_date < '{date}'
        """)
        
        # 计算正常价格范围
        normal_range_df = history_df.groupBy("product_id", "region_id") \
            .agg(
                avg_("avg_price").alias("normal_avg_price"),
                stddev("avg_price").alias("price_std")
            ) \
            .withColumn(
                "normal_range_min",
                col("normal_avg_price") - col("price_std") * 2
            ) \
            .withColumn(
                "normal_range_max",
                col("normal_avg_price") + col("price_std") * 2
            )
        
        # 获取预测价格
        prediction_df = self.spark.sql(f"""
            SELECT product_id, region_id, predicted_price
            FROM ads_price_prediction
            WHERE predict_date = '{date}'
        """)
        
        # 合并数据
        alert_df = current_df.join(
            normal_range_df,
            ["product_id", "region_id"],
            "left"
        ).join(
            prediction_df,
            ["product_id", "region_id"],
            "left"
        )
        
        # 计算偏离度
        alert_df = alert_df.withColumn(
            "deviation_rate",
            when(col("normal_avg_price") > 0,
                  abs(col("avg_price") - col("normal_avg_price")) / col("normal_avg_price") * 100)
            .otherwise(0)
        )
        
        # 计算预测误差
        alert_df = alert_df.withColumn(
            "prediction_error",
            when(col("predicted_price") > 0,
                  abs(col("avg_price") - col("predicted_price")) / col("predicted_price") * 100)
            .otherwise(0)
        )
        
        # 判断预警级别
        alert_df = alert_df.withColumn(
            "alert_level",
            when(col("deviation_rate") >= lit(self.alert_thresholds['level1'] * 100), "一级")
            .when(col("deviation_rate") >= lit(self.alert_thresholds['level2'] * 100), "二级")
            .when(col("deviation_rate") >= lit(self.alert_thresholds['level3'] * 100), "三级")
            .otherwise(lit(None))
        )
        
        # 判断预警类型
        alert_df = alert_df.withColumn(
            "alert_type",
            when(col("avg_price") > col("normal_range_max"), "暴涨")
            .when(col("avg_price") < col("normal_range_min"), "暴跌")
            .otherwise("异常")
        )
        
        # 筛选需要预警的记录
        alert_df = alert_df.filter(col("alert_level").isNotNull())
        
        # 添加预警元数据
        alert_df = (alert_df
            .withColumn("alert_id", lit(str(uuid.uuid4())))
            .withColumn("alert_time", lit(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            .withColumn("current_date", lit(date))
            .withColumn("is_handled", lit(0))
            .withColumn("handle_time", lit(None))
            .withColumn("handle_result", lit(None))
        )
        
        # 写入预警表
        alert_df.select(
            "alert_id", "product_id", "product_name", "region_id", "region_name",
            "alert_time", "alert_level", "alert_type", "current_date",
            "avg_price".alias("current_price"),
            "normal_range_min", "normal_range_max", "deviation_rate",
            "predicted_price", "prediction_error",
            "is_handled", "handle_time", "handle_result"
        ).write \
            .mode("append") \
            .format("orc") \
            .saveAsTable("ads_price_alert")
        
        alert_count = alert_df.count()
        print(f"Alert detection completed for date: {date}, alerts: {alert_count}")
        
        return alert_count
    
    def run_batch_detection(self, days=7):
        """批量检测最近几天的预警"""
        print(f"Running batch alert detection for last {days} days")
        
        total_alerts = 0
        
        for i in range(days):
            from datetime import datetime, timedelta
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            alert_count = self.run_alert_detection(date)
            total_alerts += alert_count
        
        print(f"Batch alert detection completed: {total_alerts} alerts")
        return total_alerts
    
    def stop(self):
        """停止Spark会话"""
        self.spark.stop()


if __name__ == "__main__":
    import sys
    
    job = AlertDetectionJob()
    
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "single":
                date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime('%Y-%m-%d')
                job.run_alert_detection(date)
            
            elif command == "batch":
                days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
                job.run_batch_detection(days)
            
            else:
                print(f"Unknown command: {command}")
        else:
            print("Usage: python alert_detection.py <single|batch> [date] [days]")
    finally:
        job.stop()
