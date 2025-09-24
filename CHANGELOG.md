# 📜 CHANGELOG

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-09-25

### 🎉 Initial Release

- Published `genai-starter-kit` to [PyPI](https://pypi.org/project/genai-starter-kit/)
- Added core modules:
  - RAG examples (`simple_rag.py`, `rag_pipeline.py`)
  - Multimodal demo (`image_text_app.py`)
  - Fine-tuning pipeline (`text_classification_tuning.py`)
- Included FastAPI server (`api_server.py`) with OpenAPI docs
- One-click setup script (`automation/setup.sh`)
- Batch notebook execution support
- Multi-language documentation (`docs/`, `docs-zh/`)
- GitHub Actions workflows:
  - `ci-cd.yml` for build and deploy
  - `codeql.yml` for security scanning
  - `dependabot.yml` for dependency updates

---

## [Unreleased]

### 🚧 Upcoming Features

- Add Hugging Face model integration
- Support for LangChain agents and tools
- Docker image auto-publish via GitHub Actions
- Systemd deployment templates for TANS nodes
- Mermaid architecture diagrams in README
- PyPI extras support (`pip install genai-starter-kit[rag]`)

---

