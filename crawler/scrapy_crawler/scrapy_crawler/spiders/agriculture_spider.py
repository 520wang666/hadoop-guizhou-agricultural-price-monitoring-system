# -*- coding: utf-8 -*-

"""
农业信息网爬虫
"""

import scrapy
from scrapy_crawler.spiders.base_spider import BaseSpider


class AgricultureSpider(BaseSpider):
    """农业信息网爬虫"""
    
    name = 'agriculture_spider'
    allowed_domains = ['agri.guizhou.gov.cn', 'mara.gov.cn']
    
    # 示例URL（实际使用时需要替换为真实URL）
    start_urls = [
        'https://agri.guizhou.gov.cn/price/list',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 6,
    }
    
    def parse(self, response):
        """解析价格列表页"""
        self.logger.info(f"Parsing price list page: {response.url}")
        
        # 解析价格记录
        price_records = response.css('.price-record')
        
        for record in price_records:
            # 提取产品信息
            product_name = self.extract_text(record.css('.product-name::text'))
            category = self.extract_text(record.css('.category::text'))
            
            # 提取价格信息
            wholesale_price = self.clean_price(record.css('.wholesale-price::text').get())
            retail_price = self.clean_price(record.css('.retail-price::text').get())
            highest_price = self.clean_price(record.css('.highest-price::text').get())
            lowest_price = self.clean_price(record.css('.lowest-price::text').get())
            
            # 提取市场信息
            market_name = self.extract_text(record.css('.market-name::text'))
            region = self.extract_text(record.css('.region::text'))
            
            # 提取交易信息
            trade_volume = self.extract_number(record.css('.trade-volume::text'))
            trade_date = self.extract_text(record(record.css('.trade-date::text')))
            
            # 创建数据项
            item = self.create_item(
                product_name=product_name,
                category=category,
                wholesale_price=wholesale_price,
                retail_price=retail_price,
                highest_price=highest_price,
                lowest_price=lowest_price,
                market_name=market_name,
                region=region,
                trade_volume=trade_volume,
                trade_date=trade_date,
                source_url=response.url
            )
            
            yield item
        
        # 翻页
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
