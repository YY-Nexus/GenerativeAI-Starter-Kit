# 生成式AI入门工具包 - 中文文档

🚀 **面向初学者和开发者的全面生成式AI开发工具包**

欢迎使用生成式AI入门工具包！本仓库提供了从基础概念到高级实现的一切所需内容，帮助您快速上手生成式AI开发。

## 🎯 包含内容

### 📚 核心示例
- **RAG（检索增强生成）**: 构建智能文档搜索和问答系统
- **多模态应用**: 处理文本、图像等多种模态数据
- **模型微调**: 将预训练模型适配到特定需求

### 🛠️ 工具与自动化
- **一键安装脚本**: 几分钟内完成环境搭建
- **配置管理**: 易于使用的YAML配置文件
- **测试框架**: 验证您的实现效果

### 📖 学习资源
- **循序渐进的教程**: 从入门到进阶
- **代码示例**: 详细注释的可运行代码
- **最佳实践**: 行业标准方法

## 🚀 快速开始

### 环境要求
- Python 3.8 或更高版本
- Git
- 4GB+ 内存（推荐8GB+）
- GPU支持（可选但推荐）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
```

2. **运行安装脚本**
```bash
./automation/setup.sh
```

3. **激活环境**
```bash
source venv/bin/activate
```

4. **测试安装**
```bash
python examples/rag/simple_rag.py
```

## 📁 项目结构

```
GenerativeAI-Starter-Kit/
├── examples/                  # 实用示例
│   ├── rag/                  # RAG实现
│   ├── multimodal/           # 图文应用
│   └── fine-tuning/          # 模型微调
├── automation/               # 安装和部署脚本
├── configs/                  # 配置文件
├── docs/                     # 文档
│   ├── en/                   # 英文文档
│   └── zh/                   # 中文文档
├── datasets/                 # 示例数据集
├── notebooks/                # Jupyter笔记本
└── tests/                    # 测试框架
```

## 🎓 学习路径

### 初学者
1. 从[基础概念](./concepts.md)开始
2. 跟随[RAG教程](./tutorials/rag-tutorial.md)
3. 尝试[多模态示例](./tutorials/multimodal-tutorial.md)

### 开发者
1. 探索[高级示例](./advanced/)
2. 查看[API文档](./api/)
3. 参考[最佳实践](./best-practices.md)

### 研究人员
1. 学习[微调技术](./research/fine-tuning.md)
2. 实验[自定义模型](./research/custom-models.md)
3. 参与[研究项目](./research/projects.md)

## 🌟 核心功能

### RAG系统
- **文档处理**: 自动分块和向量化
- **向量搜索**: 支持多种后端的快速相似性搜索
- **回答生成**: 基于上下文的智能回答生成
- **多语言支持**: 支持中文、英文等多种语言

### 多模态应用
- **图像理解**: 分析和描述图像内容
- **文本生图**: 根据描述生成图像
- **跨模态搜索**: 使用文本查询找到相关图像
- **交互式界面**: 用户友好的Gradio网页界面

### 模型微调
- **文本分类**: 情感分析、主题分类
- **命名实体识别**: 从文本中提取实体
- **问答系统**: 构建自定义问答系统
- **自定义任务**: 适配您的特定用例

## 🔧 配置说明

系统使用YAML配置文件便于自定义：

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

## 🚀 部署选项

### 本地开发
```bash
# 使用CPU运行
python examples/rag/simple_rag.py

# 使用GPU运行
CUDA_VISIBLE_DEVICES=0 python examples/rag/simple_rag.py
```

### 网页应用
```bash
# 启动多模态网页应用
python examples/multimodal/image_text_app.py --web

# 启动RAG API服务器
python automation/api_server.py
```

### Docker部署
```bash
# 构建容器
docker build -t generative-ai-kit .

# 运行容器
docker run -p 8000:8000 generative-ai-kit
```

## 📊 示例展示

### RAG系统
```python
from examples.rag.simple_rag import SimpleRAG

# 初始化RAG系统
rag = SimpleRAG()
rag.initialize()

# 添加文档
documents = ["您的文档内容..."]
rag.add_documents(documents)

# 查询
results = rag.search("什么是机器学习？")
response = rag.generate_response("什么是机器学习？", results)
print(response)
```

### 多模态分析
```python
from examples.multimodal.image_text_app import MultimodalApp

# 初始化应用
app = MultimodalApp()
app.initialize()

# 分析图像
image = app.load_image("图像路径.jpg")
results = app.analyze_image(image, "描述这张图片")
print(results['caption'])
```

### 模型微调
```python
from examples.fine_tuning.text_classification_tuning import TextClassificationTrainer

# 初始化训练器
trainer = TextClassificationTrainer()
trainer.initialize()

# 准备数据并训练
train_dataset, val_dataset = trainer.prepare_data(texts, labels)
trainer.train(train_dataset, val_dataset)

# 进行预测
predictions = trainer.predict(["这太棒了！"])
```

## 🤝 贡献指南

我们欢迎贡献！请查看我们的[贡献指南](../CONTRIBUTING.md)了解详情。

### 开发环境设置
```bash
# 克隆并设置开发环境
git clone https://github.com/YY-Nexus/GenerativeAI-Starter-Kit.git
cd GenerativeAI-Starter-Kit
./automation/setup.sh

# 运行测试
python -m pytest tests/

# 代码格式化
black .
flake8 .
```

## 📝 开源协议

本项目采用MIT协议 - 详见[LICENSE](../LICENSE)文件。

## 🆘 技术支持

- 📖 **文档**: [docs/](./README.md)
- 🐛 **问题反馈**: [GitHub Issues](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/issues)
- 💬 **讨论**: [GitHub Discussions](https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/discussions)
- 📧 **邮箱**: [support@example.com](mailto:support@example.com)

## 🙏 致谢

- Hugging Face 提供的优秀transformer模型
- OpenAI 的CLIP等基础性工作
- 开源AI社区的灵感和工具支持

## 📚 推荐学习资源

### 中文资源
- [生成式AI基础教程](./tutorials/basics-zh.md)
- [RAG系统详解](./tutorials/rag-detailed-zh.md)
- [多模态AI应用开发](./tutorials/multimodal-zh.md)
- [模型微调实战](./tutorials/fine-tuning-zh.md)

### 视频教程
- [B站教程合集](https://space.bilibili.com/example)
- [YouTube频道](https://youtube.com/channel/example)

### 社区交流
- QQ群：123456789
- 微信群：扫描二维码加入
- 知乎专栏：[生成式AI实战](https://zhuanlan.zhihu.com/example)

---

**祝您学习愉快！🚀**
