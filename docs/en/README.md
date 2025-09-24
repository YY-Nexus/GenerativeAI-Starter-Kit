# GenerativeAI Starter Kit - English Documentation

🚀 **A comprehensive, beginner-friendly toolkit for Generative AI development**

Welcome to the GenerativeAI Starter Kit! This repository provides everything you need to get started with Generative AI, from basic concepts to advanced implementations.

## 🎯 What's Included

### 📚 Core Examples
- **RAG (Retrieval-Augmented Generation)**: Build intelligent document search and Q&A systems
- **Multimodal Applications**: Work with text, images, and other modalities
- **Model Fine-tuning**: Adapt pre-trained models for your specific needs

### 🛠️ Tools & Automation
- **One-click Setup Scripts**: Get started in minutes
- **Configuration Management**: Easy-to-use YAML configurations
- **Testing Framework**: Validate your implementations

### 📖 Learning Resources
- **Step-by-step Tutorials**: From beginner to advanced
- **Code Examples**: Well-documented, runnable code
- **Best Practices**: Industry-standard approaches

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- 4GB+ RAM (8GB+ recommended)
- GPU support optional but recommended

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
```

2. **Run the setup script**
```bash
./automation/setup.sh
```

3. **Activate the environment**
```bash
source venv/bin/activate
```

4. **Test the installation**
```bash
python examples/rag/simple_rag.py
```

## 📁 Project Structure

```
GenerativeAI-Starter-Kit/
├── examples/                  # Practical examples
│   ├── rag/                  # RAG implementations
│   ├── multimodal/           # Image-text applications
│   └── fine-tuning/          # Model fine-tuning
├── automation/               # Setup and deployment scripts
├── configs/                  # Configuration files
├── docs/                     # Documentation
│   ├── en/                   # English docs
│   └── zh/                   # Chinese docs
├── datasets/                 # Sample datasets
├── notebooks/                # Jupyter notebooks
└── tests/                    # Testing framework
```

## 🎓 Learning Path

### For Beginners
1. Start with [Basic Concepts](./concepts.md)
2. Follow the [RAG Tutorial](./tutorials/rag-tutorial.md)
3. Try the [Multimodal Example](./tutorials/multimodal-tutorial.md)

### For Developers
1. Explore [Advanced Examples](./advanced/)
2. Check [API Documentation](./api/)
3. Review [Best Practices](./best-practices.md)

### For Researchers
1. Study [Fine-tuning Techniques](./research/fine-tuning.md)
2. Experiment with [Custom Models](./research/custom-models.md)
3. Contribute to [Research Projects](./research/projects.md)

## 🌟 Key Features

### RAG System
- **Document Processing**: Automatic chunking and embedding
- **Vector Search**: Fast similarity search with multiple backends
- **Response Generation**: Context-aware answer generation
- **Multilingual Support**: Works with multiple languages

### Multimodal Applications
- **Image Understanding**: Analyze and describe images
- **Text-to-Image**: Generate images from descriptions
- **Cross-modal Search**: Find images using text queries
- **Interactive Web Interface**: User-friendly Gradio interfaces

### Model Fine-tuning
- **Text Classification**: Sentiment analysis, topic classification
- **Named Entity Recognition**: Extract entities from text
- **Question Answering**: Build custom Q&A systems
- **Custom Tasks**: Adapt for your specific use cases

## 🔧 Configuration

The system uses YAML configuration files for easy customization:

```yaml
# configs/config.yaml
models:
  embedding:
    name: "sentence-transformers/all-MiniLM-L6-v2"
    device: "cpu"

vector_db:
  type: "chroma"
  collection_name: "my_documents"

rag:
  chunk_size: 1000
  top_k: 5
```

## 🚀 Deployment Options

### Local Development
```bash
# Run with CPU
python examples/rag/simple_rag.py

# Run with GPU
CUDA_VISIBLE_DEVICES=0 python examples/rag/simple_rag.py
```

### Web Applications
```bash
# Start multimodal web app
python examples/multimodal/image_text_app.py --web

# Start RAG API server
python automation/api_server.py
```

### Docker Deployment
```bash
# Build container
docker build -t generative-ai-kit .

# Run container
docker run -p 8000:8000 generative-ai-kit
```

## 📊 Examples Gallery

### RAG System
```python
from examples.rag.simple_rag import SimpleRAG

# Initialize RAG system
rag = SimpleRAG()
rag.initialize()

# Add documents
documents = ["Your document content here..."]
rag.add_documents(documents)

# Query
results = rag.search("What is machine learning?")
response = rag.generate_response("What is machine learning?", results)
print(response)
```

### Multimodal Analysis
```python
from examples.multimodal.image_text_app import MultimodalApp

# Initialize app
app = MultimodalApp()
app.initialize()

# Analyze image
image = app.load_image("path/to/image.jpg")
results = app.analyze_image(image, "describe this image")
print(results['caption'])
```

### Model Fine-tuning
```python
from examples.fine_tuning.text_classification_tuning import TextClassificationTrainer

# Initialize trainer
trainer = TextClassificationTrainer()
trainer.initialize()

# Prepare data and train
train_dataset, val_dataset = trainer.prepare_data(texts, labels)
trainer.train(train_dataset, val_dataset)

# Make predictions
predictions = trainer.predict(["This is amazing!"])
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
./automation/setup.sh

# Run tests
python -m pytest tests/

# Code formatting
black .
flake8 .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: [docs/](./README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/discussions)
- 📧 **Email**: [support@example.com](mailto:support@example.com)

## 🙏 Acknowledgments

- Hugging Face for amazing transformer models
- OpenAI for CLIP and other foundational work
- The open-source AI community for inspiration and tools

---

**Happy coding! 🚀**
