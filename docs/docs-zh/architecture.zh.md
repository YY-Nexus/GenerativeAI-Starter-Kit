<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 架构

<!-- TOC -->

* [软件组件概述](#软件组件概述)
* [NVIDIA AI 组件](#nvidia-ai-组件)
* [NVIDIA TensorRT-LLM 优化](#nvidia-tensorrt-llm-优化)
* [NVIDIA NIM for LLMs 容器](#nvidia-nim-for-llms-容器)
* [推理流程](#推理流程)
* [文档摄取与检索](#文档摄取与检索)
* [用户查询与响应生成](#用户查询与响应生成
* [LLM 推理服务器](#llm-推理服务器
* [向量数据库](#向量数据库

<!-- /TOC -->

## 软件组件概述

默认示例部署包含：

-推理和嵌入通过访问运行在 NVIDIA API Catalog 上的模型端点完成。

  大多数示例使用 [Meta Llama 3 70B Instruct](https://build.ngc.nvidia.com/meta/llama3-70b) 模型进行推理，使用 [Snowflake Arctic Embed L](https://build.ngc.nvidia.com/snowflake/arctic-embed-l) 模型进行嵌入。

  你也可以部署 NVIDIA NIM for LLMs 和 NVIDIA NeMo Retriever Embedding 微服务，以使用本地模型和本地 GPU。
  更多信息请参考 [](nim-llms.md) 示例。

* Chain Server 使用 [LangChain](https://github.com/langchain-ai/langchain/) 和 [LlamaIndex](https://www.llamaindex.ai/) 组合语言模型组件，便于从企业数据库构建问答系统

* [示例 Jupyter Notebooks](jupyter-server.md) 和 [](./frontend.md)，可用于交互式测试聊天系统

* [Milvus](https://milvus.io/docs/install_standalone-docker.md) 或 [pgvector](https://github.com/pgvector/pgvector) —— 嵌入存储在向量数据库中。Milvus 是一个开源向量数据库，支持 NVIDIA GPU 加速的向量检索。

该示例部署为你构建企业级 AI 解决方案提供了参考，实现最小化开发工作量。

## NVIDIA AI 组件

示例部署使用多种 NVIDIA AI 组件来定制和部署基于 RAG 的聊天机器人示例。

* [NVIDIA TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)
* [NVIDIA NIM for LLMs](https://docs.nvidia.com/nim/large-language-models/latest/index.html)

### NVIDIA TensorRT-LLM 优化

LLM 可通过 TensorRT-LLM 进行优化。
NVIDIA NIM for LLMs 使用 TensorRT-LLM 加速并最大化最新 LLM 的推理性能。
示例部署部署了一个由 TensorRT-LLM 优化的 Llama 3 8B 参数聊天模型。

### NVIDIA NIM for LLMs 容器

NVIDIA NIM for LLMs 容器简化了部署流程，提供高性能、低成本、低延迟的推理。
容器中的软件会自动检测你的 GPU 硬件，并决定使用 TensorRT-LLM 后端还是 vLLM 后端。

## 推理流程

要开始推理流程，需将 LLM 连接到示例向量数据库。
你可以上传文档，文档的嵌入将存储在向量数据库中，用于增强查询响应。
向量数据库中的知识可以是产品规格、HR 文档或财务表格等多种形式。
通过 RAG 可增强模型能力。

由于基础 LLM 未训练你的专有企业数据，且只训练到某一时间点，因此需要补充额外数据。
RAG 包含两个过程：
首先是 *检索* —— 从文档库、数据库或 API 中获取数据，这些数据都在基础模型知识之外。
其次是 *生成* —— 通过推理生成响应。

## 文档摄取与检索

RAG 以相关且最新的信息知识库为起点。
由于企业内部数据经常更新，文档摄取到知识库是一个持续过程，可设为定时任务。
接下来，将知识库内容传递给嵌入模型（如示例部署使用的 Snowflake Arctic Embedding L）。
嵌入模型将内容转换为向量，称为 *嵌入*。
