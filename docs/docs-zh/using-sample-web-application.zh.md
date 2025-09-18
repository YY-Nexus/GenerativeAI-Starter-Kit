<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 使用示例聊天 Web 应用

<!-- TOC -->

* [访问 Web 应用](#访问-web-应用)
* [使用非结构化文档作为知识库](#使用非结构化文档作为知识库)
* [故障排查](#故障排查)

<!-- /TOC -->

## 访问 Web 应用

## 连接到示例 Web 应用：<http://localhost:8090>

  ![示例聊天 Web 应用](images/sample-web-application.png)

## 使用非结构化文档作为知识库

1. 可选：如已配置 NVIDIA Riva，可勾选“启用 TTS 输出”，让 Web 应用朗读答案。

   在下方选择 ASR 语言（如“English (en-US)”）、TTS 语言（如“English (en-US)”）和 TTS 声音，即可体验语音交互。

2. 在“对话”标签输入“Grace 超级芯片有多少核心？”并点击“提交”。

   或点击文本框右侧麦克风按钮，语音提问。

   ![Grace 查询失败](../RAG/notebooks/langchain/data/imgs/grace_noanswer_with_riva.png)

3. 上传示例数据到知识库。

   点击“知识库”标签，再点击“添加文件”。

   找到 `notebooks` 目录下的 `dataset.zip`，解压后上传 PDF。

4. 如需删除知识库文件，在“知识库”标签选择文件名并点击“删除”。

5. 回到“对话”标签，勾选“使用知识库”。

6. 重新输入问题：“Grace 超级芯片有多少核心？”

   ![Grace 查询成功](../RAG/notebooks/langchain/data/imgs/grace_answer_with_riva.png)

   ```{tip}
   默认提示词针对 Llama 聊天模型优化。
   如使用补全模型，需微调提示词。
   ```

## 故障排查

如首次语音查询出现“无法访问媒体设备”错误，请按如下步骤操作：

![媒体设备访问错误窗口](images/media-device-access-error.png)

1. 新开浏览器标签页，输入 `chrome://flags`。

2. 搜索“insecure origins treated as secure”。

   ![浏览器访问 chrome://flags](images/chrome-flags-fix-media-device-access-error.png)

3. 在文本框输入 `http://<host-ip>:8090`，选择“Enabled”。

4. 点击“Relaunch”。

5. 浏览器重启后，授权 `http://host-ip:8090` 访问麦克风。

6. 重试语音请求。
