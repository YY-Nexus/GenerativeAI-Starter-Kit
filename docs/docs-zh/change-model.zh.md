<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 更换推理或嵌入模型

<!-- TOC -->

* [API Catalog 模型](#api-catalog-模型)
* [更换推理模型](#更换推理模型)
* [更换嵌入模型](#更换嵌入模型)
* [本地微服务](#本地微服务)

<!-- /TOC -->

## API Catalog 模型

### 更换推理模型

可通过启动 Chain Server 时设置 `APP_LLM_MODELNAME` 环境变量指定模型。例如：

```console
APP_LLM_MODELNAME='mistralai/mixtral-8x7b-instruct-v0.1' docker compose up -d --build
```

可通过以下方式获取模型名称：

* 浏览 <https://build.ngc.nvidia.com/explore/discover>。
  查看示例 Python 代码，获取 `client.chat.completions.create` 方法的 `model` 参数。

* 安装 [langchain-nvidia-ai-endpoints](https://pypi.org/project/langchain-nvidia-ai-endpoints/) 包。
  使用 `ChatNVIDIA` 实例的 `get_available_models()` 方法列出模型。

### 更换嵌入模型

可通过启动 Chain Server 时设置 `APP_EMBEDDINGS_MODELNAME` 环境变量指定嵌入模型。例如：

```console
APP_EMBEDDINGS_MODELNAME='NV-Embed-QA' docker compose up -d --build
```

可通过以下方式获取嵌入模型名称：

* 浏览 <https://build.ngc.nvidia.com/explore/retrieval>。
  查看示例 Python 代码，获取 `client.embeddings.create` 方法的 `model` 参数。

* 安装 [langchain-nvidia-ai-endpoints](https://pypi.org/project/langchain-nvidia-ai-endpoints/) 包。
  使用 `NVIDIAEmbeddings` 实例的 `get_available_models()` 方法列出模型。

## 本地微服务

NVIDIA NIM 容器的模型可在 `docker-compose-nim-ms.yaml` 文件中指定。

编辑 `RAG/examples/local_deploy/docker-compose-nim-ms.yaml`，指定包含模型名称的镜像名。例如：

```yaml
services:
  nemollm-inference:
    container_name: nemollm-inference-microservice
    image: nvcr.io/nim/meta/<image>:<tag>
    ...

  nemollm-embedding:
    container_name: nemo-retriever-embedding-microservice
    image: nvcr.io/nim/<image>:<tag>

  ranking-ms:
    container_name: nemo-retriever-ranking-microservice
    image: nvcr.io/nim/<image>:<tag>
```

可通过如下命令获取可用模型名：

* 运行 `ngc registry image list "nim/*"`
