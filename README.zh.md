# GenerativeAIExamples：快速上手与标准化使用指南（中文版）

欢迎使用 GenerativeAIExamples！本项目面向所有层次用户，尤其适合初学者和小白，致力于让生成式AI开发变得简单易懂。

---

## 1. 项目简介

GenerativeAIExamples 是一个涵盖多场景、多模型的生成式AI应用示例库，支持文本、语音、图像等多模态，适合学习、实验和快速开发。

---

## 2. 快速开始

### 环境准备

1. 安装 [Python 3.8+](https://www.python.org/downloads/)
2. 推荐使用 [VS Code](https://code.visualstudio.com/) 编辑器
3. 克隆项目：

   ```sh
   git clone https://github.com/NVIDIA/GenerativeAIExamples.git
   cd GenerativeAIExamples
   ```

### 一键安装依赖

在项目根目录运行：

```sh
find . -name "requirements.txt" -exec pip install -r {} \;
```

---

## 3. 一键启动与批量运行

### 启动API服务

```sh
cd RAG/src/chain_server
pip install -r requirements.txt
python main.py
```

### 批量运行所有notebook

```sh
pip install jupyter nbconvert
find RAG/notebooks -name "*.ipynb" -exec jupyter nbconvert --to notebook --execute --inplace {} \;
```

---

## 4. 目录结构与模块说明

- `docs/`：项目文档与使用说明，含中文文档（docs-zh）
  - `docs-zh/`：所有中文文档，便于本地用户查阅
  - `api_reference/`：API接口详细说明
  - `images/`：文档配图与架构图
- `RAG/`：检索增强生成主模块
  - `examples/`：基础与高级RAG示例，含多轮对话、重排序等
  - `notebooks/`：RAG相关Jupyter Notebook，便于交互式实验
  - `src/`：RAG核心源码，包含API服务、数据处理等
  - `tools/`：辅助工具与脚本
- `community/`：社区贡献与实验性资源，适合学习和扩展
- `finetuning/`：主流大模型微调脚本与流程（如Llama、NeMo等）
- `industries/`：行业应用示例（医疗、金融、安防等）
- `nemo/`、`nemotron/`、`llama_3.3_nemotron_super_49B/`：特定模型或框架相关内容
- `oss_tutorials/`：开源教程与学习笔记
- `vision_workflows/`：视觉AI相关工作流与示例

---

## 5. 核心功能细化

- 端到端RAG示例，支持多种数据源与向量数据库
- 多模态AI场景（文本、语音、图像）与行业专用智能体
- 大模型微调、训练、评估与安全策略（Guardrails）
- 社区资源丰富，支持开源贡献与扩展
- 完善的中英文文档与一键自动化脚本

---

## 6. 典型应用场景

- 智能问答、知识检索、文档分析
- 多模态交互（语音、图像、文本）
- 行业专用智能体（医疗、金融、安防等）
- 大模型微调与安全评估

---

## 7. 常见问题与帮助

- 依赖安装失败？请检查 Python 版本或使用国内镜像源。
- API服务无法启动？请确认端口未被占用，或尝试 `python main.py --help` 查看参数。
- notebook无法批量运行？请确保已安装 Jupyter 和 nbconvert。

更多问题请查阅 `docs/README.md` 或在 Github Issues 提问。

---

## 8. 贡献与反馈

- 欢迎通过 Pull Request 贡献代码、文档或示例
- 发现问题请提交 Issue，描述清楚复现步骤与环境
- 所有贡献请遵守项目 LICENSE 协议

---

## 9. 标准化与易用性承诺

- 所有脚本、文档均采用统一格式，注释清晰，步骤详细
- 目录结构清晰，模块分明，便于查找和扩展
- 提供中英文文档，适配不同用户需求
- 持续完善，欢迎反馈建议

---

> 本项目致力于让每一位用户都能轻松上手、顺利开发，欢迎你加入生成式AI学习与创新社区！
