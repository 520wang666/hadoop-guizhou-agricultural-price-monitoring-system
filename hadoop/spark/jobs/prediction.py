# -*- coding: utf-8 -*-

"""
Spark价格预测作业
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, collect_list, explode
from pyspark.sql.types import FloatType
import pandas as pd
from prophet import Prophet
import json


class PricePredictionJob:
    """价格预测作业"""
    
    def __init__(self, Prophet_model="prophet"):
        self.spark = SparkSession.builder \
            .appName("PricePredictionJob") \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .enableHiveSupport() \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        self.model_name = model_name
    
    def run_prediction(self, product_id, region_id, predict_days=7):
        """执行价格预测"""
        print(f"Running prediction for product: {product_id}, region: {region_id}")
        
        # 获取历史数据
        df = self.spark.sql(f"""
            SELECT trade_date, avg_price 
            FROM dwd_agri_price_detail
            WHERE product_id = '{product_id}' AND region_id = '{region_id}'
            ORDER BY trade_date
        """)
        
        if df.count() < 30:
            print(f"Not enough data for prediction: {df.count()} records")
            return
        
        # 转换为Pandas DataFrame
        pandas_df = df.toPandas()
        
        # 准备Prophet数据
        prophet_df = pd.DataFrame({
            'ds': pandas_df['trade_date'],
            'y': pandas_df['avg_price']
        })
        
        # 训练模型
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True
        )
        model.fit(prophet_df)
        
        # 预测未来数据
        future = model.make_future_dataframe(periods=predict_days)
        forecast = model.predict(future)
        
        # 提取预测结果
        forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(predict_days)
        
        # 转换为Spark DataFrame
        prediction_df = self.spark.createDataFrame(forecast_df)
        
        # 添加元数据
        from datetime import datetime
        prediction_df = prediction_df \
            .withColumn("prediction_id", lit(f"{product_id}_{region_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}")) \
            .withColumn("product_id", lit(product_id)) \
            .withColumn("region_id", lit(region_id)) \
            .withColumn("model_name", lit(self.model_name)) \
            .withColumn("model_version", lit("1.0.0")) \
            .withColumn("train_end_date", lit(pandas_df['trade_date'].max())) \
            .withColumnRenamed("ds", "predict_date") \
            .withColumnRenamed("yhat", "predicted_price") \
            .withColumnRenamed("yhat_lower", "confidence_lower") \
            .withColumnRenamed("yhat_upper", "confidence_upper") \
            .withColumn("confidence_level", lit(0.95)) \
            .withColumn("prediction_time", lit(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # 写入预测表
        year = datetime.now().year
        month = datetime.now().month
        
        prediction_df.write \
            .mode("append") \
            .partitionBy("year", "month") \
            .format("orc") \
            .saveAsTable("ads_price_prediction")
        
        print(f"Prediction completed for product: {product_id}, region: {region_id}")
    
    def run_batch_prediction(self, predict_days=7):
        """批量预测所有产品"""
        print("Running batch prediction for all products")
        
        # 获取所有产品-地区组合
        combinations = self.spark.sql("""
            SELECT DISTINCT product_id, region_id
            FROM dwd_agri_price_detail
        """)
        
        # 转换为列表
        combo_list = combinations.select("product_id", "region_id").collect()
        
        # 对每个组合进行预测
        for row in combo_list:
            try:
                self.run_prediction(row.product_id, row.region_id, predict_days)
            except Exception as e:
                print(f"Prediction failed for {row.product_id}_{row.region_id}: {e}")
        
        print(f"Batch prediction completed: {len(combo_list)} predictions")
    
    def stop(self):
        """停止Spark会话"""
        self.spark.stop()


if __name__ == "__main__":
    import sys
    
    job = PricePredictionJob()
    
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "single":
                product_id = sys.argv[2] if len(sys.argv) > 2 else "P001"
                region_id = sys.argv[3] if len(sys.argv) > 3 else "R001"
                predict_days = int(sys.argv[4]) if len(sys.argv) > 4 else 7
                job.run_prediction(product_id, region_id, predict_days)
            
            elif command == "batch":
                predict_days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
                job.run_batch_prediction(predict_days)
            
            else:
                print(f"Unknown command: {command}")
        else:
            print("Usage: python prediction.py <single|batch> [product_id] [region_id] [predict_days]")
    finally:
        job.stop()
