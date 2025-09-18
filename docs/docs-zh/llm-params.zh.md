<!--
  SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 运行时自定义 LLM 参数

RAG API 由 Chain Server 提供，兼容 OpenAI。
更多信息可参考 [openapi_schema](./api_reference/openapi_schema.json)。

Chain Server 的 `/generate` API 端点可根据请求生成响应。
你可以在请求体中动态指定多种参数，定制语言模型（LLM）行为。

可在请求体中包含如下参数：

## 参数说明

### temperature（数字，可选）

说明：控制生成文本的随机性。值越高，输出越随机；值越低，输出越确定。

范围：`0.1` 到 `1`

默认值：`0.2`

### top_p（数字，可选）

说明：定义采样时累计概率阈值。top-p 值决定采样时考虑的最可能 token。

范围：`0.1` 到 `1`

默认值：`0.7`

### max_tokens（整数，可选）

说明：限制生成响应的最大 token 数。

默认值：`1024`

### stop（字符串数组，可选）

说明：API 在遇到 stop 序列时停止生成。返回文本不包含 stop 序列。

默认值：[]

## 运行时 LLM 配置示例请求

```json
{
    "messages": [
        {
            "role": "user",
            "content": "请解释 FastAPI 的主要特性。"
        }
    ],
    "use_knowledge_base": true,
    "temperature": 0.3,
    "top_p": 0.8,
    "max_tokens": 150,
    "stop": ["\n"]
}
```

上述示例配置说明：

- temperature: 0.3（适度随机性）
- top_p: 0.8（采样累计概率至 0.8）
- max_tokens: 150（响应长度限制为 150 token）
- stop: ["\n"]（遇到换行符停止生成）
