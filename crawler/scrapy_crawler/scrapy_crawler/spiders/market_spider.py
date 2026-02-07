# -*- coding: utf-8 -*-

"""
批发市场爬虫
"""

import scrapy
from scrapy_crawler.spiders.base_spider import BaseSpider


class MarketSpider(BaseSpider):
    """批发市场爬虫"""
    
    name = 'market_spider'
    allowed_domains = ['xinfadi.com.cn', 'gyagri.gov.cn']
    
    # 示例URL（实际使用时需要替换为真实URL）
    start_urls = [
        'https://www.xinfadi.com.cn/priceList',
        'https://www.gyagri.gov.cn/price',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 6,
    }
    
    def parse(self, response):
        """解析价格列表页"""
        self.logger.info(f"Parsing market price page: {response.url}")
        
        # 解析价格记录
        price_records = response.css('.price-row')
        
        for record in price_records:
            # 提取产品信息
            product_name = self.extract_text(record.css('.product-name::text'))
            category = self.extract_text(record.css('.category::text'))
            spec = self.extract_text(record.css('.spec::text'))
            unit = self.extract_text(record.css('.unit::text'))
            
            # 提取价格信息
            wholesale_price = self.clean_price(record.css('.wholesale-price::text').get())
            retail_price = self.clean_price(record.css('.retail-price::text').get())
            highest_price = self.clean_price(record.css('.highest-price::text').get())
            lowest_price = self.clean_price(record.css('.lowest-price::text').get())
            
            # 提取市场信息
            market_name = self.extract_text(record.css('.market-name::text'))
            market_type = self.extract_text(record.css('.market-type::text'))
            region = self.extract_text(record.css('.region::text'))
            address = self.extract_text(record.css('.address::text'))
            
            # 提取地理坐标
            latitude = self.extract_number(record.css('.latitude::text'))
            longitude = self.extract_number(record.css('.longitude::text'))
            
            # 提取交易信息
            trade_volume = self.extract_number(record.css('.trade-volume::text'))
            trade_date = self.extract_text(record.css('.trade-date::text'))
            
            # 创建数据项
            item = self.create_item(
                product_name=product_name,
                category=category,
                spec=spec,
                unit=unit,
                wholesale_price=wholesale_price,
                retail_price=retail_price,
                highest_price=highest_price,
                lowest_price=lowest_price,
                market_name=market_name,
                market_type=market_type,
                region=region,
                address=address,
                latitude=latitude,
                longitude=longitude,
                trade_volume=trade_volume,
                trade_date=trade_date,
                source_url=response.url
            )
            
            yield item
        
        # 翻页
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
