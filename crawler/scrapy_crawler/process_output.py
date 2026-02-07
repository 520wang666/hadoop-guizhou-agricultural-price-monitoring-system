#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬虫输出数据处理脚本
处理爬虫生成的数据，进行清洗、转换和存储
"""

import os
import sys
import json
import csv
from datetime import datetime
from pathlib import Path
import mysql.connector


class DataProcessor:
    """数据处理器类"""

    def __init__(self):
        """初始化数据处理器"""
        self.data_dir = Path("/app/data")
        self.output_dir = Path("/app/output")
        self.mysql_config = {
            'host': os.getenv('MYSQL_HOST', 'mysql'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'Root123!'),
            'database': os.getenv('MYSQL_DATABASE', 'agriculture')
        }
        self.hdfs_url = os.getenv('HDFS_URL', 'hdfs://namenode:9000')

    def load_data(self, source='ecommerce'):
        """
        加载爬虫数据

        Args:
            source: 数据源类型 (ecommerce, agriculture, market)

        Returns:
            list: 解析后的数据列表
        """
        data_file = self.data_dir / f"{source}_data.json"

        if not data_file.exists():
            print(f"警告: 数据文件 {data_file} 不存在")
            return []

        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"已加载 {len(data)} 条 {source} 数据")
        return data

    def clean_data(self, data, source):
        """
        清洗数据

        Args:
            data: 原始数据列表
            source: 数据源类型

        Returns:
            list: 清洗后的数据列表
        """
        cleaned_data = []

        for item in data:
            try:
                cleaned_item = {
                    'source': source,
                    'product_name': item.get('product_name', '').strip(),
                    'price': float(item.get('price', 0)),
                    'unit': item.get('unit', 'kg').strip(),
                    'location': item.get('location', '贵州').strip(),
                    'date': self.parse_date(item.get('date', datetime.now().isoformat())),
                    'category': item.get('category', '').strip(),
                    'url': item.get('url', ''),
                    'raw_data': json.dumps(item, ensure_ascii=False)
                }

                # 基本验证
                if cleaned_item['price'] > 0 and cleaned_item['product_name']:
                    cleaned_data.append(cleaned_item)

            except Exception as e:
                print(f"数据处理错误: {e}, 跳过记录: {item}")
                continue

        print(f"清洗后剩余 {len(cleaned_data)} 条有效数据")
        return cleaned_data

    def parse_date(self, date_str):
        """
        解析日期字符串

        Args:
            date_str: 日期字符串

        Returns:
            datetime: 解析后的日期对象
        """
        if not date_str:
            return datetime.now()

        # 尝试多种日期格式
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y年%m月%d日',
            '%Y-%m-%d %H:%M:%S',
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str[:19], fmt)
            except ValueError:
                continue

        return datetime.now()

    def save_to_database(self, data):
        """
        将数据保存到 MySQL 数据库

        Args:
            data: 数据列表
        """
        if not data:
            print("没有数据需要保存")
            return

        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()

            # 创建表（如果不存在）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw_price_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    source VARCHAR(50) NOT NULL,
                    product_name VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    unit VARCHAR(20),
                    location VARCHAR(100),
                    date DATE,
                    category VARCHAR(100),
                    url TEXT,
                    raw_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_source (source),
                    INDEX idx_date (date),
                    INDEX idx_product (product_name)
                )
            """)

            # 插入数据
            insert_sql = """
                INSERT INTO raw_price_data
                (source, product_name, price, unit, location, date, category, url, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            for item in data:
                cursor.execute(insert_sql, (
                    item['source'],
                    item['product_name'],
                    item['price'],
                    item['unit'],
                    item['location'],
                    item['date'].strftime('%Y-%m-%d'),
                    item['category'],
                    item['url'],
                    item['raw_data']
                ))

            conn.commit()
            print(f"成功保存 {len(data)} 条数据到数据库")

        except mysql.connector.Error as e:
            print(f"数据库错误: {e}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_to_csv(self, data, source):
        """
        将数据保存为 CSV 文件

        Args:
            data: 数据列表
            source: 数据源类型
        """
        if not data:
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        csv_file = self.output_dir / f"{source}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['source', 'product_name', 'price', 'unit', 'location', 'date', 'category', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                writer.writerow({
                    'source': item['source'],
                    'product_name': item['product_name'],
                    'price': item['price'],
                    'unit': item['unit'],
                    'location': item['location'],
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'category': item['category'],
                    'url': item['url']
                })

        print(f"CSV 文件已保存到 {csv_file}")

    def upload_to_hdfs(self, data, source):
        """
        将数据上传到 HDFS

        Args:
            data: 数据列表
            source: 数据源类型
        """
        # 这里可以实现 HDFS 上传逻辑
        # 需要安装 hdfs3 或使用 hadoop 命令
        print(f"HDFS 上传功能待实现，数据源: {source}")
        print(f"可以使用以下命令上传:")
        print(f"  hdfs dfs -put {self.output_dir}/{source}_*.csv /agriculture/raw/")

    def process_source(self, source):
        """
        处理单个数据源

        Args:
            source: 数据源类型
        """
        print(f"\n{'='*50}")
        print(f"开始处理 {source} 数据源")
        print(f"{'='*50}")

        # 加载数据
        data = self.load_data(source)

        if not data:
            print(f"没有 {source} 数据需要处理")
            return

        # 清洗数据
        cleaned_data = self.clean_data(data, source)

        if not cleaned_data:
            print(f"{source} 数据清洗后为空，跳过")
            return

        # 保存数据
        self.save_to_database(cleaned_data)
        self.save_to_csv(cleaned_data, source)
        self.upload_to_hdfs(cleaned_data, source)

        print(f"{source} 数据处理完成\n")

    def run(self, sources=None):
        """
        运行数据处理流程

        Args:
            sources: 要处理的数据源列表，None 表示处理所有
        """
        if sources is None:
            sources = ['ecommerce', 'agriculture', 'market']

        for source in sources:
            self.process_source(source)

        print("\n所有数据处理完成")


def main():
    """主函数"""
    # 从命令行参数获取要处理的数据源
    sources = sys.argv[1:] if len(sys.argv) > 1 else None

    # 创建并运行数据处理器
    processor = DataProcessor()
    processor.run(sources)


if __name__ == '__main__':
    main()