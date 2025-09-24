import pytest
from unittest.mock import MagicMock
from chains import DocumentSyncChain


class DummyDoc:
    def __init__(self, doc_id):
        self.metadata = {
            "id": doc_id,
            "title": f"Title {doc_id}",
            "source": "src",
            "tags": "tag",
        }
        self.page_content = f"Content for {doc_id}"


def test_doc_id_uniqueness(monkeypatch):
    # 模拟 MySQL 已有 doc_id
    chain = DocumentSyncChain(
        {"collection_name": "test"},
        {"host": "localhost", "user": "root", "password": "", "database": "test"},
    )
    monkeypatch.setattr(chain, "get_existing_doc_ids", lambda: {"a", "b"})
    chain.vector_db = MagicMock()
    chain.save_metadata_to_mysql = MagicMock()
    docs = [DummyDoc("a"), DummyDoc("b"), DummyDoc("c"), DummyDoc("d")]
    chain.process_and_store(docs)
    # 只处理未重复的 doc_id
    chain.vector_db.add_documents.assert_called_once()
    assert chain.vector_db.add_documents.call_args[0][0][0].metadata["id"] == "c"
    assert chain.vector_db.add_documents.call_args[0][0][1].metadata["id"] == "d"
    # 只写入新文档元数据
    assert chain.save_metadata_to_mysql.call_count == 2


def test_extract_metadata():
    chain = DocumentSyncChain(
        {"collection_name": "test"},
        {"host": "localhost", "user": "root", "password": "", "database": "test"},
    )
    doc = DummyDoc("x")
    meta = chain.extract_metadata(doc)
    assert meta["doc_id"] == "x"
    assert meta["title"] == "Title x"
    assert meta["summary"].startswith("Content for x")
    assert meta["embedding_status"] is True
