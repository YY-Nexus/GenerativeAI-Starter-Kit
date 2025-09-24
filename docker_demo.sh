#!/bin/bash
# 一键Docker演示脚本
# ===================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数定义
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 主程序
echo "🐳 GenerativeAI-Starter-Kit Docker 完整演示"
echo "============================================"

# 1. 检查 Docker
print_step "检查 Docker 环境"
if ! command -v docker &> /dev/null; then
    print_error "Docker 未安装，请先安装 Docker Desktop"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    print_error "Docker 未运行，请启动 Docker Desktop"
    exit 1
fi

print_success "Docker 环境正常"

# 2. 清理之前的容器和镜像
print_step "清理旧的测试环境"
docker stop genai-demo 2>/dev/null || true
docker rm genai-demo 2>/dev/null || true
docker rmi genai-starter-kit:demo 2>/dev/null || true

# 3. 构建镜像
print_step "构建 Docker 镜像（这可能需要几分钟）"
if docker build -t genai-starter-kit:demo . --quiet; then
    print_success "镜像构建成功"
else
    print_error "镜像构建失败"
    exit 1
fi

# 4. 运行容器
print_step "启动 Docker 容器"
if docker run -d --name genai-demo -p 8000:8000 genai-starter-kit:demo; then
    print_success "容器启动成功"
else
    print_error "容器启动失败"
    exit 1
fi

# 5. 等待服务启动
print_step "等待服务启动"
for i in {1..30}; do
    if curl -f http://localhost:8000 >/dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 2
done
echo

# 6. 测试服务
print_step "测试服务响应"
if curl -f http://localhost:8000 >/dev/null 2>&1; then
    print_success "服务运行正常！"
    echo "🌐 访问地址: http://localhost:8000"
else
    print_warning "服务可能还在启动中"
    echo "📋 容器日志："
    docker logs genai-demo --tail 10
fi

# 7. 显示状态信息
print_step "容器状态信息"
docker ps --filter "name=genai-demo" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 8. 显示管理命令
echo ""
echo "🔧 管理命令："
echo "  查看日志:   docker logs -f genai-demo"
echo "  重启容器:   docker restart genai-demo"
echo "  停止容器:   docker stop genai-demo"
echo "  删除容器:   docker rm -f genai-demo"
echo "  删除镜像:   docker rmi genai-starter-kit:demo"
echo ""
echo "🚀 Docker Hub 部署："
echo "  1. 注册 Docker Hub 账户: https://hub.docker.com"
echo "  2. 本地登录: docker login"
echo "  3. 运行部署脚本: ./docker_hub_deploy.sh"
echo ""

print_success "Docker 演示完成！"

# 询问是否要推送到 Docker Hub
echo ""
read -p "是否要配置 Docker Hub 部署？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "准备 Docker Hub 部署配置"

    # 检查是否已登录
    if docker info | grep -q "Username:"; then
        USERNAME=$(docker info | grep "Username:" | awk '{print $2}')
        print_success "已登录 Docker Hub，用户名: $USERNAME"

        # 提供部署选项
        echo "选择部署方式："
        echo "1. 自动部署（推荐）"
        echo "2. 手动部署指南"
        read -p "请选择 (1/2): " -n 1 -r
        echo

        if [[ $REPLY == "1" ]]; then
            print_step "执行自动部署"
            export DOCKER_USERNAME=$USERNAME
            if [ -f "./docker_hub_deploy.sh" ]; then
                ./docker_hub_deploy.sh
            else
                print_error "未找到 docker_hub_deploy.sh 脚本"
            fi
        else
            print_step "手动部署步骤："
            echo "1. docker build -t $USERNAME/genai-starter-kit:v0.2.0 ."
            echo "2. docker push $USERNAME/genai-starter-kit:v0.2.0"
            echo "3. 访问 https://hub.docker.com/r/$USERNAME/genai-starter-kit"
        fi
    else
        print_warning "请先登录 Docker Hub:"
        echo "docker login"
    fi
fi
