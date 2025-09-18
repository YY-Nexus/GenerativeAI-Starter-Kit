<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 可选：启用 NVIDIA Riva ASR 与 TTS

<!-- TOC -->

* [RAG Playground 集成](#rag-playground-集成)
* [本地 Riva 服务器](#本地-riva-服务器)
* [托管 Riva API 端点](#托管-riva-api-端点
* [启动 RAG 示例](#启动-rag-示例
* [后续步骤](#后续步骤

<!-- /TOC -->

## RAG Playground 集成

按如下步骤可用语音提交查询，RAG Playground 可朗读 LLM 响应。

## 本地 Riva 服务器

本地启动 Riva 服务器请参考 [Riva 快速入门指南](https://docs.nvidia.com/deeplearning/riva/user-guide/docs/quick-start-guide.html)。

-在 `config.sh` 脚本中设置：

-`service_enabled_asr=true` 和 `service_enabled_tts=true`
-通过 `asr_language_code` 和 `tts_language_code` 设置 ASR 与 TTS 语言。
-`models_tts` 变量需包含如 `rmir_tts_radtts_hifigan_${modified_lang_code}_ipa` 的 Rad-TTS 模型。

## NVIDIA API Catalog 托管 Riva API 端点

可通过 [NVIDIA API Catalog](https://build.nvidia.com/explore/speech) 访问多种 GPU 加速语音模型，无需本地部署。
需获取 API 密钥，参考[获取方法](common-prerequisites.md#get-an-api-key-for-the-accessing-models-on-the-api-catalog)。

## 启动 RAG 示例

获得 Riva 服务器访问后，按如下步骤启动支持语音的 RAG 示例：

1. 在终端导出 `PLAYGROUND_MODE` 环境变量：

   ```console
   export PLAYGROUND_MODE=speech
   ```

2. 编辑示例的 `docker-compose.yaml`，在 `rag-playground` 服务添加如下环境变量：

   * 使用 API Catalog 托管语音模型：

     ```yaml
     rag-playgound:
       ...
       environment:
         RIVA_API_URI: grpc.nvcf.nvidia.com:443
         NVIDIA_API_KEY: ${NVIDIA_API_KEY}
         RIVA_ASR_FUNCTION_ID: 1598d209-5e27-4d3c-8079-4751568b1081 # nvidia/parakeet-ctc-riva-1-1b
         RIVA_TTS_FUNCTION_ID: 5e607c81-7aa6-44ce-a11d-9e08f0a3fe49 # nvidia/radtts-hifigan-riva
         TTS_SAMPLE_RATE: 48000
     ```

     获取 API 密钥和 function ID：进入语音模型页面，点击 **Try API**，再点击 **Get API Key** 生成密钥，参考 **Run python client** 获取 function-id。

   * 使用本地 RIVA 模型：

     ```yaml
     rag-playgound:
       ...
       environment:
         RIVA_API_URI: <riva-ip-address>:50051
         TTS_SAMPLE_RATE: 48000
     ```

   * `RIVA_API_URI` 为 Riva IP 地址或主机名及端口。
   * `NVIDIA_API_KEY` 为 API Catalog 托管 Riva API 的密钥。
   * `RIVA_ASR_FUNCTION_ID` 为托管 ASR 的 Riva Function ID。
   * `RIVA_TTS_FUNCTION_ID` 为托管 TTS 的 Riva Function ID。
