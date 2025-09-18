#!/bin/bash
# 一键发布 genai-starter-kit 到 PyPI 和 DockerHub
set -e

PKG_NAME="genai-starter-kit"
DOCKER_IMAGE="yyc3/genai-starter-kit"

# 构建并发布 PyPI 包
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload dist/*

# 构建并推送 Docker 镜像
DOCKER_TAG="latest"
docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
docker push $DOCKER_IMAGE:$DOCKER_TAG

echo "发布完成：PyPI 包和 Docker 镜像已推送。"
