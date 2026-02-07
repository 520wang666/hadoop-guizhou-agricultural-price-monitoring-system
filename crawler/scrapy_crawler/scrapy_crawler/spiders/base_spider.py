# -*- coding: utf-8 -*-

"""
基础爬虫类
"""

import scrapy
from scrapy_crawler.items import AgriculturalProductPriceItem


class BaseSpider(scrapy.Spider):
    """基础爬虫类"""
    
    name = 'base_spider'
    allowed_domains = []
    start_urls = []
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 8,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger.info(f"Spider {self.name} initialized")
    
    def parse(self, response):
        """解析响应"""
        self.logger.info(f"Parsing: {response.url}")
        # 子类需要实现此方法
        yield {}
    
    def create_item(self, **kwargs):
        """创建数据项"""
        item = AgriculturalProductPriceItem()
        
        # 设置默认值
        item['source'] = self.name
        item['crawl_time'] = self.get_crawl_time()
        
        # 设置传入的值
        for key, value in kwargs.items():
            if value is not None:
                item[key] = value
        
        return item
    
    def get_crawl_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def extract_text(self, selector, default=''):
        """提取文本"""
        if selector:
            text = selector.get().strip()
            return text if text else default
        return default
    
    def extract_number(self, selector, default=0.0):
        """提取数字"""
        text = self.extract_text(selector)
        try:
            return float(text)
        except (ValueError, TypeError):
            return default
    
    def clean_price(self, price_str):
        """清洗价格字符串"""
        if not price_str:
            return None
        
        # 移除货币符号和空格
        price_str = price_str.replace('￥', '').replace('¥', '').replace('元', '').strip()
        
        try:
            return float(price_str)
        except (ValueError, TypeError):
            return None
