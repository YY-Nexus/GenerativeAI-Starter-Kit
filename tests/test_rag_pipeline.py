#!/usr/bin/env python3
"""
Tests for RAG pipeline functionality
"""

import sys
import os
import pytest
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from rag.vector_store import VectorStoreManager, ChromaVectorStore
from rag.retriever import DocumentRetriever
from rag.generator import ResponseGenerator, HuggingFaceLLM
from rag.pipeline import RAGPipeline


class TestVectorStore:
    """Test vector store functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.documents = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing deals with human language."
        ]
        self.metadata = [
            {"source": "ml.txt", "topic": "ml"},
            {"source": "dl.txt", "topic": "dl"},
            {"source": "nlp.txt", "topic": "nlp"}
        ]
    
    def teardown_method(self):
        """Cleanup test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_chroma_vector_store(self):
        """Test ChromaDB vector store"""
        store = VectorStoreManager(
            store_type="chroma",
            collection_name="test",
            persist_directory=str(Path(self.temp_dir) / "chroma")
        )
        
        # Add documents
        store.add_documents(self.documents, self.metadata)
        
        # Search
        results = store.search("neural networks", k=2)
        
        assert len(results) <= 2
        assert len(results) > 0
        assert "distance" in results[0]
        assert "document" in results[0]
        assert "metadata" in results[0]
    
    def test_faiss_vector_store(self):
        """Test FAISS vector store"""
        store = VectorStoreManager(
            store_type="faiss",
            collection_name="test",
            persist_directory=str(Path(self.temp_dir) / "faiss")
        )
        
        # Add documents
        store.add_documents(self.documents, self.metadata)
        
        # Search
        results = store.search("artificial intelligence", k=2)
        
        assert len(results) <= 2
        assert len(results) > 0
        assert "distance" in results[0]
        assert "document" in results[0]
        assert "metadata" in results[0]


class TestRetriever:
    """Test document retriever"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.vector_store = VectorStoreManager(
            store_type="chroma",
            collection_name="test_retriever",
            persist_directory=str(Path(self.temp_dir) / "chroma")
        )
        
        documents = [
            "Machine learning algorithms learn from data.",
            "Deep learning is a subset of machine learning.",
            "Neural networks are the foundation of deep learning."
        ]
        metadata = [
            {"source": "doc1.txt"},
            {"source": "doc2.txt"},
            {"source": "doc3.txt"}
        ]
        
        self.vector_store.add_documents(documents, metadata)
        self.retriever = DocumentRetriever(
            self.vector_store,
            top_k=2,
            similarity_threshold=0.3
        )
    
    def teardown_method(self):
        """Cleanup test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_basic_retrieval(self):
        """Test basic document retrieval"""
        results = self.retriever.retrieve("machine learning", k=2)
        
        assert len(results) <= 2
        assert all("relevance_score" in result for result in results)
        assert all("rank" in result for result in results)
    
    def test_context_window(self):
        """Test context window generation"""
        context = self.retriever.get_context_window("neural networks", window_size=2)
        
        assert isinstance(context, str)
        assert len(context) > 0
        assert "Source:" in context or "No relevant documents" in context
    
    def test_metadata_filtering(self):
        """Test metadata filtering"""
        results = self.retriever.retrieve_with_metadata_filter(
            "machine learning",
            metadata_filter={"source": "doc1.txt"},
            k=1
        )
        
        # Should find at most 1 result with specific source
        assert len(results) <= 1
        if results:
            assert results[0]["metadata"]["source"] == "doc1.txt"


class TestGenerator:
    """Test response generator"""
    
    def test_huggingface_llm_initialization(self):
        """Test Hugging Face LLM initialization"""
        try:
            llm = HuggingFaceLLM(model_name="microsoft/DialoGPT-small")
            assert llm.model_name == "microsoft/DialoGPT-small"
            assert hasattr(llm, 'generator')
        except ImportError:
            pytest.skip("Transformers not installed")
    
    def test_response_generator_initialization(self):
        """Test response generator initialization"""
        try:
            llm = HuggingFaceLLM(model_name="microsoft/DialoGPT-small")
            generator = ResponseGenerator(llm)
            assert generator.llm == llm
            assert hasattr(generator, 'response_template')
        except ImportError:
            pytest.skip("Transformers not installed")


class TestRAGPipeline:
    """Test complete RAG pipeline"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_pipeline_initialization(self):
        """Test RAG pipeline initialization"""
        try:
            pipeline = RAGPipeline(
                vector_store_type="chroma",
                llm_provider="huggingface",
                collection_name="test_pipeline",
                vector_store_kwargs={
                    "persist_directory": str(Path(self.temp_dir) / "chroma")
                }
            )
            
            assert pipeline.collection_name == "test_pipeline"
            assert pipeline.vector_store.store_type == "chroma"
            assert hasattr(pipeline, 'retriever')
            assert hasattr(pipeline, 'generator')
        except ImportError:
            pytest.skip("Required dependencies not installed")
    
    def test_add_documents(self):
        """Test adding documents to pipeline"""
        try:
            pipeline = RAGPipeline(
                vector_store_type="chroma",
                llm_provider="huggingface",
                collection_name="test_add_docs",
                vector_store_kwargs={
                    "persist_directory": str(Path(self.temp_dir) / "chroma")
                }
            )
            
            documents = [
                "Test document about machine learning.",
                "Another document about artificial intelligence."
            ]
            
            result = pipeline.add_documents(documents)
            
            assert result["status"] == "success"
            assert result["documents_added"] == 2
            assert "processing_time" in result
        except ImportError:
            pytest.skip("Required dependencies not installed")
    
    def test_chunking(self):
        """Test document chunking"""
        try:
            pipeline = RAGPipeline(
                vector_store_type="chroma",
                llm_provider="huggingface",
                collection_name="test_chunking",
                vector_store_kwargs={
                    "persist_directory": str(Path(self.temp_dir) / "chroma")
                }
            )
            
            # Create a long document that will be chunked
            long_document = "This is a test. " * 100  # 1600+ characters
            
            chunks, metadata = pipeline._chunk_documents(
                [long_document],
                [{"source": "long_doc.txt"}],
                chunk_size=100,
                chunk_overlap=20
            )
            
            assert len(chunks) > 1  # Should be chunked
            assert len(chunks) == len(metadata)
            assert all("chunk" in meta for meta in metadata)
        except ImportError:
            pytest.skip("Required dependencies not installed")


def test_environment_setup():
    """Test that the environment is set up correctly"""
    # Check that src directory exists
    src_dir = Path(__file__).parent.parent / "src"
    assert src_dir.exists(), "src directory not found"
    
    # Check that key modules exist
    assert (src_dir / "rag" / "__init__.py").exists()
    assert (src_dir / "rag" / "pipeline.py").exists()
    assert (src_dir / "rag" / "vector_store.py").exists()
    

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])