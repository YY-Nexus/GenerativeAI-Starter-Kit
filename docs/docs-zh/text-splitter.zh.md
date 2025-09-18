<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 文本分割器自定义
<!-- TOC -->

* [更新模型名称](#更新模型名称)
* [调整分块大小与重叠](#调整分块大小与重叠)
* [自定义文本分割器](#自定义文本分割器)
* [构建并启动容器](#构建并启动容器)

<!-- /TOC -->

## 更新模型名称

默认文本分割器为 `SentenceTransformersTokenTextSplitter`。
分割器使用 Hugging Face 预训练模型识别句子边界。
可在 `chain-server` 服务的 `docker-compose.yaml` 文件中通过环境变量 `APP_TEXTSPLITTER_MODELNAME` 更改模型，例如：

```yaml
services:
  chain-server:
    environment:
      APP_TEXTSPLITTER_MODELNAME: intfloat/e5-large-v2
```

## 调整分块大小与重叠

分割器将文档拆分为更小块。
可通过如下环境变量控制分块大小与重叠：

-`APP_TEXTSPLITTER_CHUNKSIZE`：每块最大 token 数。
-`APP_TEXTSPLITTER_CHUNKOVERLAP`：相邻块之间重叠 token 数。

```yaml
services:
  chain-server:
    environment:
      APP_TEXTSPLITTER_CHUNKSIZE: 256
      APP_TEXTSPLITTER_CHUNKOVERLAP: 128
```

## 自定义文本分割器

默认分割器效果良好，但可按需自定义。

1. 修改 `RAG/src/chain_server/utils.py` 的 `get_text_splitter` 方法，集成自定义分割器类。

   ```python
   def get_text_splitter():

      from langchain.text_splitter import RecursiveCharacterTextSplitter

      return RecursiveCharacterTextSplitter(
          chunk_size=get_config().text_splitter.chunk_size - 2,
          chunk_overlap=get_config().text_splitter.chunk_overlap
      )
   ```

   请确保分块 token 数小于嵌入模型上下文长度。

## 构建并启动容器

修改分割器后，按如下步骤构建并启动容器：

1. 进入示例目录。

   ```console
   cd RAG/examples/basic_rag/llamaindex
   ```

2. 构建并部署微服务。

   ```console
   docker compose up -d --build
   ```
