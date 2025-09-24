# 🐳 Docker Hub 创建和部署指南

## 第一步：创建 Docker Hub 仓库

### 1. 注册 Docker Hub 账户
1. 访问 [Docker Hub](https://hub.docker.com)
2. 点击 "Sign Up" 创建账户
3. 验证邮箱地址

### 2. 创建仓库
1. 登录后点击 "Create Repository"
2. 填写仓库信息：
   - **Repository Name**: `genai-starter-kit`
   - **Description**: `GenerativeAI-Starter-Kit - AI Application Development Toolkit`
   - **Visibility**: Public (免费账户)

### 3. 仓库配置建议
- 添加详细的 README
- 设置适当的标签 (tags)
- 配置自动构建 (可选)

## 第二步：本地 Docker 准备

### 1. 登录 Docker Hub
```bash
docker login
# 输入您的 Docker Hub 用户名和密码
```

### 2. 验证登录状态
```bash
docker info | grep Username
```

## 第三步：构建和推送镜像

### 使用自动化脚本 (推荐)
```bash
# 设置您的 Docker Hub 用户名
export DOCKER_USERNAME="your-dockerhub-username"

# 运行部署脚本
./docker_hub_deploy.sh
```

### 手动构建推送
```bash
# 1. 构建多架构镜像
docker build -t your-username/genai-starter-kit:v0.2.0 .
docker build -t your-username/genai-starter-kit:latest .

# 2. 推送到 Docker Hub
docker push your-username/genai-starter-kit:v0.2.0
docker push your-username/genai-starter-kit:latest
```

## 第四步：验证部署

### 1. 检查 Docker Hub 仓库
- 访问 `https://hub.docker.com/r/your-username/genai-starter-kit`
- 确认镜像已上传
- 查看下载统计

### 2. 测试拉取镜像
```bash
# 删除本地镜像
docker rmi your-username/genai-starter-kit:latest

# 从 Docker Hub 拉取
docker pull your-username/genai-starter-kit:latest

# 运行测试
docker run -p 8000:8000 your-username/genai-starter-kit:latest
```

## 第五步：使用示例

### Docker Run
```bash
docker run -d \
  --name genai-app \
  -p 8000:8000 \
  your-username/genai-starter-kit:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  genai-app:
    image: your-username/genai-starter-kit:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped
```

## 常用命令速查

### 本地开发
```bash
# 快速测试构建
./docker_quick_test.sh

# 本地运行
./docker_local_run.sh

# 查看运行状态
docker ps
docker logs container-name
```

### Docker Hub 管理
```bash
# 登录
docker login

# 推送新版本
docker tag local-image:latest username/repo:v1.0.0
docker push username/repo:v1.0.0

# 查看远程标签
curl -s https://registry.hub.docker.com/v2/repositories/username/repo/tags/
```

## 故障排除

### 常见问题

1. **推送失败 - 权限问题**
   ```bash
   # 重新登录
   docker logout
   docker login
   ```

2. **镜像太大**
   ```bash
   # 使用 .dockerignore 排除不必要的文件
   # 使用多阶段构建
   # 清理缓存: RUN pip install --no-cache-dir
   ```

3. **构建失败**
   ```bash
   # 清除构建缓存
   docker system prune -a
   docker build --no-cache -t image:tag .
   ```

## 高级配置

### 多架构支持
```bash
# 创建构建器
docker buildx create --name multiplatform

# 构建多架构镜像
docker buildx build --platform linux/amd64,linux/arm64 \
  -t username/genai-starter-kit:latest --push .
```

### 自动化 CI/CD
GitHub Actions 示例：
```yaml
name: Docker Build and Push
on:
  push:
    tags: ['v*']
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        push: true
        tags: username/genai-starter-kit:latest
```

---

## 🎉 完成

您现在拥有：
- ✅ Docker Hub 公开仓库
- ✅ 自动化构建和推送流程
- ✅ 版本管理系统
- ✅ 用户友好的部署方式

其他用户现在可以通过以下方式使用您的应用：
```bash
docker pull your-username/genai-starter-kit:latest
docker run -p 8000:8000 your-username/genai-starter-kit:latest
