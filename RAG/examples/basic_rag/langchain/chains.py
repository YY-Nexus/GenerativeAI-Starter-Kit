# === 高效生成式 AI 数据管道集成 ===
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Milvus
import pymysql


class DocumentSyncChain:
    def __init__(self, vector_db_config, mysql_config):
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = Milvus(
            collection_name=vector_db_config["collection_name"],
            embedding_function=self.embeddings,
        )
        self.mysql_config = mysql_config

    def get_existing_doc_ids(self):
        """
        查询 MySQL 已存在的 doc_id 集合，避免重复写入。
        """
        conn = pymysql.connect(
            host=self.mysql_config["host"],
            user=self.mysql_config["user"],
            password=self.mysql_config["password"],
            database=self.mysql_config["database"],
            charset="utf8mb4",
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT doc_id FROM documents")
            rows = cursor.fetchall()
        conn.close()
        return set(row[0] for row in rows)

    def process_and_store(self, documents):
        # 唯一性校验，避免重复写入
        existing_ids = self.get_existing_doc_ids()
        new_docs = [
            doc for doc in documents if doc.metadata.get("id") not in existing_ids
        ]
        # 向量数据库存储，返回 doc_id 与状态
        results = self.vector_db.add_documents(new_docs)
        # results 可为 List[dict]，如 {"doc_id": ..., "status": ...}
        # 元数据写入 MySQL，并精准更新 embedding_status
        for i, doc in enumerate(new_docs):
            meta = self.extract_metadata(doc)
            # 若 results 有状态反馈，可用 meta["embedding_status"] = results[i].get("status", True)
            self.save_metadata_to_mysql(meta)

    def summarize_with_llm(self, documents, model_name="gpt-3.5-turbo"):
        """
        用 LLM 进行智能摘要（集成 LangChain SummarizerChain 或 OpenAI API）。
        """
        from langchain.chains.summarize import load_summarize_chain
        from langchain.chat_models import ChatOpenAI

        llm = ChatOpenAI(model_name=model_name)
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(documents)
        return summary

    def extract_metadata(self, doc):
        return {
            "doc_id": doc.metadata.get("id", ""),
            "title": doc.metadata.get("title", ""),
            "summary": getattr(doc, "page_content", str(doc))[:200],
            "source_path": doc.metadata.get("source", ""),
            "tags": doc.metadata.get("tags", ""),
            "embedding_status": True,
        }

    def save_metadata_to_mysql(self, meta):
        conn = pymysql.connect(
            host=self.mysql_config["host"],
            user=self.mysql_config["user"],
            password=self.mysql_config["password"],
            database=self.mysql_config["database"],
            charset="utf8mb4",
        )
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO documents (doc_id, title, summary, source_path, tags, embedding_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title), summary=VALUES(summary), source_path=VALUES(source_path), tags=VALUES(tags), embedding_status=VALUES(embedding_status)
            """
            cursor.execute(
                sql,
                (
                    meta["doc_id"],
                    meta["title"],
                    meta["summary"],
                    meta["source_path"],
                    meta["tags"],
                    meta["embedding_status"],
                ),
            )
        conn.commit()
        conn.close()


# 用法示例：
# vector_db_config = {"collection_name": "doc_vectors"}
# mysql_config = {"host": "127.0.0.1", "user": "root", "password": "yourpass", "database": "yyc3_GenerativeAI"}
# chain = DocumentSyncChain(vector_db_config, mysql_config)
# docs = ingest_docs("your_file_path")
# chain.process_and_store(docs)
"""
chains.py - RAG 文档链处理模块
支持多种文档类型自动同步化、智能扩展，适用于 Jupyter Notebook、PDF、Markdown、TXT 等。
"""
from langchain_community.document_loaders import NotebookLoader, UnstructuredFileLoader
from langchain_core.documents import Document
from typing import List, Union
import os

SUPPORTED_EXTS = (".txt", ".pdf", ".md", ".ipynb")


def ingest_docs(filepath: str) -> List[Document]:
    """
    智能文档同步化加载器，自动识别并加载支持的文档类型。
    支持扩展：可根据实际需求添加更多 loader。
    """
    filename = os.path.basename(filepath)
    if not filename.endswith(SUPPORTED_EXTS):
        raise ValueError(f"{filename} 不是有效的文档类型: {SUPPORTED_EXTS}")
    try:
        if filename.endswith(".ipynb"):
            # Jupyter Notebook 支持，包含输出内容
            raw_documents = NotebookLoader(filepath, include_outputs=True).load()
        else:
            # 其他文档类型自动处理
            raw_documents = UnstructuredFileLoader(filepath).load()
        # 智能化拓展：可在此处添加后处理、向量化、摘要等功能
        return raw_documents
    except Exception as e:
        raise RuntimeError(f"文档加载失败: {e}")


# === 智能拓展功能框架 ===
import threading
import time


def auto_sync_docs(directory: str, interval: int = 300):
    """
    自动同步目录下文档，定时扫描并更新知识库。
    interval: 扫描间隔（秒），默认5分钟。
    """

    def sync_loop():
        while True:
            for fname in os.listdir(directory):
                fpath = os.path.join(directory, fname)
                if os.path.isfile(fpath) and fname.endswith(SUPPORTED_EXTS):
                    try:
                        ingest_docs(fpath)
                        # 可在此处集成知识库更新逻辑
                    except Exception as e:
                        print(f"同步失败: {fname}: {e}")
            time.sleep(interval)

    thread = threading.Thread(target=sync_loop, daemon=True)
    thread.start()


def summarize_documents(documents: List[Document], max_length: int = 200) -> List[str]:
    """
    对文档内容进行智能摘要（示例：截断文本）。
    可集成 LLM/摘要算法。
    """
    summaries: List[str] = []
    for doc in documents:
        text = getattr(doc, "page_content", str(doc))
        # 预留：可调用 LLM summarization API
        summaries.append(text[:max_length] + ("..." if len(text) > max_length else ""))
    return summaries


def filter_documents(documents: List[Document], keywords: List[str]) -> List[Document]:
    """
    按关键词过滤文档内容。
    """
    filtered: List[Document] = []
    for doc in documents:
        text = getattr(doc, "page_content", str(doc))
        if any(kw in text for kw in keywords):
            filtered.append(doc)
    return filtered


# === 向量化/LLM集成预留接口 ===
def vectorize_documents(documents: List[Document]) -> List[Union[list, dict]]:
    """
    文档向量化处理（可集成 embedding/向量数据库）。
    """
    # 预留：可调用 embedding API 或本地模型
    return [getattr(doc, "page_content", str(doc)) for doc in documents]


def llm_summarize(texts: List[str], model_name: str = "gpt-3.5-turbo") -> List[str]:
    """
    调用 LLM API 进行智能摘要（需集成 openai/azure/langchain LLM）。
    """
    # 预留：可集成 openai/langchain LLM summarization
    return [t[:100] + "..." for t in texts]
