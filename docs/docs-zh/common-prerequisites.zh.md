<!--
  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->

# 先决条件

1. 使用 Git LFS 克隆 Generative AI 示例仓库：

    ```console
    sudo apt -y install git-lfs
    git clone git@github.com:NVIDIA/GenerativeAIExamples.git
    cd GenerativeAIExamples/
    git lfs pull
    ```

2. 安装 Docker Engine。Ubuntu 安装参考 [官方文档](https://docs.docker.com/engine/install/ubuntu/)。

3. 安装 Docker Compose。参考 [Compose 插件安装](https://docs.docker.com/compose/install/linux/)。

    a. 确保 Docker Compose 插件版本为 2.20 或更高。

    b. 安装后运行 `docker compose version` 确认。

4. 可选：如需 GPU 加速容器（如 Milvus、NVIDIA NIM for LLMs），请[安装](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) NVIDIA Container Toolkit。

5. 获取 API Catalog 模型访问密钥。可用同一密钥访问不同模型 API 端点。

    a. 访问 [https://build.nvidia.com/explore/discover](https://build.nvidia.com/explore/discover)。

    b. 找到 **Llama 3.1 70B Instruct** 卡片并点击。

    ![Llama 3 70B Instruct model card](images/llama3-70b-instruct-model-card.png)

    c. 点击 **Get API Key**。

    ![API section of the model page.](images/llama3-70b-instruct-get-api-key.png)

    d. 点击 **Generate Key**。

    ![Generate key window.](images/api-catalog-generate-api-key.png)

    e. 点击 **Copy Key** 并保存 API 密钥。密钥以 ``nvapi-`` 开头。

    ![Key Generated window.](images/key-generated.png)

6. 获取 NGC 许可证。方法如下：

    a. 可申请 [90 天试用](https://enterpriseproductregistration.nvidia.com/?LicType=EVAL&ProductFamily=NVAIEnterprise)。详情见 [NVIDIA AI Enterprise 介绍](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/)。

    b. 注册 [NVIDIA Developer Program](https://developer.nvidia.com/login)。详情见 [开发者计划介绍](https://developer.nvidia.com/developer-program)。

7. 获取 NVIDIA NGC API 密钥。用于登录 NVIDIA 容器注册中心 nvcr.io 并拉取安全基础镜像。参考[官方文档](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key)生成密钥。

    a. 获取密钥后可运行 `docker login nvcr.io` 验证有效性。
