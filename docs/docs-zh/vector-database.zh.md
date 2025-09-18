<!--
  SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 向量数据库自定义
<!-- TOC -->

* [可用向量数据库](#可用向量数据库)
* [Milvus GPU 加速配置](#milvus-gpu-加速配置)
* [pgvector 配置](#pgvector-配置
* [外部 Milvus 或 pgvector 支持](#外部-milvus-或-pgvector-支持
* [新增向量存储](#新增向量存储
* [LlamaIndex 框架](#llamaindex-框架
* [LangChain 框架](#langchain-框架

<!-- /TOC -->

## 可用向量数据库

示例默认通过 Docker Compose 部署 Milvus（仅 CPU）。
如需 GPU 加速，需安装 NVIDIA Container Toolkit。

各框架支持的向量数据库如下：

LlamaIndex：Milvus、pgvector
LangChain：FAISS、Milvus、pgvector

常见自定义方式：

使用 GPU 加速的 Milvus。
用 pgvector 替代 Milvus（仅 CPU）。
使用自有向量数据库，避免每个 RAG 示例都部署数据库。

## Milvus GPU 加速配置

1. 编辑 `RAG/examples/local_deploy/docker-compose-vectordb.yaml`，修改 Milvus 服务：

   -镜像标签加 `-gpu` 后缀：

     ```yaml
     milvus:
       container_name: milvus-standalone
       image: milvusdb/milvus:v2.4.5-gpu
       ...
     ```

   -增加 GPU 资源预留：

     ```yaml
     ...
     depends_on:
       - "etcd"
       - "minio"
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               capabilities: ["gpu"]
               device_ids: ['${VECTORSTORE_GPU_DEVICE_ID:-0}']  
     profiles: ["nemo-retriever", "milvus", ""]
     ```

2. 停止并启动容器：

   ```console
   docker compose down
   docker compose up -d --build
   ```

   注意：如与 `local-nim` 一同部署 milvus，需用 `milvus`

profile：

   docker compose --profile local-nim --profile milvus up -d --build

3.可选：查看 chain server 日志确认数据库运行状态。

   1. 查看日志：

   ```console
   # 此处补充日志命令，例如：
   docker compose logs milvus-standalone
   ```
