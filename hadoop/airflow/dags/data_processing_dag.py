# -*- coding: utf-8 -*-

"""
数据处理DAG
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
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
    'data_processing_dag',
    default_args=default_args,
    description='农产品价格数据处理DAG',
    schedule_interval='0 9 * * *',  # 每天9点执行
    catchup=False,
    tags=['spark', 'data-processing'],
)

# 每日价格汇总任务
daily_summary = SparkSubmitOperator(
    task_id='daily_summary',
    application='/app/spark/jobs/price_analysis.py',
    application_args=['daily', '{{ ds }}'],
    conn_id='spark_default',
    conf={
        'spark.master': 'spark://spark-master:7077',
        'spark.executor.memory': '2g',
        'spark.driver.memory': '1g',
        'spark.executor.cores': '2',
    },
    dag=dag,
)

# 价格趋势分析任务
trend_analysis = SparkSubmitOperator(
    task_id='trend_analysis',
    application='/app/spark/jobs/price_analysis.py',
    application_args=['trend', '{{ ds }}'],
    conn_id='spark_default',
    conf={
        'spark.master': 'spark://spark-master:7077',
        'spark.executor.memory': '2g',
        'spark.driver.memory': '1g',
        'spark.executor.cores': '2',
    },
    dag=dag,
)

# 价格预警检测任务
alert_detection = SparkSubmitOperator(
    task_id='alert_detection',
    application='/app/spark/jobs/alert_detection.py',
    application_args=['single', '{{ ds }}'],
    conn_id='spark_default',
    conf={
        'spark.master': 'spark://spark-master:7077',
        'spark.executor.memory': '2g',
        'spark.driver.memory': '1g',
        'spark.executor.cores': '2',
    },
    dag=dag,
)

# 设置任务依赖
daily_summary >> trend_analysis >> alert_detection
