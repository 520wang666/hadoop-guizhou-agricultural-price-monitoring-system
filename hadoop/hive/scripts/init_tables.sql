-- ========================================
-- Hive数据仓库初始化脚本
-- ========================================

-- 设置数据库
USE default;

-- ========================================
-- ODS层：原始数据层
-- ========================================

-- 原始价格数据表
CREATE EXTERNAL TABLE IF NOT EXISTS ods_agri_price_raw (
    raw_data STRING COMMENT '原始JSON数据',
    crawl_time TIMESTAMP COMMENT '抓取时间',
    source STRING COMMENT '数据来源',
    data_version STRING COMMENT '数据版本',
    status STRING COMMENT '处理状态'
) 
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY',
    'orc.create.index'='true'
);

-- 原始日志表
CREATE EXTERNAL TABLE IF NOT EXISTS ods_crawler_log (
    log_id STRING COMMENT '日志ID',
    crawler_name STRING COMMENT '爬虫名称',
    url STRING COMMENT '请求URL',
    status STRING COMMENT '状态',
    error_msg STRING COMMENT '错误信息',
    duration BIGINT COMMENT '耗时(ms)',
    log_time TIMESTAMP COMMENT '日志时间'
) 
PARTITIONED BY (dt STRING COMMENT '日期分区')
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- ========================================
-- DWD层：明细数据层
-- ========================================

-- 产品价格明细表
CREATE TABLE IF NOT EXISTS dwd_agri_price_detail (
    price_id STRING COMMENT '价格ID',
    product_id STRING COMMENT '产品ID',
    product_name STRING COMMENT '产品名称',
    category_id STRING COMMENT '分类ID',
    market_id STRING COMMENT '市场ID',
    market_name STRING COMMENT '市场名称',
    region_id STRING COMMENT '地区ID',
    region_name STRING COMMENT '地区名称',
    avg_price DECIMAL(10,2) COMMENT '平均价格',
    wholesale_price DECIMAL(10,2) COMMENT '批发价',
    retail_price DECIMAL(10,2) COMMENT '零售价',
    highest_price DECIMAL(10,2) COMMENT '最高价',
    lowest_price DECIMAL(10,2) COMMENT '最低价',
    trade_volume DECIMAL(15,2) COMMENT '交易量',
    trade_date DATE COMMENT '交易日期',
    crawl_time TIMESTAMP COMMENT '抓取时间',
    source STRING COMMENT '数据来源',
    data_quality_score DECIMAL(3,2) COMMENT '数据质量评分'
) 
PARTITIONED BY (year STRING, month STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY',
    'orc.create.index'='true',
    'orc.stripe.size'='67108864'
);

