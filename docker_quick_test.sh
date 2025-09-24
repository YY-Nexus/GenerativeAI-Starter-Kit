#!/bin/bash
# 快速Docker测试脚本
# ===================

echo "🐳 Docker 快速测试"

# 检查Docker状态
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker未运行，请启动Docker Desktop"
    exit 1
fi

echo "✅ Docker运行正常"

# 构建镜像（使用缓存加速）
echo "📦 构建测试镜像..."
docker build -t genai-test:latest . || {
    echo "❌ 镜像构建失败"
    exit 1
}

echo "✅ 镜像构建成功"

# 快速测试运行
echo "🚀 启动测试容器..."
docker run -d --name genai-test-container -p 8001:8000 genai-test:latest

# 等待启动
sleep 10

# 检查容器状态
if docker ps | grep -q genai-test-container; then
    echo "✅ 容器启动成功"
    echo "🌐 测试访问: http://localhost:8001"

    # 尝试健康检查
    if curl -f http://localhost:8001 >/dev/null 2>&1; then
        echo "✅ 应用响应正常"
    else
        echo "⚠️ 应用可能还在启动中，请稍后测试"
        docker logs genai-test-container --tail 10
    fi
else
    echo "❌ 容器启动失败"
    docker logs genai-test-container
fi

echo ""
echo "🔧 管理命令:"
echo "  查看日志: docker logs -f genai-test-container"
echo "  停止容器: docker stop genai-test-container"
echo "  清理容器: docker rm -f genai-test-container"
echo "  清理镜像: docker rmi genai-test:latest"
