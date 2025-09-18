<!--
  SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# Chain Server 自定义

<!-- TOC -->

* [关于 Chain Server](#关于-chain-server)
* [独立运行 Chain Server](#独立运行-chain-server)
* [支持更多文档文件类型](#支持更多文档文件类型)
* [Chain Server REST API 参考](#chain-server-rest-api-参考

<!-- /TOC -->

## 关于 Chain Server

Chain Server 以 FastAPI 为基础实现，便于体验问答聊天机器人。
该服务器封装了对不同组件的调用，并编排所有生成式 AI 示例的整体流程。

## 独立运行 Chain Server

开发时可按如下命令运行服务器：

1. 从源码构建容器：

   ```console
   cd RAG/examples/advanced_rag/multi_turn_rag
   docker compose build chain-server
   ```

2. 启动容器（即启动服务器）：

   ```console
   docker compose up -d chain-server
   ```

3. 在浏览器中打开 <http://host-ip:8081/docs> 查看 REST API 并尝试相关接口。

## 支持更多文档文件类型

大多数示例支持读取文本、Markdown 和 PDF 文件。
[多模态示例](../RAG/examples/advanced_rag/multimodal_rag/) 支持 PDF、PPT 和 PNG 文件。

以下为添加 Jupyter Notebook 支持的简单示例：

1. 可选：编辑 `RAG/src/chain-server/requirements.txt`，添加文档加载器包。
   本例已包含 `langchain_community`，无需修改。

2. 编辑 `RAG/examples/basic_rag/langchain/chains.py`，如下：

* 导入 notebook 文档加载器：

     ```python
     from langchain_community.document_loaders import NotebookLoader
     ```

 *更新 `ingest_docs` 方法，示例：

```python

     if not filename.endswith((".txt", ".pdf", ".md", ".ipynb")):
         raise ValueError(f"{filename} 不是有效的文本、PDF、Markdown 或 Jupyter Notebook 文件")
     try:
         _path = filepath
         if filename.endswith(".ipynb"):
             raw_documents = NotebookLoader(_path, include_outputs=True).load()
         else:
             raw_documents = UnstructuredFileLoader(_path).load()
     ```

1. 构建并启动容器：

   ```console
   docker compose up -d --build
   ```
