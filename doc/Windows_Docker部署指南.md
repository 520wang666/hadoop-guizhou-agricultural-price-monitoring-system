# Windows Docker 部署指南

本指南介绍如何在 Windows 环境下使用 Docker Desktop 部署贵州农产品价格监测系统。

## 目录

- [环境要求](#环境要求)
- [安装 Docker Desktop](#安装-docker-desktop)
- [Docker Desktop 配置](#docker-desktop-配置)
- [项目部署](#项目部署)
- [访问服务](#访问服务)
- [数据持久化](#数据持久化)
- [常见问题](#常见问题)

---

## 环境要求

### 硬件要求

- **操作系统**: Windows 10/11 (64位)
- **处理器**: 支持 Hyper-V 的 CPU
- **内存**: 至少 16GB RAM (推荐 32GB)
- **磁盘空间**: 至少 50GB 可用空间

### 软件要求

- Docker Desktop for Windows 4.x 或更高版本
- Windows PowerShell 或命令提示符
- (可选) Git 用于克隆项目

---

## 安装 Docker Desktop

### 下载和安装

1. 访问 [Docker Desktop 官网](https://www.docker.com/products/docker-desktop/)
2. 下载 Windows 版本
3. 运行安装程序，按照提示完成安装

### 启用 Hyper-V

安装过程中，Docker 会自动启用 Hyper-V。如果需要手动启用：

1. 以管理员身份打开 PowerShell
2. 运行以下命令：

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

3. 重启计算机

### WSL 2 后端（推荐）

Docker Desktop 2.3.0+ 支持 WSL 2 后端，性能更好：

1. 以管理员身份打开 PowerShell
2. 运行以下命令：

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

3. 重启计算机
4. 下载并安装 [WSL 2 Linux kernel update 包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
5. 在 PowerShell 中运行：

```powershell
wsl --set-default-version 2
```

---

## Docker Desktop 配置

### 1. 启动 Docker Desktop

安装完成后启动 Docker Desktop，等待其完全启动（状态栏显示 "Docker Desktop is running"）。

### 2. 配置资源

打开 Docker Desktop 设置：

1. 点击任务栏 Docker 图标
2. 选择 **Settings** (齿轮图标)
3. 在 **Resources** 部分配置：

#### 内存配置

- **Memory**: 至少 8GB，推荐 12-16GB
- **Swap**: 2GB

#### 处理器配置

- **Processors**: 至少 4 核，推荐 6 核或更多

#### 磁盘配置

- **Disk image size**: 至少 50GB

### 3. 配置文件共享

在 **Settings > Resources > File Sharing** 中：

1. 点击 **"+"** 按钮
2. 添加项目根目录：`D:\Code_Workspace\hadoop-guizhou-agricultural-price-monitoring-system`
3. 如果提示需要凭证，输入 Windows 登录凭据

### 4. 配置网络

在 **Settings > Resources > Network** 中：

- 确保启用 **Docker Desktop DNS server**
- 添加 DNS 服务器（如：8.8.8.8, 8.8.4.4）

### 5. 配置代理（如需要）

如果网络需要代理，在 **Settings > Resources > Proxies** 中配置。

---

## 项目部署

### 1. 验证 Docker 安装

在 PowerShell 中运行：

```powershell
docker --version
docker-compose --version
```

应该显示 Docker 和 Docker Compose 的版本号。

### 2. 进入项目目录

```powershell
cd D:\Code_Workspace\hadoop-guizhou-agricultural-price-monitoring-system
```

### 3. 检查配置文件

确保以下文件存在且配置正确：

- `docker-compose.yml` - Docker Compose 配置文件
- `hadoop/hdfs/core-site.xml` - HDFS 配置
- `hadoop/hdfs/hdfs-site.xml` - HDFS 配置
- `hadoop/hive/hive-site.xml` - Hive 配置

### 4. 构建和启动服务

#### 首次启动

```powershell
# 构建所有服务镜像
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 启动特定服务

```powershell
# 仅启动基础服务（MySQL、Redis）
docker-compose up -d mysql redis

# 启动 Hadoop 生态
docker-compose up -d namenode datanode hive-metastore hive-server

# 启动 Spark
docker-compose up -d spark-master spark-worker

# 启动 Airflow
docker-compose up -d postgres airflow-init airflow-webserver airflow-scheduler
```

### 5. 初始化 HDFS

等待 Hadoop 服务完全启动后（约 2-3 分钟）：

```powershell
# 进入 namenode 容器
docker exec -it agriculture-namenode bash

# 格式化 namenode（仅首次运行需要）
hdfs namenode -format

# 创建必要的目录
hdfs dfs -mkdir -p /agriculture/raw
hdfs dfs -mkdir -p /agriculture/detail
hdfs dfs -mkdir -p /agriculture/summary
hdfs dfs -mkdir -p /agriculture/application
hdfs dfs -mkdir -p /user/hive/warehouse

# 退出容器
exit
```

### 6. 初始化 Hive

等待 Hive 服务启动后：

```powershell
# 进入 hive-server 容器
docker exec -it agriculture-hive-server bash

# 启动 Hive CLI
beeline -u jdbc:hive2://localhost:10000

# 在 Hive CLI 中运行
CREATE DATABASE IF NOT EXISTS agriculture;
USE agriculture;

# 退出 Hive CLI
!quit

# 退出容器
exit
```

---

## 访问服务

### 服务端口映射

| 服务 | 容器内端口 | 宿主机端口 | 访问地址 |
|------|-----------|-----------|---------|
| MySQL | 3306 | 3306 | localhost:3306 |
| Redis | 6379 | 6379 | localhost:6379 |
| HDFS NameNode | 9000 | 9000 | localhost:9000 |
| HDFS Web UI | 9870 | 9870 | http://localhost:9870 |
| Hive Metastore | 9083 | 9083 | localhost:9083 |
| HiveServer2 | 10000 | 10000 | localhost:10000 |
| Hive Web UI | 10002 | 10002 | http://localhost:10002 |
| Spark Master Web | 8080 | 8081 | http://localhost:8081 |
| Spark Worker Web | 8042 | 8042 | http://localhost:8042 |
| Airflow Web | 8080 | 8080 | http://localhost:8080 |
| Backend API | 8080 | 8080 | http://localhost:8080 |
| Frontend | 80 | 80 | http://localhost |
| PostgreSQL | 5432 | 5432 | localhost:5432 |

**注意**：Airflow 和 Backend API 都使用 8080 端口。生产环境建议修改端口配置以避免冲突。

### 访问 Web 界面

#### HDFS Web UI

1. 浏览器访问: http://localhost:9870
2. 查看 HDFS 文件系统状态

#### Hive Web UI

1. 浏览器访问: http://localhost:10002
2. 查询 Hive 服务状态

#### Spark Master Web UI

1. 浏览器访问: http://localhost:8081
2. 查看 Spark 应用和任务状态

#### Airflow Web UI

1. 浏览器访问: http://localhost:8080
2. 默认用户名: `admin`
3. 默认密码: `admin`
4. 查看 DAG 和任务执行状态

#### 前端界面

1. 浏览器访问: http://localhost
2. 查看农产品价格监测系统前端

---

## 数据持久化

### Docker 卷

Docker Compose 配置使用以下命名卷来持久化数据：

```yaml
volumes:
  mysql-data:           # MySQL 数据
  redis-data:           # Redis 数据
  namenode-data:        # HDFS NameNode 数据
  datanode-data:        # HDFS DataNode 数据
  hive-metastore-data:  # Hive 元数据
  spark-logs:           # Spark 日志
  airflow-db:           # Airflow 数据库
  airflow-logs:         # Airflow 日志
  airflow-dags:         # Airflow DAG 文件
  crawler-data:         # 爬虫数据
```

### 查看和管理卷

```powershell
# 列出所有卷
docker volume ls

# 查看卷详细信息
docker volume inspect agriculture-mysql-data

# 删除卷（谨慎使用）
docker volume rm agriculture-mysql-data
```

### 备份数据

#### 备份 MySQL

```powershell
# 导出数据库
docker exec agriculture-mysql mysqldump -u root -pRoot123! agriculture > backup.sql

# 导出 Hive 元数据库
docker exec agriculture-mysql mysqldump -u root -pRoot123! hive > hive_backup.sql
```

#### 备份 HDFS 数据

```powershell
# 将 HDFS 数据导出到本地
docker exec agriculture-namenode hdfs dfs -get /agriculture ./agriculture_backup
```

#### 恢复数据

```powershell
# 恢复 MySQL
docker exec -i agriculture-mysql mysql -u root -pRoot123! agriculture < backup.sql

# 将本地数据导入 HDFS
docker exec agriculture-namenode hdfs dfs -put ./agriculture_backup /agriculture
```

---

## 常见问题

### 1. 服务启动失败

#### 检查日志

```powershell
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs mysql
docker-compose logs namenode
docker-compose logs airflow-scheduler
```

#### 常见原因和解决方法

**端口冲突**

```powershell
# 查看端口占用
netstat -ano | findstr :8080

# 停止占用端口的进程
taskkill /PID <进程ID> /F
```

**内存不足**

- 增加 Docker Desktop 内存分配
- 关闭不必要的应用释放内存

**磁盘空间不足**

```powershell
# 清理 Docker 未使用的资源
docker system prune -a
```

### 2. HDFS 无法连接

**问题**: Spark 或其他服务无法连接到 HDFS

**解决方法**:

1. 检查 NameNode 是否运行

```powershell
docker ps | grep namenode
```

2. 检查 HDFS 配置中的 `fs.defaultFS` 是否正确

3. 验证网络连接

```powershell
docker exec agriculture-namenode ping datanode
```

### 3. Hive 元数据连接失败

**问题**: HiveServer2 无法连接到 MySQL

**解决方法**:

1. 确保 MySQL 容器正在运行

```powershell
docker ps | grep mysql
```

2. 检查 MySQL 是否准备就绪

```powershell
docker exec agriculture-mysql mysqladmin ping -h localhost
```

3. 检查 hive-site.xml 中的连接 URL 是否正确（应使用服务名 `mysql`）

### 4. Airflow DAG 无法加载

**问题**: Airflow Web UI 中看不到 DAG

**解决方法**:

1. 检查 DAG 文件是否正确挂载

```powershell
docker exec agriculture-airflow-scheduler ls -la /opt/airflow/dags
```

2. 检查 DAG 文件语法

```powershell
docker exec agriculture-airflow-scheduler python -m py_compile /opt/airflow/dags/data_collection_dag.py
```

3. 查看 Airflow Scheduler 日志

```powershell
docker-compose logs airflow-scheduler | grep DAG
```

### 5. Spark 任务提交失败

**问题**: Airflow 中的 Spark 任务无法执行

**解决方法**:

1. 检查 Spark Master 是否运行

```powershell
docker ps | grep spark-master
```

2. 检查 DAG 中的 Spark 配置

```python
conf={
    'spark.master': 'spark://spark-master:7077',  # 确保使用正确的主机名
    # ...
}
```

3. 检查 Spark 应用文件路径是否正确挂载

### 6. 爬虫任务无法执行

**问题**: Airflow 中的爬虫任务失败

**解决方法**:

1. 检查爬虫容器是否运行

```powershell
docker ps | grep crawler
```

2. 手动测试爬虫

```powershell
docker exec agriculture-crawler scrapy crawl ecommerce_spider
```

3. 检查网络连接（爬虫需要访问外部网站）

### 7. Windows 文件系统问题

**问题**: Docker 容器无法访问 Windows 文件

**解决方法**:

1. 检查文件共享设置

2. 重启 Docker Desktop

3. 尝试使用 WSL 2 后端而不是 Hyper-V

4. 如果出现权限问题，在 Docker Desktop 中重新配置文件共享凭据

### 8. 性能问题

**问题**: 服务运行缓慢

**优化建议**:

1. **增加 Docker 资源分配**
   - 内存: 12-16GB
   - CPU: 6 核或更多

2. **使用 WSL 2 后端**（性能优于 Hyper-V）

3. **减少日志级别**
   - 修改各服务的日志配置

4. **优化 Spark 配置**
   - 调整 executor 数量和内存

### 9. 容器无法访问网络

**问题**: 容器无法访问外部网络（如爬虫无法获取网页）

**解决方法**:

1. 检查 Docker Desktop 网络配置

2. 配置代理（如果需要）

3. 检查 Windows 防火墙设置

4. 测试网络连接

```powershell
docker exec agriculture-crawler ping google.com
```

### 10. 数据丢失

**问题**: 重启容器后数据丢失

**解决方法**:

1. 确保使用 Docker 卷而不是绑定挂载用于数据目录

2. 定期备份数据（见"数据持久化"章节）

3. 检查 docker-compose.yml 中的卷配置

---

## 管理命令

### 启动和停止

```powershell
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose stop

# 重启所有服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器及数据卷（谨慎使用）
docker-compose down -v
```

### 查看状态

```powershell
# 查看容器状态
docker-compose ps

# 查看资源使用情况
docker stats

# 查看特定容器日志
docker logs agriculture-namenode
```

### 进入容器

```powershell
# 进入 namenode
docker exec -it agriculture-namenode bash

# 进入 mysql
docker exec -it agriculture-mysql mysql -u root -p

# 进入 airflow-scheduler
docker exec -it agriculture-airflow-scheduler bash
```

---

## 更新和维护

### 更新服务

```powershell
# 拉取最新镜像
docker-compose pull

# 重新构建镜像
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

### 清理资源

```powershell
# 清理未使用的镜像
docker image prune

# 清理未使用的容器
docker container prune

# 清理未使用的网络
docker network prune

# 清理所有未使用的资源
docker system prune -a
```

---

## 生产环境建议

1. **配置 SSL/TLS**
   - 为 Web 界面配置 HTTPS

2. **修改默认密码**
   - 更改所有服务的默认密码

3. **使用外部数据库**
   - 生产环境使用独立数据库服务器

4. **配置监控**
   - 集成 Prometheus + Grafana

5. **配置日志收集**
   - 使用 ELK Stack 或类似方案

6. **配置备份策略**
   - 定期自动备份所有数据

7. **使用多节点部署**
   - HDFS 集群使用多个 DataNode
   - Spark 使用多个 Worker

---

## 获取帮助

如果遇到本指南未涵盖的问题：

1. 查看服务日志: `docker-compose logs <服务名>`
2. 查看 Docker Desktop 日志
3. 访问各服务官方文档
4. 在项目 Issues 中报告问题

---

## 版本信息

- Docker Desktop: 4.x+
- Docker Compose: 2.x+
- 本指南最后更新: 2026-02-07