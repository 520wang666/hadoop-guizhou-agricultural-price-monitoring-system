# Spring Boot API Dockerfile
FROM openjdk:11-jre-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN groupadd -r spring && useradd -r -g spring spring

# 创建必要的目录
RUN mkdir -p /app/data /app/logs && \
    chown -R spring:spring /app

# 复制 JAR 文件（假设构建后的 JAR 文件名为 agriculture-api.jar）
COPY agriculture-api.jar /app/app.jar

# 设置权限
RUN chown spring:spring /app/app.jar

# 切换到非 root 用户
USER spring

# 设置环境变量
ENV JAVA_OPTS="-Xms512m -Xmx2g -XX:+UseG1GC -Djava.security.egd=file:/dev/./urandom"

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# 启动应用
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]