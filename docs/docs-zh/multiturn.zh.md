<!--
  SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 支持多轮对话

RAG API 由 Chain Server 提供，兼容 OpenAI。
更多信息可参考 [openapi_schema](./api_reference/openapi_schema.json)。

Chain Server 的 `/generate` API 端点可根据请求生成响应。
如需支持多轮对话，请在请求体中包含完整的消息序列。

## 参数说明

### messages（消息对象数组，必填）

说明：包含当前对话历史的消息列表。每条消息需包含角色和内容。

* role（字符串，必填）：消息角色，如 `user`、`assistant` 或 `system`。
* content（字符串，必填）：消息内容。

* use_knowledge_base（布尔值，必填）

说明：是否使用知识库。

默认值：False

### 多轮对话示例请求

```json
{
    "messages": [
        {
            "role": "system",
            "content": "你是一个提供 FastAPI 信息的助手。"
        },
        {
            "role": "user",
            "content": "什么是 FastAPI？"
        },
        {
            "role": "assistant",
            "content": "FastAPI 是一个基于 Python 3.6+ 类型提示的现代高性能 Web API 框架。"
        },
        {
            "role": "user",
            "content": "FastAPI 的主要特性有哪些？"
        }
    ],
    "use_knowledge_base": true
}
```

上述示例配置说明：

-system 消息设定助手上下文。
-user 和 assistant 消息构成对话历史。
-最后一个 user 消息继续提问 FastAPI 的主要特性。
