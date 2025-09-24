# 🚀 Docker操作核心命令速查

## 🎯 立即使用（推荐）

```bash
# 拉取并运行推荐版本
docker pull yanyuit/genai-starter-kit:v0.2.1
docker run -d --name genai-app -p 8000:8000 yanyuit/genai-starter-kit:v0.2.1

# 验证运行
curl http://localhost:8000/health
# 返回: {"status":"healthy","message":"Service is running normally","version":"0.2.0"}
```

## 🛠 本地构建

```bash
# 轻量级构建（推荐）
docker build -f Dockerfile.simple -t genai-starter-kit:custom .

# 完整版构建
docker build -f Dockerfile -t genai-starter-kit:full .
```

## 🔧 容器管理

```bash
# 查看运行状态
docker ps

# 查看日志
docker logs genai-app

# 停止和清理
docker stop genai-app
docker rm genai-app
```

## 🎪 自动化脚本

```bash
# 快速演示
./docker_demo.sh

# Docker Hub部署
./docker_hub_deploy.sh

# 完整测试
./docker_quick_test.sh
```

## 📊 重要信息

- **Docker Hub**: `yanyuit/genai-starter-kit`
- **推荐版本**: `v0.2.1` (6.51GB)
- **API端点**: `http://localhost:8000`
- **健康检查**: `/health`
- **API文档**: `/docs`

## 🎉 项目状态：✅ 完全就
