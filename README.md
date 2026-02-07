# 基于Hadoop的贵州农产品价格监测分析系统

## 项目简介

本项目是一个基于Hadoop生态系统的农产品价格监测分析系统，通过爬虫技术抓取电商平台和农业信息网关于贵州农产品的信息数据，利用Hadoop生态进行数据存储、处理和分析，为农产品买家和平台运营者提供全面的价格信息和趋势预测。

## 系统架构

系统采用五层架构设计：
- **数据采集层**：Scrapy爬虫 + Kafka消息队列
- **数据存储层**：HDFS + HBase + MySQL
- **数据处理层**：Hive + MapReduce + Spark
- **数据分析层**：Spark MLlib + Prophet/LSTM预测模型
- **应用展现层**：Vue3 + Element Plus + ECharts

## 技术栈

| 层级 | 技术组件 |
|------|----------|
| 数据采集 | Python, Scrapy, Scrapy-Redis, Kafka |
| 数据存储 | Hadoop HDFS, HBase, MySQL |
| 数据处理 | Hive, MapReduce, Spark |
| 数据分析 | Spark MLlib, Prophet, TensorFlow |
| API服务 | Spring Boot, MyBatis, Redis |
| 前端展示 | Vue3, Element Plus, ECharts |
| 任务调度 | Airflow |

## 快速开始

### 环境要求

- JDK 11+
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Hadoop 3.3.x
- Hive 3.1.x
- Spark 3.3.x
- Kafka 2.8.x
- Redis 6.x

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-repo/hadoop-guizhou-agricultural-price-monitoring-system.git
cd hadoop-guizhou-agricultural-price-monitoring-system
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，配置数据库、Redis等连接信息
```

3. 初始化配置
```bash
# 创建项目目录
mkdir -p crawler data logs models scripts tests

# 初始化MySQL数据库
mysql -u root -p < backend/mysql/init.sql
```

4. 启动Hadoop集群
```bash
# 启动HDFS
start-dfs.sh

# 启动Hive
hive --service metastore &
hive --service hiveserver2 &

# 启动Spark
start-all.sh
```

5. 启动后端服务
```bash
cd backend/spring-boot-api
mvn clean package
java -jar target/agriculture-price-price-api-1.0.0.jar
```

6. 启动前端服务
```bash
cd frontend/vue3-web
npm install
npm run dev
```

7. 启动爬虫服务
```bash
cd crawler/scrapy_crawler
pip install -r requirements.txt
scrapy crawl ecommerce_spider
```

## 项目结构

```
hadoop-guizhou-agricultural-price-monitoring-system/
├── doc/                          # 项目文档
├── plans/                        # 设计文档
├── crawler/                      # 数据采集模块
├── hadoop/                       # Hadoop相关配置
├── backend/                      # 后端服务
├── frontend/                     # 前端项目
├── models/                       # 机器学习模型
├── scripts/                      # 脚本工具
├── tests/                        # 测试
├── logs/                         # 日志目录
└── data/                         # 数据目录
```

## 核心功能

### 1. 数据采集
- 支持多数据源爬取（电商平台、农业信息网、批发市场）
- 分布式爬虫架构
- 数据清洗和验证
- 反爬机制处理

### 2. 数据存储
- HDFS分布式存储
- Hive数据仓库（ODS/DWD/DWS/ADS四层架构）
- HBase实时查询
- MySQL元数据管理

### 3. 数据处理
- MapReduce批处理
- Spark SQL快速查询
- 数据倾斜处理
- 性能优化

### 4. 数据分析
- 价格趋势分析
- 价格预测（Prophet/LSTM）
- 异常检测
- 预警机制

### 5. 数据可视化
- 价格趋势图表
- 市场热力图
- 预警雷达图
- 报表导出

## API文档

API文档请参考：[`plans/API接口设计文档.md`](plans/API接口设计文档.md)

## 开发指南

详细的开发环境配置请参考：[`plans/开发环境配置说明.md`](plans/开发环境配置说明.md)

## 许可证

MIT License

## 联系方式

- 作者：蒋丹
- 指导教师：赵光煜
- 学校：软件工程三班
