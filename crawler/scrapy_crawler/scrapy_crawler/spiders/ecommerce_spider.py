# -*- coding: utf-8 -*-

"""
电商平台爬虫
"""

import scrapy
from scrapy_crawler.spiders.base_spider import BaseSpider


class EcommerceSpider(BaseSpider):
    """电商平台爬虫"""
    
    name = 'ecommerce_spider'
    allowed_domains = ['taobao.com', 'jd.com', 'pinduoduo.com']
    
    # 示例URL（实际使用时需要替换为真实URL）
    start_urls = [
        'https://www.taobao.com/search?q=贵州农产品',
        'https://search.jd.com/Search?keyword=贵州农产品',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 4,
    }
    
    def parse(self, response):
        """解析搜索结果页"""
        self.logger.info(f"Parsing search page: {response.url}")
        
        # 解析商品列表
        products = response.css('.product-item')
        
        for product in products:
            # 提取商品详情页URL
            detail_url = product.css('a::attr(href)').get()
            if detail_url:
                yield response.follow(detail_url, callback=self.parse_detail)
        
        # 翻页
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_detail(self, response):
        """解析商品详情页"""
        self.logger.info(f"Parsing detail page: {response.url}")
        
        # 提取商品信息
        product_name = self.extract_text(response.css('.product-title::text'))
        price = self.clean_price(response.css('.price::text').get())
        
        # 提取规格信息
        spec = self.extract_text(response.css('.spec::text'))
        unit = self.extract_text(response.css('.unit::text'))
        
        # 提取产地信息
        region = self.extract_text(response.css('.origin::text'))
        
        # 提取销量
        sales_volume = self.extract_number(response.css('.sales::text'))
        
        # 创建数据项
        item = self.create_item(
            product_name=product_name,
            retail_price=price,
            wholesale_price=price * 0.9,  # 假设批发价为零售价的90%
            spec=spec,
            unit=unit,
            region=region,
            trade_volume=sales_volume,
            trade_date=self.get_trade_date(),
            source_url=response.url
        )
        
        yield item
    
    def get_trade_date(self):
        """获取交易日期"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
