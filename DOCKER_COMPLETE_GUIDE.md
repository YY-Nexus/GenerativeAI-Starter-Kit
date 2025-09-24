# 🐳 GenerativeAI-Starter-Kit Docker 完整使用指南

## 📋 概述

本项目已完全支持Docker容器化部署，提供两个版本的镜像：

- **轻量级版本** (`v0.2.1`): 6.51GB - 修复版本，推荐使用
- **完整版本** (`latest`): 9.94GB - 包含所有依赖

## 🚀 快速启动

### 1. 从Docker Hub拉取镜像

```bash
# 拉取推荐的轻量级版本
docker pull yanyuit/genai-starter-kit:v0.2.1

# 或拉取完整版本
docker pull yanyuit/genai-starter-kit:latest
```

### 2. 运行容器

```bash
# 运行轻量级版本（推荐）
docker run -d --name genai-app -p 8000:8000 yanyuit/genai-starter-kit:v0.2.1

# 运行完整版本
docker run -d --name genai-app -p 8000:8000 yanyuit/genai-starter-kit:latest
```

### 3. 验证部署

```bash
# 检查容器状态
docker ps

# 测试健康检查
curl http://localhost:8000/health

# 测试API根端点
curl http://localhost:8000/
```

## 🛠 本地构建

如果您想从源码构建镜像：

### 使用轻量级Dockerfile（推荐）

```bash
# 构建轻量级镜像
docker build -f Dockerfile.simple -t genai-starter-kit:custom .

# 运行自定义镜像
docker run -d --name genai-custom -p 8000:8000 genai-starter-kit:custom
```

### 使用完整版Dockerfile

```bash
# 构建完整镜像
docker build -f Dockerfile -t genai-starter-kit:full .

# 运行完整镜像
docker run -d --name genai-full -p 8000:8000 genai-starter-kit:full
```

## 🔧 自动化脚本

项目提供了便捷的自动化脚本：

### 快速演示
```bash
./docker_demo.sh
```
- 自动构建轻量级镜像
- 启动容器
- 运行API测试
- 显示访问说明

### Docker Hub部署
```bash
./docker_hub_deploy.sh
```
- 构建生产版本镜像
- 推送到Docker Hub
- 支持版本标记

### 快速测试
```bash
./docker_quick_test.sh
```
- 运行完整的容器测试套件
- 验证所有API端点

## 📚 API端点说明

容器启动后，可访问以下端点：

### 基础端点
- `GET /` - API根信息
- `GET /health` - 健康检查
- `GET /docs` - Swagger API文档
- `GET /info` - 系统信息

### 功能端点
- `POST /process-text` - 文本处理
  ```bash
  curl -X POST http://localhost:8000/process-text \
    -H "Content-Type: application/json" \
    -d '{"text": "测试文本", "task": "分析"}'
  ```

- `GET /demo` - 功能演示
  ```bash
  curl http://localhost:8000/demo
  ```

## 🏗 容器架构特性

### 安全特性
- 非root用户运行 (`appuser`)
- 最小权限原则
- 健康检查机制

### 性能优化
- 多阶段构建
- 依赖缓存
- 轻量级基础镜像

### 可维护性
- 清晰的日志记录
- 标准化环境变量
- 版本标记管理

## 🔄 容器管理

### 查看日志
```bash
docker logs genai-app
```

### 进入容器
```bash
docker exec -it genai-app bash
```

### 停止和清理
```bash
# 停止容器
docker stop genai-app

# 删除容器
docker rm genai-app

# 清理镜像
docker rmi yanyuit/genai-starter-kit:v0.2.1
```

### 更新镜像
```bash
# 拉取最新版本
docker pull yanyuit/genai-starter-kit:v0.2.1

# 重新启动容器
docker stop genai-app
docker rm genai-app
docker run -d --name genai-app -p 8000:8000 yanyuit/genai-starter-kit:v0.2.1
```

## 🌐 Docker Hub 仓库信息

**仓库地址**: `yanyuit/genai-starter-kit`
**访问链接**: <https://hub.docker.com/r/yanyuit/genai-starter-kit>

### 可用标签
- `latest` - 完整版本 (9.94GB)
- `v0.2.1` - 轻量级修复版本 (6.51GB) **推荐**
- `v0.2.0` - 历史版本

## 🚨 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 使用其他端口
   docker run -d --name genai-app -p 8080:8000 yanyuit/genai-starter-kit:v0.2.1
   ```

2. **内存不足**
   ```bash
   # 限制内存使用
   docker run -d --name genai-app -p 8000:8000 -m 4g yanyuit/genai-starter-kit:v0.2.1
   ```

3. **容器无法启动**
   ```bash
   # 查看详细日志
   docker logs genai-app

   # 检查容器状态
   docker inspect genai-app
   ```

### 性能调优

1. **增加内存限制**
   ```bash
   docker run -d --name genai-app -p 8000:8000 -m 8g yanyuit/genai-starter-kit:v0.2.1
   ```

2. **挂载本地数据**
   ```bash
   docker run -d --name genai-app -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     yanyuit/genai-starter-kit:v0.2.1
   ```

## 📝 开发说明

如果您需要修改代码并重新构建：

1. 修改源代码
2. 使用 `docker build` 重新构建
3. 测试新镜像
4. 推送到Docker Hub（如果需要）

## 🤝 贡献

欢迎提交Issue和Pull Request来改进Docker支持！

## 📄 许可证

遵循项目根目录的LICENSE.md文件
