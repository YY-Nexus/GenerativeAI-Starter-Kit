from setuptools import setup, find_packages
import os


def load_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="genai-starter-kit",
    version="0.1.2",  # 自动更新建议见下方
    description="🚀 A comprehensive, beginner-friendly Generative AI development toolkit with RAG, LLM, and multimodal capabilities",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="YY-Nexus",
    author_email="contact@yynexus.com",
    maintainer="YY-Nexus",
    maintainer_email="contact@yynexus.com",
    license="MIT",
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
        "langchain",
        "openai",
        "milvus",
        "fastapi",
        "machine-learning",
        "artificial-intelligence",
        "multimodal",
    ],
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0,<2.0.0",  # ✅ 锁定兼容版本，避免构建失败
        *load_requirements("requirements.txt"),
    ],
    extras_require={
        "rag": ["chromadb", "milvus"],
        "multimodal": ["transformers", "torch", "opencv-python"],
        "dev": ["black", "flake8", "pre-commit"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
        "Framework :: FastAPI",
    ],
    entry_points={
        "console_scripts": ["sync-docs=RAG.examples.basic_rag.langchain.sync_docs:main"]
    },
    include_package_data=True,
    package_data={"genai_starter_kit": ["configs/*.yaml", "assets/*.png", "docs/*.md"]},
)
