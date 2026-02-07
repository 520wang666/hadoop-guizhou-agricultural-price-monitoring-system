# -*- coding: utf-8 -*-

"""
数据管道
"""

import json
import logging
from datetime import datetime
from kafka import KafkaProducer
import hdfs3

from scrapy_crawler.items import AgriculturalProductPriceItem, CrawlerLogItem


class ValidationPipeline:
    """数据验证管道"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_item(self, item, spider):
        """验证数据项"""
        
        if isinstance(item, AgriculturalProductPriceItem):
            # 验证必填字段
            required_fields = ['product_name', 'market', 'trade_date']
            for field in required_fields:
                if not item.get(field):
                    self.logger.warning(f"Missing required field: {field}")
                    return None
            
            # 验证价格字段
            price_fields = ['wholesale_price', 'retail_price', 'highest_price', 'lowest_price']
            for field in price_fields:
                if item.get(field) is not None:
                    try:
                        price = float(item[field])
                        if price < 0:
                            self.logger.warning(f"Invalid price value: {field}={price}")
                            return None
                    except (ValueError, TypeError):
                        self.logger.warning(f"Invalid price format: {field}={item[field]}")
                        return None
            
            # 验证日期格式
            try:
                datetime.strptime(item['trade_date'], '%Y-%m-%d')
            except (ValueError, TypeError):
                self.logger.warning(f"Invalid date format: {item['trade_date']}")
                return None
        
        return item


class CleaningPipeline:
    """数据清洗管道"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_item(self, item, spider):
        """清洗数据项"""
        
        if isinstance(item, AgriculturalProductPriceItem):
            # 统一价格单位（转换为元/公斤）
            item = self._normalize_price_unit(item)
            
            # 填充缺失值
            item = self._fill_missing_values(item)
            
            # 生成产品ID
            if not item.get('product_id'):
                item['product_id'] = self._generate_product_id(item)
            
            # 生成市场ID
            if not item.get('market_id'):
                item['market_id'] = self._generate_market_id(item)
            
            # 设置抓取时间
            if not item.get('crawl_time'):
                item['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return item
    
    def _normalize_price_unit(self, item):
        """统一价格单位"""
        unit = item.get('unit', '')
        
        # 如果单位是斤，转换为公斤
        if '斤' in unit:
            for field in ['wholesale_price', 'retail_price', 'highest_price', 'lowest_price', 'avg_price']:
                if item.get(field) is not None:
                    item[field] = float(item[field]) * 2
            item['unit'] = '千克'
        
        return item
    
    def _fill_missing_values(self, item):
        """填充缺失值"""
        # 如果没有平均价格，计算批发价和零售价的平均值
        if not item.get('avg_price'):
            wholesale = item.get('wholesale_price')
            retail = item.get('retail_price')
            if wholesale and retail:
                item['avg_price'] = (float(wholesale) + float(retail)) / 2
            elif wholesale:
                item['avg_price'] = float(wholesale)
            elif retail:
                item['avg_price'] = float(retail)
        
        # 如果没有最高价，使用批发价或零售价
        if not item.get('highest_price'):
            if item.get('wholesale_price'):
                item['highest_price'] = item['wholesale_price']
            elif item.get('retail_price'):
                item['highest_price'] = item['retail_price']
        
        # 如果没有最低价，使用批发价或零售价
        if not item.get('lowest_price'):
            if item.get('wholesale_price'):
                item['lowest_price'] = item['wholesale_price']
            elif item.get('retail_price'):
                item['lowest_price'] = item['retail_price']
        
        return item
    
    def _generate_product_id(self, item):
        """生成产品ID"""
        product_name = item.get('product_name', '')
        category = item.get('category', '')
        return f"P_{category}_{product_name}".replace(' ', '_')
    
    def _generate_market_id(self, item):
        """生成市场ID"""
        market_name = item.get('market_name', '')
        region = item.get('region', '')
        return f"M_{region}_{market_name}".replace(' ', '_')


class KafkaPipeline:
    """Kafka数据管道"""
    
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        return cls(
            bootstrap_servers=crawler.settings.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            topic=crawler.settings.get('KAFKA_TOPIC', 'price-data')
        )
    
    def open_spider(self, spider):
        """打开spider时初始化Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            self.logger.info(f"Kafka producer initialized: {self.bootstrap_servers}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka producer: {e}")
    
    def close_spider(self, spider):
        """关闭spider时关闭Kafka producer"""
        if self.producer:
            self.producer.close()
            self.logger.info("Kafka producer closed")
    
    def process_item(self, item, spider):
        """发送数据到Kafka"""
        if not self.producer:
            return item
        
        try:
            # 转换为字典
            item_dict = dict(item)
            
            # 发送到Kafka
            self.producer.send(self.topic, value=item_dict)
            self.producer.flush()
            
            self.logger.debug(f"Sent item to Kafka: {item.get('product_name')}")
        except Exception as e:
            self.logger.error(f"Failed to send item to Kafka: {e}")
        
        return item


class HDFSPipeline:
    """HDFS数据管道"""
    
    def __init__(self, hdfs_host, hdfs_port, hdfs_path):
        self.hdfs_host = hdfs_host
        self.hdfs_port = hdfs_port
        self.hdfs_path = hdfs_path
        self.hdfs = None
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        return cls(
            hdfs_host=crawler.settings.get('HDFS_HOST', 'localhost'),
            hdfs_port=crawler.settings.get('HDFS_PORT', 9000),
            hdfs_path=crawler.settings.get('HDFS_PATH', '/agriculture/raw/ods_agri_price_raw')
        )
    
    def open_spider(self, spider):
        """打开spider时初始化HDFS连接"""
        try:
            self.hdfs = hdfs3.HDFileSystem(host=self.hdfs_host, port=self.hdfs_port)
            
            # 确保目录存在
            if not self.hdfs.exists(self.hdfs_path):
                self.hdfs.mkdir(self.hdfs_path)
            
            self.logger.info(f"HDFS connection established: {self.hdfs_host}:{self.hdfs_port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to HDFS: {e}")
    
    def close_spider(self, spider):
        """关闭spider时关闭HDFS连接"""
        if self.hdfs:
            self.hdfs.close()
            self.logger.info("HDFS connection closed")
    
    def process_item(self, item, spider):
        """写入数据到HDFS"""
        if not self.hdfs:
            return item
        
        try:
            # 转换为JSON
            item_json = json.dumps(dict(item), ensure_ascii=False) + '\n'
            
            # 生成文件路径（按日期分区）
            trade_date = item.get('trade_date', datetime.now().strftime('%Y-%m-%d'))
            file_path = f"{self.hdfs_path}/dt={trade_date}/data.json"
            
            # 写入HDFS
            if self.hdfs.exists(file_path):
                with self.hdfs.open_file(file_path, mode='a') as f:
                    f.write(item_json.encode('utf-8'))
            else:
                with self.hdfs.open_file(file_path, mode='w') as f:
                    f.write(item_json.encode('utf-8'))
            
            self.logger.debug(f"Wrote item to HDFS: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write item to HDFS: {e}")
        
        return item
