# -*- coding: utf-8 -*-

"""
农产品价格数据模型
"""

import scrapy


class AgriculturalProductPriceItem(scrapy.Item):
    """农产品价格数据项"""
    
    # 产品信息
    product_id = scrapy.Field()          # 产品ID
    product_name = scrapy.Field()        # 产品名称
    category = scrapy.Field()            # 分类（蔬菜、水果、畜产等）
    spec = scrapy.Field()                # 规格（一级、二级）
    unit = scrapy.Field()                # 单位（千克/斤）
    
    # 价格信息
    wholesale_price = scrapy.Field()      # 批发价
    retail_price = scrapy.Field()         # 零售价
    highest_price = scrapy.Field()        # 最高价
    lowest_price = scrapy.Field()         # 最低价
    avg_price = scrapy.Field()            # 平均价格
    
    # 市场信息
    market_id = scrapy.Field()           # 市场ID
    market_name = scrapy.Field()         # 市场名称
    market_type = scrapy.Field()          # 市场类型（批发/零售）
    region = scrapy.Field()              # 地区
    address = scrapy.Field()             # 地址
    latitude = scrapy.Field()            # 纬度
    longitude = scrapy.Field()           # 经度
    
    # 交易信息
    trade_volume = scrapy.Field()        # 交易量
    trade_date = scrapy.Field()          # 交易日期
    
    # 元数据
    crawl_time = scrapy.Field()          # 抓取时间
    source = scrapy.Field()              # 数据来源
    source_url = scrapy.Field()          # 来源URL


class CrawlerLogItem(scrapy.Item):
    """爬虫日志数据项"""
    
    log_id = scrapy.Field()             # 日志ID
    crawler_name = scrapy.Field()        # 爬虫名称
    url = scrapy.Field()                # 请求URL
    status = scrapy.Field()              # 状态
    error_msg = scrapy.Field()           # 错误信息
    duration = scrapy.Field()           # 耗时(ms)
    log_time = scrapy.Field()           # 日志时间
