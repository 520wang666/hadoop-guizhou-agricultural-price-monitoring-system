# Crawler Dockerfile - 基于 Python 3.10
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制爬虫代码
COPY . /app/scrapy_crawler

# 创建数据目录
RUN mkdir -p /app/data /app/output

# 设置环境变量
ENV PYTHONPATH=/app/scrapy_crawler
ENV SCRAPY_SETTINGS_MODULE=scrapy_crawler.settings

# 暴露端口（如果需要）
# EXPOSE 8888

# 默认命令
CMD ["bash", "-c", "tail -f /dev/null"]