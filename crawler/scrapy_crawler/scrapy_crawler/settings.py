# -*- coding: utf-8 -*-

"""
Scrapy爬虫配置文件
"""

# Scrapy项目名称
BOT_NAME = 'scrapy_crawler'

# Scrapy爬虫模块
SPIDER_MODULES_MODULES = ['scrapy_crawler.spiders']
NEWSPIDER_MODULE = 'scrapy_crawler.spiders'

# ====================
# 并发设置
# ====================
# 并发请求数
CONCURRENT_REQUESTS = 16

# 每个域名的并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 下载延迟（秒）
DOWNLOAD_DELAY = 2

# ====================
# 去重设置
# ====================
# 启用去重
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# 去重记录数量
DUPEFILTER_DEBUG = False

# ====================
# Redis分布式爬虫设置
# ====================
# Redis主机
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis数据库
REDIS_DB = 0

# Redis密码
REDIS_PASSWORD = ''

# ====================
# User-Agent设置
# ====================
# 默认User-Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# User-Agent池
USER_AGENT_POOL = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]

# ====================
# 代理设置
# ====================
# 启用代理
ENABLE_PROXY = False

# 代理池
PROXY_POOL = [
    # 'http://proxy1:port',
    # 'http://proxy2:port',
]

# ====================
# 中间件设置
# ====================
DOWNLOADER_MIDDLEWARES = {
    'scrapy_crawler.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_crawler.middlewares.ProxyMiddleware': 410,
    'scrapy_crawler.middlewares.RetryMiddleware': 500,
}

# ====================
# 管道设置
# ====================
ITEM_PIPELINES = {
    'scrapy_crawler.pipelines.ValidationPipeline': 200,
    'scrapy_crawler.pipelines.CleaningPipeline': 300,
    'scrapy_crawler.pipelines.KafkaPipeline': 400,
    'scrapy_crawler.pipelines.HDFSPipeline': 500,
}

# ====================
# 日志设置
# ====================
# 日志级别
LOG_LEVEL = 'INFO'

# 日志文件
LOG_FILE = 'logs/crawler/scrapy_crawler.log'

# 日志格式
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# ====================
# 超时设置
# ====================
# 下载超时（秒）
DOWNLOAD_TIMEOUT = 30

# ====================
# 重试设置
# ====================
# 最大重试次数
RETRY_TIMES = 3

# 重试延迟（秒）
RETRY_DELAY = 5

# ====================
# 其他设置
# ====================
# 遵守robots.txt
ROBOTSTXT_OBEY = False

# 启用Cookie
COOKIES_ENABLED = True

# 编码
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
}

# ====================
# 数据源配置
# ====================
# 数据源配置文件路径
SOURCES_CONFIG = 'crawler/config/sources.yaml'

# ====================
# Kafka配置
# ====================
# Kafka主题
KAFKA_TOPIC = 'price-data'

# Kafka服务器
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# ====================
# HDFS配置
# ====================
# HDFS路径
HDFS_PATH = '/agriculture/raw/ods_agri_price_raw'

# HDFS文件格式
HDFS_FILE_FORMAT = 'json'
