from setuptools import setup, find_packages


# 注意：已移除 load_requirements 函数，直接列出核心依赖


# 读取 README.md 作为长描述
def get_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A comprehensive Generative AI development toolkit with RAG, LLM, and multimodal capabilities."

setup(
    name="genai-starter-kit",
    version="0.2.0",  # 版本升级，反映重大依赖清理
    description="🚀 完整的生成式AI开发工具包，支持RAG、LLM和多模态AI功能",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="YY-Nexus",
    author_email="contact@yynexus.com",
    maintainer="YY-Nexus",
    maintainer_email="contact@yynexus.com",
    license="MIT",
    license_files=["LICENSE.md"],
    url="https://github.com/YY-Nexus/GenerativeAI-Starter-Kit",
    download_url="https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/archive/main.zip",
    project_urls={
        "Homepage": "https://github.com/YY-Nexus/GenerativeAI-Starter-Kit",
        "Bug Reports": "https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/issues",
        "Source Code": "https://github.com/YY-Nexus/GenerativeAI-Starter-Kit",
        "Documentation": "https://yy-nexus.github.io/GenerativeAI-Starter-Kit/",
        "中文文档": "https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/blob/main/README.zh.md",
        "Changelog": "https://github.com/YY-Nexus/GenerativeAI-Starter-Kit/blob/main/CHANGELOG.md",
    },
    keywords=[
        "generative-ai",
        "rag",
        "llm",
        "transformers",
        "openai",
        "pytorch",
        "fastapi",
        "machine-learning",
        "artificial-intelligence",
        "multimodal",
        "deep-learning",
    ],
    packages=find_packages(),
    install_requires=[
        # 核心依赖 - 已清理并验证
        "torch>=2.8.0",
        "transformers>=4.56.2",
        "numpy>=2.3.3",
        "fastapi>=0.117.1",
        # 基础工具
        "requests>=2.31.0",
        "pyyaml>=6.0",
        "pillow>=9.0.0",
        # 注意：已移除 langchain 和 sentence-transformers 依赖
    ],
    extras_require={
        "rag": ["chromadb", "milvus"],
        "multimodal": ["transformers", "torch", "opencv-python"],
        "dev": ["black", "flake8", "pre-commit"],
    },
    python_requires=">=3.8",
    classifiers=[
        # 开发状态
        "Development Status :: 4 - Beta",
        
        # 目标受众
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        
        # 主题
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        
        # 许可证
        "License :: OSI Approved :: MIT License",
        
        # Python 版本支持
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # 操作系统
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        
        # 语言支持
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
        
        # 框架
        "Framework :: FastAPI",
        
        # 环境
        "Environment :: Console",
        "Environment :: Web Environment",
    ],
    entry_points={
        "console_scripts": ["sync-docs=RAG.examples.basic_rag.langchain.sync_docs:main"]
    },
    include_package_data=True,
    package_data={"genai_starter_kit": ["configs/*.yaml", "assets/*.png", "docs/*.md"]},
)
