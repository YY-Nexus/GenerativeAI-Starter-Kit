# GenerativeAIExamples: Quick Start & Standardized Guide

Welcome to GenerativeAIExamples! This project is designed for all levels of users, especially beginners, making generative AI development simple and accessible.

---

## 1. Project Overview

GenerativeAIExamples is a multi-scenario, multi-model generative AI application library. It supports text, speech, image, and more, suitable for learning, experimentation, and rapid development.

---

## 2. Quick Start

### Environment Setup

1. Install [Python 3.8+](https://www.python.org/downloads/)
2. Recommended: [VS Code](https://code.visualstudio.com/) editor
3. Clone the project:

   ```sh
   git clone https://github.com/NVIDIA/GenerativeAIExamples.git
   cd GenerativeAIExamples
   ```

### Install All Dependencies

Run in the project root:

```sh
find . -name "requirements.txt" -exec pip install -r {} \;
```

---

## 3. One-Click Launch & Batch Notebook Execution

### Start API Service

```sh
cd RAG/src/chain_server
pip install -r requirements.txt
python main.py
```

### Batch Run All Notebooks

```sh
pip install jupyter nbconvert
find RAG/notebooks -name "*.ipynb" -exec jupyter nbconvert --to notebook --execute --inplace {} \;
```

---

## 4. Directory Structure

- `docs/`: Documentation and usage guides (with Chinese docs in docs-zh)
- `RAG/`: Retrieval Augmented Generation main module (examples, source, tools)
- `community/`: Community contributions and experimental resources
- `finetuning/`, `nemo/`, `llama_3.3_nemotron_super_49B/`: Model fine-tuning and framework content
- See "Project Architecture Overview" for details

---

## 5. Core Features

- End-to-end RAG examples (basic & advanced)
- Multi-modal and industry-specific AI agents (text, speech, image, healthcare, finance, security)
- Model fine-tuning, training, evaluation, and safety (Llama, NeMo, Nemotron)
- Community resources, open-source contributions, and tutorials
- Comprehensive documentation (Chinese & English), one-click scripts, batch notebook execution

---

## 6. Typical Use Cases

- Intelligent Q&A, knowledge retrieval, document analysis
- Multi-modal interaction (speech, image, text)
- Industry-specific agents (healthcare, finance, security)
- Large model fine-tuning and safety evaluation

---

## 7. FAQ & Help

- Dependency install failed? Check Python version or use a local mirror.
- API service won't start? Check port usage or run `python main.py --help` for options.
- Notebooks won't batch run? Ensure Jupyter and nbconvert are installed.

See `docs/README.md` or open a Github Issue for more help.

---

## 8. Contributing & Feedback

## 9. Standardization & Usability Commitment

> This project is committed to making generative AI development easy for everyone. Join our community and start building today!

## 10. 文档同步链（DocumentSyncChain）使用指南

DocumentSyncChain 支持文档唯一性校验、向量数据库存储、MySQL元数据写入、LLM智能摘要。

### CLI 批量同步示例

```sh
python RAG/examples/basic_rag/langchain/sync_docs.py --file your_file.txt --collection doc_vectors --mysql_host 127.0.0.1 --mysql_user root --mysql_password yourpass --mysql_db yyc3_GenerativeAI
```

### FastAPI 接口示例

启动服务：

上传文档：

```sh
curl -F "file=@your_file.txt" http://localhost:8000/sync_doc/
```

### pytest 单元测试

```sh
pytest RAG/examples/basic_rag/langchain/test_chains.py
```

### 代码集成示例

```python
from chains import DocumentSyncChain, ingest_docs
vector_db_config = {"collection_name": "doc_vectors"}
mysql_config = {"host": "127.0.0.1", "user": "root", "password": "yourpass", "database": "yyc3_GenerativeAI"}
chain = DocumentSyncChain(vector_db_config, mysql_config)
docs = ingest_docs("your_file.txt")
chain.process_and_store(docs)
```

更多高级用法见 chains.py 注释。

---

## 11. 自动化交付与集成

### PyPI 包发布

- 包名：`genai-starter-kit`
- 安装：

   ```sh
   pip install genai-starter-kit
   ```

- [PyPI 包主页](https://pypi.org/project/genai-starter-kit/)

### Docker 镜像发布

- 镜像名：`yanyuit/genai-starter-kit`
- 拉取与运行：

   ```sh
   docker pull yanyuit/genai-starter-kit:latest
   docker run -p 8000:8000 yanyuit/genai-starter-kit:latest
   ```

- [DockerHub 镜像主页](https://hub.docker.com/r/yanyuit/genai-starter-kit)

### CI/CD 自动化

- 推送代码到 main 分支，自动完成测试、构建、PyPI/Docker 发布、文档同步。

- 相关脚本见 `.github/workflows/ci-cd.yml`，支持多版本测试、代码检查、安全扫描、文档自动发布。

---
> This project is committed to making generative AI development easy for everyone. Join our community and start building today!
