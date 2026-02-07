# .gitignore 配置文件

将以下内容复制到项目根目录的 `.gitignore` 文件中：

```gitignore
# ====================
# Python
# ====================
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/
.mypy_cache/
.dmypy.json
dmypy.json
venv/
ENV/
env/
.venv

# ====================
# Java / Maven
# ====================
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar
*.class
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar
hs_err_pid*
replay_pid*

# ====================
# Node.js / npm
# ====================
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*
dist/
dist-ssr/
*.local
.nuxt
.cache
.temp
.DS_Store
*.log
logs/
*.log.*

# ====================
# IDE
# ====================
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/
*.sublime-project
*.sublime-workspace
.history/
*.iml

# ====================
# Hadoop / Spark
# ====================
*.pid
*.out
*.err
spark-warehouse
metastore_db
derby.log

# ====================
# 数据文件
# ====================
data/
data/raw/
data/processed/
data/cache/
*.csv
*.json
*.xml
*.parquet
*.orc
*.avro
*.dat
*.db
*.sqlite
*.sqlite3

# ====================
# 日志文件
# ====================
logs/
*.log
log/
*.log.*

# ====================
# 临时文件
# ====================
tmp/
temp/
*.tmp
*.temp
*.bak
*.backup
*.old
*.swp
*.swo
.cache/
*.cache

# ====================
# 系统文件
# ====================
.DS_Store
.DS_Store?
._*
.Spotlight-Vars
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini
$RECYCLE.BIN/

# ====================
# 环境变量
# ====================
.env
.env.local
.env.development
.env.production
.env.test
*.env

# ====================
# 配置文件（敏感信息）
# ====================
config/secrets.yaml
config/secrets.yml
config/secrets.json
secrets.yaml
secrets.yml
secrets.json
*.key
*.pem
*.crt
*.p12
*.pfx

# ====================
# 模型文件
# ====================
models/saved/
*.h5
*.pkl
*.pickle
*.pt
*.pth
*.onnx
*.pb
*.tflite

# ====================
# 测试覆盖率
# ====================
coverage/
.coverage
.coverage.*
htmlcov/
*.cover
.hypothesis/
.pytest_cache/

# ====================
# Docker
# ====================
.dockerignore

# ====================
# 打包文件
# ====================
*.tar
*.tar.gz
*.tgz
*.zip
*.rar
*.7z

# ====================
# Scrapy
# ====================
.scrapy/
*.scrapy

# ====================
# Jupyter Notebook
# ====================
.ipynb_checkpoints/
*.ipynb

# ====================
# Airflow
# ====================
airflow.cfg
airflow.db
*.dagbag.pickle

# ====================
# Kafka
# ====================
kafkaafka-logs/
zookeeper-data/

# ====================
# HBase
# ====================
hbase-data/

# ====================
# MySQL
# ====================
mysql-data/
*.sql.gz

# ====================
# Redis
# ====================
redis-data/
dump.rdb

# ====================
# 其他
# ====================
*.pid
*.lock
.lock
```

## 使用说明

1. 将上述内容复制到项目根目录的 `.gitignore` 文件中
2. 该文件会忽略以下类型的文件和目录：
   - Python虚拟环境和缓存文件
   - Java/Maven编译产物
   - Node.js依赖和构建产物
   - IDE配置文件
   - 日志文件
   - 临时文件
   - 环境变量文件（包含敏感信息）
   - 数据文件
   - 模型文件
   - 数据库文件

3. 如果需要添加其他忽略规则，请按照相同格式添加
