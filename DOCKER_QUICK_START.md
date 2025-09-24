# 🚀 Docker 快速开始指南

## 一键体验 Docker 部署

```bash
# 1. 快速测试（推荐新手）
./docker_demo.sh

# 2. 快速构建测试
./docker_quick_test.sh

# 3. 本地完整部署
./docker_local_run.sh
```

## 🐳 Docker Hub 部署流程

### 第一步：准备 Docker Hub 账户

1. **注册账户**: [Docker Hub](https://hub.docker.com)
2. **创建仓库**: 点击 "Create Repository"
   - 名称: `genai-starter-kit`
   - 描述: `GenerativeAI AI Development Toolkit`
   - 可见性: Public

### 第二步：本地构建推送

```bash
# 1. 登录 Docker Hub
docker login

# 2. 一键部署到 Docker Hub
export DOCKER_USERNAME="your-username"  # 替换为您的用户名
./docker_hub_deploy.sh

# 3. 验证部署
docker pull your-username/genai-starter-kit:latest
```

### 第三步：使用您的镜像

```bash
# 其他用户可以这样使用您的镜像
docker pull your-username/genai-starter-kit:latest
docker run -p 8000:8000 your-username/genai-starter-kit:latest
```

## 📋 可用的 Docker 文件

- **Dockerfile**: 完整功能版本（较大）
- **Dockerfile.simple**: 精简快速版本（推荐测试）
- **requirements-docker.txt**: Docker 专用依赖列表

## 🔧 管理命令

```bash
# 查看镜像
docker images | grep genai

# 查看运行容器
docker ps

# 查看容器日志
docker logs container-name

# 停止所有相关容器
docker stop $(docker ps -q --filter ancestor=genai-starter-kit)

# 清理资源
docker system prune -a
```

## 🌐 Docker Hub 仓库示例

成功部署后，您的仓库将类似：
- URL: `https://hub.docker.com/r/your-username/genai-starter-kit`
- 拉取命令: `docker pull your-username/genai-starter-kit`
- 标签: `latest`, `v0.2.0`

## 📖 详细文档

- [完整 Docker 部署指南](./DOCKER_DEPLOYMENT_GUIDE.md)
- [Docker Hub 设置指南](./DOCKER_HUB_SETUP_GUIDE.md)

---

**🎉 现在就开始您的 Docker 之旅！**

1. 运行 `./docker_demo.sh` 体验完整流程
2. 注册 Docker Hub 账户
3. 执行 `./docker_hub_deploy.sh` 发布您的镜像
4. 分享给全世界使用！
