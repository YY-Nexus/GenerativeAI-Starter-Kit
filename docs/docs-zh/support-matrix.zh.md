<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 支持矩阵

## GPU 要求

大语言模型对 GPU 资源要求极高。
所有 LLM 都以参数数量（数十亿）衡量。
本示例聚焦于 Meta 的 Llama 3 Instruct 模型，分为 8B 和 70B 两种规模。

|        聊天模型         | GPU 显存需求 |
| ----------------------- | ------------ |
| Meta Llama 3 8B Instruct  | 30 GB        |
| Meta Llama 3 70B Instruct | 320 GB       |

可通过多块 GPU 提供所需资源。

检索增强需用到嵌入模型，将文本序列转为向量。

| 默认嵌入模型           | GPU 显存需求 |
| ---------------------- | ------------ |
| Snowflake Arctic-Embed-L | 2 GB        |

如需重排序，重排序模型可提升检索相关性。

| 默认重排序模型         | GPU 显存需求 |
| ---------------------- | ------------ |
| NV-RerankQA-Mistral4B-v3 | 9 GB        |

更多模型显存需求请参考：

- NVIDIA NIM for LLMs [支持矩阵](https://docs.nvidia.com/nim/large-language-models/latest/support-matrix.html)
- NVIDIA Text Embedding NIM [支持矩阵](https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/support-matrix.html)
- NVIDIA Text Reranking NIM [支持矩阵](https://docs.nvidia.com/nim/nemo-retriever/text-reranking/latest/support-matrix.html)

Milvus 数据库建议额外预留 4GB GPU 显存。

## CPU 与内存要求

开发建议至少 10 核 CPU 和 64 GB 内存。

## 存储要求

RAG 主要存储需求为模型权重和向量数据库文档。
模型文件大小随参数数量变化：

|          模型           | 磁盘存储 |
| ---------------------- | -------- |
| Llama 3 8B Instruct    | 30 GB    |
| Llama 3 70B Instruct   | 140 GB   |
| Snowflake Arctic-Embed-L | 17 GB  |
| NV-RerankQA-Mistral4B-v3 | 23 GB  |

向量数据库空间随上传文档数量变化，开发建议 10 GB。

Docker 镜像建议预留约 60 GB。
