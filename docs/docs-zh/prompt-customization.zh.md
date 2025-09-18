<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 自定义提示词

<!-- TOC -->

* [关于提示词文件](#关于提示词文件)
* [访问提示词](#访问提示词)
* [示例：添加数学运算提示词](#示例-添加数学运算提示词

<!-- /TOC -->

## 关于提示词文件

每个示例都使用一个 `prompt.yaml` 文件，定义不同场景下的提示词。
这些提示词引导 RAG 模型生成合适的响应。
你可以根据实际需求定制提示词，以获得理想的模型回复。

## 访问提示词

提示词会作为 Python 字典加载到应用中。
可通过 `utils` 模块的 `get_prompts()` 方法获取完整提示词字典。

假设有如下 `prompt.yaml` 文件：

```yaml
chat_template: |
    你是一个乐于助人、尊重且诚实的助手。
    请始终尽可能有帮助且安全地回答。
    请确保你的回答积极向上。

rag_template: |
    你是名为 Envie 的 AI 助手。
    你只会根据提供的上下文回答问题。
    超出上下文的问题请礼貌拒绝。
```

在 chain server 中可通过如下代码访问 chat_template：

```python3
from RAG.src.chain_server.utils import get_prompts

prompts = get_prompts()

chat_template = prompts.get("chat_template", "")
```

更新提示词后可按如下步骤重启服务：

1. 进入示例目录：

   ```console
   cd RAG/examples/basic_rag/llamaindex
   ```

2. 启动 chain server 微服务：

   ```console
   docker compose down
   docker compose up -d --build
   ```

3. 访问 `http://<ip>:<port>` 进行交互。

## 示例：添加海盗提示词

创建一个让 llm 以“海盗”身份回复的提示词：

1. 在 `prompt.yaml` 添加：

   ```yaml
   pirate_prompt: |
      你是一名海盗，对所有问题都用同样的方式回复。
   ```

2. 在 `chains.py` 的 `llm_chain` 方法中使用 `pirate_prompt` 生成回复：
