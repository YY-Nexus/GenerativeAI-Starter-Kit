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

- Pull Requests welcome for code, docs, or examples
- Report issues with clear steps and environment details
- All contributions must comply with the LICENSE

---

## 9. Standardization & Usability Commitment

- All scripts and docs use unified format, clear comments, and step-by-step instructions
- Clear directory structure, modular organization for easy navigation and extension
- Chinese and English documentation for global accessibility
- Continuous improvement—feedback is welcome!

---

> This project is committed to making generative AI development easy for everyone. Join our community and start building today!
>>>>>>> daf1912 (Initial commit: GenerativeAI-Starter-Kit project structure and docs)
