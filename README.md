# GenerativeAI-Starter-Kit

🚀 **A comprehensive, beginner-friendly Generative AI development toolkit**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![RAG](https://img.shields.io/badge/RAG-✓-brightgreen.svg)](#rag-examples)
[![Multimodal](https://img.shields.io/badge/Multimodal-✓-brightgreen.svg)](#multimodal-applications)
[![Fine-tuning](https://img.shields.io/badge/Fine--tuning-✓-brightgreen.svg)](#model-fine-tuning)

Welcome to GenerativeAI-Starter-Kit! This repository provides everything you need to get started with Generative AI, from basic concepts to production-ready applications. Perfect for learning, rapid prototyping, and real-world deployment.

## 🌟 What's Included

### 🧠 Core AI Examples
- **🔍 RAG (Retrieval-Augmented Generation)**: Build intelligent document Q&A systems
- **🎨 Multimodal Applications**: Work with text, images, and cross-modal tasks
- **🎯 Model Fine-tuning**: Adapt pre-trained models for specific domains
- **🚀 Production-Ready APIs**: FastAPI servers with full documentation

### 🛠️ Development Tools
- **⚡ One-Click Setup**: Automated environment configuration
- **📊 Interactive Notebooks**: Step-by-step Jupyter tutorials
- **🔧 Configuration Management**: Easy YAML-based settings
- **🧪 Testing Framework**: Comprehensive test suites

### 📚 Learning Resources
- **📖 Multi-language Docs**: Complete guides in English and Chinese
- **🎓 Progressive Tutorials**: From beginner to advanced
- **💡 Best Practices**: Industry-standard approaches
- **🔬 Research Examples**: Latest techniques and methods

## 🚀 Quick Start

### 1️⃣ Clone & Setup
```bash
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
./automation/setup.sh
source venv/bin/activate
```

### 2️⃣ Try the Examples
```bash
# RAG System Demo
python examples/rag/simple_rag.py

# Multimodal Web App
python examples/multimodal/image_text_app.py --web

# Fine-tuning Demo
python examples/fine-tuning/text_classification_tuning.py

# Start API Server
python automation/api_server.py
```

### 3️⃣ Explore the Notebooks
```bash
jupyter notebook notebooks/01_rag_introduction.ipynb
```

## 📁 Project Structure

```
GenerativeAI-Starter-Kit/
├── 📚 examples/           # Practical implementations
│   ├── 🔍 rag/           # Document Q&A systems
│   ├── 🎨 multimodal/    # Image-text applications  
│   └── 🎯 fine-tuning/   # Model customization
├── 🤖 automation/        # Setup & deployment scripts
├── ⚙️  configs/          # Configuration files
├── 📖 docs/              # Documentation (EN/中文)
├── 💾 datasets/          # Sample data & generators
├── 📓 notebooks/         # Interactive tutorials
└── 🧪 tests/            # Testing framework
```

## 🎓 Learning Paths

### 🟢 **Beginners**
1. [📖 Read Basic Concepts](docs/en/README.md)
2. [🚀 Follow Quick Start](#quick-start)
3. [📓 Try Interactive Notebooks](notebooks/)
4. [🔍 Build Your First RAG App](examples/rag/)

### 🟡 **Developers** 
1. [🛠️ Explore API Examples](automation/api_server.py)
2. [🎨 Build Multimodal Apps](examples/multimodal/)
3. [⚙️ Customize Configurations](configs/)
4. [🧪 Run Test Suites](tests/)

### 🔴 **Researchers**
1. [🎯 Fine-tune Custom Models](examples/fine-tuning/)
2. [🔬 Study Advanced Techniques](docs/en/advanced/)
3. [💡 Contribute New Examples](#contributing)
4. [📊 Analyze Performance Metrics](notebooks/)

## 💎 Key Features

### 🔍 RAG System
```python
from examples.rag.simple_rag import SimpleRAG

# Initialize RAG system
rag = SimpleRAG()
rag.initialize()

# Add your documents
rag.add_documents(["Your document content..."])

# Ask questions
results = rag.search("What is machine learning?")
response = rag.generate_response("What is machine learning?", results)
```

**Features:**
- ✅ Automatic document chunking and embedding
- ✅ Multiple vector database backends (Chroma, FAISS)
- ✅ Multilingual support (Chinese, English, etc.)
- ✅ Customizable similarity search
- ✅ Context-aware response generation

### 🎨 Multimodal Applications
```python
from examples.multimodal.image_text_app import MultimodalApp

# Initialize multimodal app
app = MultimodalApp()
app.initialize()

# Analyze images
results = app.analyze_image(image, "describe this image")
similarity = app.calculate_similarity(image, "a cat on a table")
```

**Features:**
- ✅ Image captioning with BLIP
- ✅ Text-image similarity with CLIP
- ✅ Interactive web interfaces with Gradio
- ✅ Cross-modal search capabilities
- ✅ Support for multiple image formats

### 🎯 Model Fine-tuning
```python
from examples.fine_tuning.text_classification_tuning import TextClassificationTrainer

# Initialize trainer
trainer = TextClassificationTrainer()
trainer.initialize()

# Train on your data
trainer.train(train_dataset, val_dataset)

# Make predictions
predictions = trainer.predict(["This is amazing!"])
```

**Features:**
- ✅ Text classification fine-tuning
- ✅ Custom dataset support
- ✅ Automatic model evaluation
- ✅ Easy deployment and inference
- ✅ Progress tracking and metrics

## 🌐 API Server

Start a production-ready API server:

```bash
python automation/api_server.py --host 0.0.0.0 --port 8000
```

**Endpoints:**
- `POST /rag/documents` - Add documents to RAG system
- `POST /rag/query` - Query the RAG system  
- `POST /multimodal/analyze` - Analyze images
- `GET /health` - Health check

## 📊 Example Gallery

<table>
<tr>
<td align="center"><strong>🔍 RAG Q&A</strong></td>
<td align="center"><strong>🎨 Image Analysis</strong></td>
</tr>
<tr>
<td>
<pre><code>Query: "What is deep learning?"
Response: "Deep learning is a subset 
of machine learning that uses neural
networks with multiple layers..."</code></pre>
</td>
<td>
<pre><code>Image: cat_photo.jpg
Caption: "A fluffy orange cat sitting
on a wooden table next to a window"
Similarity to "pet animal": 0.89</code></pre>
</td>
</tr>
</table>

## 🔧 Configuration

Customize behavior with YAML configs:

```yaml
# configs/config.yaml
models:
  embedding:
    name: "sentence-transformers/all-MiniLM-L6-v2"
    device: "cpu"  # or "cuda"
    
vector_db:
  type: "chroma"
  collection_name: "my_docs"
  
rag:
  chunk_size: 1000
  top_k: 5
```

## 📖 Documentation

- **🇺🇸 English**: [docs/en/README.md](docs/en/README.md)
- **🇨🇳 中文**: [docs/zh/README.md](docs/zh/README.md)
- **📊 API Docs**: http://localhost:8000/docs (when server running)
- **📓 Notebooks**: [notebooks/](notebooks/)

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md).

```bash
# Development setup
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
./automation/setup.sh
python -m pytest tests/
```

## 📋 Requirements

- **Python**: 3.8+
- **Memory**: 4GB+ (8GB+ recommended)  
- **Storage**: 2GB+ for models
- **GPU**: Optional but recommended for large models

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- 🤗 [Hugging Face](https://huggingface.co/) for transformer models
- 🎨 [OpenAI](https://openai.com/) for CLIP and foundational research
- 🚀 The open-source AI community for inspiration and tools

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/discussions)
- 📧 **Email**: admin@0379.email

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

*Built with ❤️ for the AI community*

</div>
