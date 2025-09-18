from setuptools import setup, find_packages

setup(
    name="genai-starter-kit",
    version="0.1.0",
    description="A starter kit for Generative AI applications, including RAG, LLM, vector DB, CLI, API, and more.",
    author="YY-Nexus",
    author_email="contact@yynexus.com",
    url="https://github.com/YY-Nexus/GenerativeAI-Starter-Kit",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "pymilvus",
        "pymysql",
        "fastapi",
        "uvicorn",
        "pytest"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "sync-docs=RAG.examples.basic_rag.langchain.sync_docs:main"
        ]
    },
    include_package_data=True,
)