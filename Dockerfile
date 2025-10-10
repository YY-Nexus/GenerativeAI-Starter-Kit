FROM python:3.14-slim

LABEL maintainer="YY-Nexus <contact@yynexus.com>"
LABEL description="GenerativeAI-Starter-Kit Docker Image"
LABEL version="v0.2.0"

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 安装应用
RUN pip install -e .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# 启动命令 - 使用修复的API
CMD ["python", "-m", "uvicorn", "docker_api:app", "--host", "0.0.0.0", "--port", "8000"]