-- 价格变化明细表
CREATE TABLE IF NOT EXISTS dwd_price_change_detail (
    change_id STRING COMMENT '变化ID',
    product_id STRING COMMENT '产品ID',
    region_id STRING COMMENT '地区ID',
    trade_date DATE COMMENT '交易日期',
    prev_price DECIMAL(10,2) COMMENT '前一日价格',
    curr_price DECIMAL(10,2) COMMENT '当日价格',
    price_change DECIMAL(10,2) COMMENT '价格变化',
    price_change_rate DECIMAL(5,2) COMMENT '价格变化率(%)',
    change_type STRING COMMENT '变化类型(上涨/下跌/持平)'
) 
PARTITIONED BY (year STRING, month STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- ========================================
-- DWS层：汇总数据层
-- ========================================

-- 每日价格汇总表
CREATE TABLE IF NOT EXISTS dws_price_daily_summary (
    summary_date DATE COMMENT '汇总日期',
    product_id STRING COMMENT ' '产品ID',
    region_id STRING COMMENT '地区ID',
    avg_price DECIMAL(10,2) COMMENT '平均价格',
    max_price DECIMAL(10,2) COMMENT '最高价格',
    min_price DECIMAL(10,2) COMMENT '最低价格',
    price_std DECIMAL(10,2) COMMENT '价格标准差',
'    total_volume DECIMAL(15,2) COMMENT '总交易量',
    market_count INT COMMENT '市场数量',
    price_trend STRING COMMENT '价格趋势'
) 
PARTITIONED BY (year STRING, month STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- 每月价格汇总表
CREATE TABLE IF NOT EXISTS dws_price_monthly_summary (
    summary_year INT COMMENT '汇总年份',
    summary_month INT COMMENT '汇总月份',
    product_id STRING COMMENT '产品ID',
    region_id STRING COMMENT '地区ID',
    month_avg_price DECIMAL(10,2) COMMENT '月均价格',
    month_max_price DECIMAL(10,2) COMMENT '月最高价',
    month_min_price DECIMAL(10,2) COMMENT '月最低价',
    month_start_price DECIMAL(10,2) COMMENT '月初价格',
    month_end_price DECIMAL(10,2) COMMENT '月末价格',
    month_change_rate DECIMAL(5,2) COMMENT '月变化率(%)',
    total_volume DECIMAL(15,2) COMMENT '月总交易量'
) 
PARTITIONED BY (year STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- ========================================
-- ADS层：应用数据层
-- ========================================

-- 价格趋势分析表
CREATE TABLE IF NOT EXISTS ads_price_trend_analysis (
    product_id STRING COMMENT '产品ID',
    region_id STRING COMMENT '地区ID',
    analysis_date DATE COMMENT '分析日期',
    ma_7day DECIMAL(10,2) COMMENT '7日均线',
    ma_30day DECIMAL(10,2) COMMENT '30日均线',
    current_price DECIMAL(10,2) COMMENT '当前价格',
    price_position STRING COMMENT '价格位置(高位/中位/低位)',
    trend_direction STRING COMMENT '趋势方向(上升/下降/震荡)',
    trend_strength DECIMAL(3,2) COMMENT '趋势强度'
) 
PARTITIONED BY (region STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- 价格预警表
CREATE TABLE IF NOT EXISTS ads_price_alert (
    alert_id STRING COMMENT '预警ID',
    product_id STRING COMMENT '产品ID',
    product_name STRING COMMENT '产品名称',
    region_id STRING COMMENT '地区ID',
    region_name STRING COMMENT '地区名称',
    alert_time TIMESTAMP COMMENT '预警时间',
    alert_level STRING COMMENT '预警级别(一级/二级/三级)',
    alert_type STRING COMMENT '预警类型(暴涨/暴跌/异常)',
    current_date DATE COMMENT '当前日期',
    current_price DECIMAL(10,2) COMMENT '当前价格',
    normal_range_min DECIMAL(10,2)’ COMMENT '正常范围最小值',
    normal_range_max DECIMAL(10,2) COMMENT '正常范围最大值',
    deviation_rate DECIMAL(5,2) COMMENT '偏离度(%)',
    predicted_price DECIMAL(10,2) COMMENT '预测价格',
    prediction_error DECIMAL(5,2) COMMENT '预测误差(%)',
    is_handled TINYINT COMMENT '是否处理',
    handle_time TIMESTAMP COMMENT '处理时间',
    handle_result STRING COMMENT '处理结果'
) 
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- 价格预测结果表
CREATE TABLE IF NOT EXISTS ads_price_prediction (
    prediction_id STRING COMMENT '预测ID',
    product_id STRING COMMENT '产品ID',
    region_id STRING COMMENT '地区ID',
    model_name STRING COMMENT '模型名称',
    model_version STRING COMMENT '模型版本',
    train_end_date DATE COMMENT '训练结束日期',
    predict_date DATE COMMENT '预测日期',
    predicted_price DECIMAL(10,2) COMMENT '预测价格',
    confidence_lower DECIMAL(10,2) COMMENT '置信区间下限',
    confidence_upper DECIMAL(10,2) COMMENT '置信区间上限',
    confidence_level DECIMAL(3,2) COMMENT '置信水平',
    prediction_time TIMESTAMP COMMENT '预测时间'
) 
PARTITIONED BY (year STRING, month STRING)
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY'
);

-- ========================================
-- 创建HDFS目录
-- ========================================

-- 创建原始数据目录
CREATE DATABASE IF NOT EXISTS agriculture;
USE agriculture;

-- 创建分区目录
MSCK REPAIR TABLE ods_agri_price_raw;
MSCK REPAIR TABLE ods_crawler_log;
MSCK REPAIR TABLE dwd_agri_price_detail;
MSCK REPAIR TABLE dwd_price_change_detail;
MSCK REPAIR TABLE dws_price_daily_summary;
MSCK REPAIR TABLE dws_price_monthly_summary;
MSCK REPAIR TABLE ads_price_trend_analysis;
MSCK REPAIR TABLE ads_price_alert;
MSCK REPAIR TABLE ads_price_prediction;

-- ========================================
-- 显示创建的表
-- ========================================

SHOW TABLES;
