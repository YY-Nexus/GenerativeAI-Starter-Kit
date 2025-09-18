<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# RAG Playground Web 应用

<!-- TOC -->

* [关于 Web 应用](#关于-web-应用)
* [Web 应用设计](#web-应用设计)
* [单独运行 Web 应用](#单独运行-web-应用)

<!-- /TOC -->

## 关于 Web 应用

该 Web 应用为 RAG [chain server](./chain-server.md) API 提供用户界面。

-可与 LLM 聊天，查看不同示例的流式响应。
-选择“使用知识库”后，聊天机器人会返回结合你上传并存储在向量数据库--中的文档数据增强的答案。
-上传文档请点击右上角“知识库”并上传文件。

![示意图](images/image4.jpg)

## Web 应用设计

应用核心为 Python 编写的 FastAPI 服务器。该服务器托管两个 [Gradio](https://www.gradio.app/) 应用，一个用于模型对话，一个用于文档上传。Gradio 页面嵌入在由 NVIDIA Kaizen UI React+Next.js 框架创建的静态框架中，并编译为静态页面。通过 iframe 挂载 Gradio 应用。

## 单独运行 Web 应用

开发时可按如下命令运行：

## 构建容器

  ```console
  docker compose build rag-playground
  ```

## 启动容器

  ```console
  docker compose up rag-playground
  ```

## 在浏览器打开 ``http://host-ip:8090``

如上传多个 PDF，Web 应用显示的预计完成时间可能不准确。
