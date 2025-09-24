# Docker 部署完整指南

## 🐳 本地Docker运行

### 1. 快速开始

```bash
# 一键本地部署
./docker_local_run.sh
```

### 2. 手动步骤

```bash
# 构建镜像
docker build -t genai-starter-kit:latest .

# 运行容器
docker run -d --name genai-kit -p 8000:8000 genai-starter-kit:latest

# 查看状态
docker ps
docker logs genai-kit

# 访问应用
curl http://localhost:8000
```

### 3. Docker Compose 部署

```bash
# 使用docker-compose.yml（推荐）
docker-compose up -d

# 查看服务状态
docker-compose ps
docker-compose logs -f
```

## 🚀 Docker Hub 仓库创建

### 1. 准备工作

1. **注册Docker Hub账户**
   - 访问: <https://hub.docker.com>
   - 创建账户并验证邮箱

2. **本地登录Docker Hub**
   ```bash
   docker login
   # 输入用户名和密码
   ```

### 2. 推送到Docker Hub

```bash
# 自动部署到Docker Hub
./docker_hub_deploy.sh

# 或者手动执行：
DOCKER_USERNAME="你的用户名" ./docker_hub_deploy.sh
```

### 3. 手动推送步骤

```bash
# 1. 构建镜像（替换为你的用户名）
docker build -t yynexus/genai-starter-kit:v0.2.0 .
docker build -t yynexus/genai-starter-kit:latest .

# 2. 推送到Docker Hub
docker push yynexus/genai-starter-kit:v0.2.0
docker push yynexus/genai-starter-kit:latest

# 3. 验证推送
docker search yynexus/genai-starter-kit
```

## 🌐 Docker Hub 仓库配置

### 创建公开仓库

1. 登录Docker Hub
2. 点击 "Create Repository"
3. 填写信息：
   - Repository Name: `genai-starter-kit`
   - Description: `GenerativeAI-Starter-Kit - AI应用开发工具包`
   - Visibility: Public（免费）

### 仓库描述示例

```markdown
# GenerativeAI-Starter-Kit

🚀 一个完整的生成式AI应用开发工具包

## 特性
- 🤖 RAG（检索增强生成）示例
- 🎨 多模态AI应用
- 📝 文本分类微调
- 🔧 零配置快速启动

## 快速使用

### Docker 运行
```bash
docker pull yynexus/genai-starter-kit:latest
docker run -p 8000:8000 yynexus/genai-starter-kit:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  genai-app:
    image: yynexus/genai-starter-kit:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
```

## 文档
- GitHub: <https://github.com/YY-Nexus/GenerativeAI-Starter-Kit>
- 文档: <https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/blob/main/README.md>

## 支持的架构
- linux/amd64
- linux/arm64

## 许可证
MIT License


## 📋 常用Docker命令

### 容器管理
```bash
# 查看运行的容器
docker ps

# 查看所有容器
docker ps -a

# 停止容器
docker stop genai-kit

# 重启容器
docker restart genai-kit

# 删除容器
docker rm genai-kit

# 进入容器
docker exec -it genai-kit bash
```

### 镜像管理
```bash
# 查看本地镜像
docker images

# 删除镜像
docker rmi genai-starter-kit:latest

# 从Docker Hub拉取
docker pull yynexus/genai-starter-kit:latest

# 查看镜像详情
docker inspect yynexus/genai-starter-kit:latest
```

### 日志和监控
```bash
# 查看实时日志
docker logs -f genai-kit

# 查看容器资源使用
docker stats genai-kit

# 健康检查
docker healthcheck genai-kit
```

## 🔧 高级配置

### 环境变量配置
```bash
docker run -d \
  --name genai-kit \
  -p 8000:8000 \
  -e PYTHONPATH=/app \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  yynexus/genai-starter-kit:latest
```

### 持久化数据
```bash
docker run -d \
  --name genai-kit \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  yynexus/genai-starter-kit:latest
```

### 网络配置
```bash
# 创建自定义网络
docker network create genai-network

# 使用自定义网络运行
docker run -d \
  --name genai-kit \
  --network genai-network \
  -p 8000:8000 \
  yynexus/genai-starter-kit:latest
```

## 🚨 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 检查端口占用
   lsof -i :8000
   # 使用不同端口
   docker run -p 8001:8000 yynexus/genai-starter-kit:latest
   ```

2. **权限问题**
   ```bash
   # 以root用户运行
   docker run --user root yynexus/genai-starter-kit:latest
   ```

3. **内存不足**
   ```bash
   # 限制内存使用
   docker run -m 2g yynexus/genai-starter-kit:latest
   ```

### 调试技巧
```bash
# 进入容器调试
docker run -it --entrypoint /bin/bash yynexus/genai-starter-kit:latest

# 查看构建过程
docker build --no-cache -t genai-starter-kit:debug .

# 查看详细日志
docker logs --details genai-kit
```

## 📊 监控和维护

### Docker Health Check
```bash
# 查看健康状态
docker inspect --format='{{.State.Health.Status}}' genai-kit

# 手动执行健康检查
docker exec genai-kit curl -f http://localhost:8000/ || echo "Health check failed"
```

### 自动更新
```bash
#!/bin/bash
# update_container.sh
docker pull yynexus/genai-starter-kit:latest
docker stop genai-kit
docker rm genai-kit
docker run -d --name genai-kit -p 8000:8000 yynexus/genai-starter-kit:latest
```

---

## 🎉 完成

现在您已经拥有：
- ✅ 本地Docker运行环境
- ✅ Docker Hub仓库
- ✅ 自动化部署脚本
- ✅ 完整的使用文档

访问您的应用: <http://localhost:8000>
