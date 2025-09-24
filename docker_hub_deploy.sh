#!/bin/bash
# Docker Hub 部署脚本
# ===================

set -e

# 配置信息
DOCKER_USERNAME=${DOCKER_USERNAME:-"yynexus"}  # 替换为您的Docker Hub用户名
IMAGE_NAME="genai-starter-kit"
VERSION=${VERSION:-"v0.2.0"}
LATEST_TAG="latest"

echo "🐳 Docker Hub 部署开始..."

# 1. 检查Docker登录状态
echo "🔐 检查Docker Hub登录状态..."
if ! docker info | grep -q "Username:"; then
    echo "请先登录Docker Hub:"
    echo "docker login"
    read -p "按Enter继续，或Ctrl+C退出..."
    docker login
fi

# 2. 构建多标签镜像
echo "📦 构建Docker镜像..."
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} .
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${LATEST_TAG} .

# 3. 推送到Docker Hub
echo "🚀 推送镜像到Docker Hub..."
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${LATEST_TAG}

# 4. 验证推送结果
echo "✅ 推送完成! 镜像信息:"
echo "  仓库: ${DOCKER_USERNAME}/${IMAGE_NAME}"
echo "  标签: ${VERSION}, ${LATEST_TAG}"
echo "  拉取命令: docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

# 5. 创建Docker Compose文件用于部署
cat > docker-compose.yml << EOF
version: '3.8'

services:
  genai-starter-kit:
    image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}
    container_name: genai-kit-app
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
      - ENVIRONMENT=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 可选: 添加数据库服务
  # postgres:
  #   image: postgres:13
  #   environment:
  #     POSTGRES_DB: genai_db
  #     POSTGRES_USER: genai_user
  #     POSTGRES_PASSWORD: genai_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

# volumes:
#   postgres_data:
EOF

echo "📄 已创建 docker-compose.yml 文件"

# 6. 使用说明
echo ""
echo "🎯 使用说明:"
echo "  本地运行: docker-compose up -d"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo ""
echo "🌐 Docker Hub 仓库地址:"
echo "  https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
echo ""
echo "📋 其他用户使用方式:"
echo "  docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
echo "  docker run -p 8000:8000 ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

echo "✅ Docker Hub 部署完成!"
