# -*- coding: utf-8 -*-

"""
爬虫中间件
"""

import random
import logging
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class RandomUserAgentMiddleware:
    """随机User-Agent中间件"""
    
    def __init__(self, user_agent_pool):
        self.user_agent_pool = user_agent_pool
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        return cls(
            user_agent_pool=crawler.settings.get('USER_AGENT_POOL', [])
        )
    
    def process_request(self, request, spider):
        """为请求设置随机User-Agent"""
        if self.user_agent_pool:
            user_agent = random.choice(self.user_agent_pool)
            request.headers['User-Agent'] = user_agent
            self.logger.debug(f"Set User-Agent: {user_agent}")


class ProxyMiddleware:
    """代理中间件"""
    
    def __init__(self, proxy_pool, enable_proxy):
        self.proxy_pool = proxy_pool
        self.enable_proxy = enable_proxy
        self.current_proxy_index = 0
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        return cls(
            proxy_pool=crawler.settings.get('PROXY_POOL', []),
            enable_proxy=crawler.settings.get('ENABLE_PROXY', False)
        )
    
    def process_request(self, request, spider):
        """为请求设置代理"""
        if self.enable_proxy and self.proxy_pool:
            proxy = self._get_next_proxy()
            request.meta['proxy'] = proxy
            self.logger.debug(f"Set proxy: {proxy}")
    
    def _get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxy_pool:
            return None
        
        proxy = self.proxy_pool[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_pool)
        return proxy


class RetryMiddleware(RetryMiddleware):
    """重试中间件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
    
    def process_response(self, request, response, spider):
        """处理响应"""
        # 检查响应状态码
        if response.status in [403, 429, 500, 502, 503, 504]:
            self.logger.warning(f"Received status {response.status}, retrying...")
            return self._retry(request, spider) or response
        
        return response
    
    def process_exception(self, request, exception, spider):
        """处理异常"""
        self.logger.error(f"Request failed: {exception}")
        return super().process_exception(request, exception, spider)


class LoggingMiddleware:
    """日志中间件"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls()
    
    def process_request(self, request, spider):
        """记录请求"""
        self.logger.info(f"Requesting: {request.url}")
    
    def process_response(self, request, response, spider):
        """记录响应"""
        self.logger.info(f"Response: {response.status} - {request.url}")
        return response
    
    def process_exception(self, request, exception, spider):
        """记录异常"""
        self.logger.error(f"Exception: {exception} - {request.url}")


class SpiderMiddleware:
    """Spider中间件"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls()
    
    @classmethod
    def from_settings(cls, settings):
        return cls()
    
    def process_spider_input(self, response, result, spider):
        """处理spider输入"""
        for item_or_request in result:
            yield item_or_request
    
    def process_spider_output(self, result, response, spider):
        """处理spider输出"""
        for item_or_request in result:
            yield item_or_request
    
    def process_spider_exception(self, response, exception, spider):
        """处理spider异常"""
        self.logger.error(f"Spider exception: {exception}")
    
    def process_start_requests(self, start_requests, spider):
        """处理起始请求"""
        for request in start_requests:
            yield request
