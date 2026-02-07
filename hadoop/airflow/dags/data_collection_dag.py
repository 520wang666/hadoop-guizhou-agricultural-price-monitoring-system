# -*- coding: utf-8 -*-

"""
数据采集DAG
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_collection_dag',
    default_args=default_args,
    description='农产品价格数据采集DAG',
    schedule_interval='0 8 * * *',  # 每天8点执行
    catchup=False,
    tags=['crawler', 'data-collection'],
)

# 电商平台爬虫任务
ecommerce_crawler = BashOperator(
    task_id='ecommerce_crawler',
    bash_command='cd /path/to/crawler/scrapy_crawler && scrapy crawl ecommerce_spider',
    dag=dag,
)

# 农业信息网爬虫任务
agriculture_crawler = BashOperator(
    task_id='agriculture_crawler',
    bash_command='cd /path/to/crawler/scrapy_crawler && scrapy crawl agriculture_spider',
    dag=dag,
)

# 批发市场爬虫任务
market_crawler = BashOperator(
    task_id='market_crawler',
    bash_command='cd /path/to/crawler/scrapy_crawler && scrapy crawl market_spider',
    dag=dag,
)

# 数据清洗任务
data_cleaning = BashOperator(
    task_id='data_cleaning',
    bash_command='python /path/to/crawler/data_cleaner/cleaner.py',
    dag=dag,
)

# 设置任务依赖
[ecommerce_crawler, agriculture_crawler, market_crawler] >> data_cleaning
