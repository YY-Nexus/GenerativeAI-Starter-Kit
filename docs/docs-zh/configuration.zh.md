<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 软件组件配置
<!-- TOC -->

* [环境变量配置](#环境变量配置)
* [Milvus](#milvus)
* [Pgvector](#pgvector)
* [Chain Server](#chain-server)
* [RAG Playground](#rag-playground)

<!-- /TOC -->

## 环境变量配置

以下部分列出 `docker-compose.yaml` 文件中使用的环境变量。

## Milvus

Milvus 是默认的向量数据库服务器。
可通过如下环境变量配置 Milvus：

<dl>
<dt>DOCKER_VOLUME_DIRECTORY</dt>
<dd>指定主机上用于向量数据库文件的挂载卷位置。
默认值为当前工作目录下的 `./volumes/milvus`。
</dd>
</dl>

## Pgvector

Pgvector 是另一种向量数据库服务器。
可通过如下环境变量配置 pgvector：

<dl>
<dt>DOCKER_VOLUME_DIRECTORY</dt>
<dd>指定主机上用于向量数据库文件的挂载卷位置。
默认值为当前工作目录下的 `./volumes/data`。
</dd>
<dt>POSTGRES_PASSWORD</dt>
<dd>pgvector 认证密码。默认值为 `password`。</dd>
<dt>POSTGRES_USER</dt>
<dd>pgvector 认证用户名。默认值为 `postgres`。</dd>
<dt>POSTGRES_DB</dt>
<dd>数据库实例名。默认值为 `api`。</dd>
</dl>

## Chain Server

Chain Server 是核心组件，负责与 LLM 推理服务器和 Milvus 服务器交互以获取响应。
可通过如下环境变量配置服务器：

<dl>
<dt>APP_VECTORSTORE_URL</dt>
<dd>向量数据库服务器的 URL。</dd>
<dt>APP_VECTORSTORE_NAME</dt>
<dd>向量数据库厂商名。可选值：`milvus` 或 `pgvector`。</dd>
<dt>COLLECTION_NAME</dt>
<dd>向量数据库中的示例集合名。</dd>
<dt>APP_LLM_SERVERURL</dt>
<dd>NVIDIA NIM for LLMs 的 URL。</dd>
<dt>APP_LLM_MODELNAME</dt>
<dd>NIM for LLMs 使用的模型名。</dd>
<dt>APP_LLM_MODELENGINE</dt>
<dd>托管模型的后端名。仅支持 `nvidia-ai-endpoints`，用于云端或本地 NIM for LLMs。</dd>
<dt>APP_RETRIEVER_TOPK</dt>
<dd>检索相关结果数量。默认值为 `4`。</dd>
<dt>APP_RETRIEVER_SCORETHRESHOLD</dt>
<dd>相关结果的分数阈值。</dd>
</dl>
* APP_RETRIEVER_SCORETHRESHOLD：相关结果的分数阈值。
