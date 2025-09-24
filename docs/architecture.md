# 🧠 项目架构说明

## 📦 模块结构

GENERATIVE-AI-STARTER-KIT/
├── genai_starter_kit/          # 核心库模块
│   ├── rag/                    # RAG 组件
│   ├── multimodal/            # 多模态组件
│   └── utils/                 # 工具函数
├── examples/                  # 示例脚本
├── tests/                     # 单元测试
├── scripts/                   # 自动化脚本
├── docs/                      # 文档目录
└── setup.py                   # 构建配置

## 🔗 依赖关系图（建议使用 mermaid）

```mermaid
graph TD
    A[rag.py] --> B[vector_db.py]
    A --> C[retriever.py]
    D[multimodal.py] --> E[image_encoder.py]
    D --> F[text_encoder.py]
    
## 🧩 技术栈

- Python 3.11
- Streamlit / FastAPI
- Docker / GitHub Actions
- PyPI / pre-commit / CodeQL

---
