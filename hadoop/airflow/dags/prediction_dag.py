# -*- coding: utf-8 -*-

"""
价格预测DAG
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'prediction_dag',
    default_args=default_args,
    description='农产品价格预测DAG',
    schedule_interval='0 10 * * *',  # 每天10点执行
    catchup=False,
    tags=['spark', 'prediction'],
)

# 批量预测任务
batch_prediction = SparkSubmitOperator(
    task_id='batch_prediction',
    application='/path/to/hadoop/spark/jobs/prediction.py',
    application_args=['batch', '7'],  # 预测未来7天
    conn_id='spark_default',
    conf={
        'spark.master': 'yarn',
        'spark.executor.memory': '4g',
        'spark.driver.memory': '2g',
        'spark.executor.cores': '4',
        'spark.dynamicAllocation.enabled': 'true',
        'spark.shuffle.service.enabled': 'true',
    },
    dag=dag,
)
