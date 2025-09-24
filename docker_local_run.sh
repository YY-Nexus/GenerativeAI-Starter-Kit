# Docker 部署指南
# ===============

# 1. 本地Docker构建和运行
echo "🐳 开始Docker本地部署..."

# 构建Docker镜像
echo "📦 构建Docker镜像..."
docker build -t genai-starter-kit:latest .

# 查看构建的镜像
echo "📋 查看构建的镜像..."
docker images | grep genai-starter-kit

# 运行Docker容器
echo "🚀 启动Docker容器..."
docker run -d \
  --name genai-kit-container \
  -p 8000:8000 \
  -e PYTHONPATH=/app \
  genai-starter-kit:latest

# 查看运行状态
echo "📊 检查容器运行状态..."
docker ps | grep genai-kit-container

# 查看容器日志
echo "📋 查看容器日志..."
docker logs genai-kit-container

echo "✅ 本地Docker部署完成!"
echo "🌐 访问地址: http://localhost:8000"

# 测试API端点
echo "🔍 测试API端点..."
sleep 5
curl -X GET "http://localhost:8000/" || echo "API测试失败，请检查容器状态"

echo "📝 常用Docker命令:"
echo "  停止容器: docker stop genai-kit-container"
echo "  重启容器: docker restart genai-kit-container"
echo "  删除容器: docker rm -f genai-kit-container"
echo "  查看日志: docker logs -f genai-kit-container"
