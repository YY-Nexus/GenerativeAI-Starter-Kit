"""
Test Suite for RAG System
=========================

This module contains tests for the RAG (Retrieval-Augmented Generation) system.

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import pytest
import tempfile
import shutil
import os
import sys

# Add parent directory to path to import examples
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.rag.simple_rag import SimpleRAG, RAGConfig


class TestRAGSystem:
    """Test cases for the RAG system"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def rag_config(self, temp_dir):
        """Create a test configuration"""
        return RAGConfig(
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            chunk_size=100,  # Small for testing
            chunk_overlap=20,
            top_k=3,
            collection_name="test_collection",
            persist_directory=temp_dir
        )
    
    @pytest.fixture
    def rag_system(self, rag_config):
        """Create and initialize a RAG system for testing"""
        rag = SimpleRAG(rag_config)
        rag.initialize()
        return rag
    
    @pytest.fixture
    def sample_documents(self):
        """Sample documents for testing"""
        return [
            "Machine learning is a subset of artificial intelligence that focuses on algorithms.",
            "Deep learning uses neural networks with multiple layers to process data.",
            "Natural language processing helps computers understand human language."
        ]
    
    def test_initialization(self, rag_config):
        """Test RAG system initialization"""
        rag = SimpleRAG(rag_config)
        assert rag.config == rag_config
        assert rag.embedding_model is None
        assert rag.collection is None
        
        # Test initialization
        rag.initialize()
        assert rag.embedding_model is not None
        assert rag.collection is not None
    
    def test_add_documents(self, rag_system, sample_documents):
        """Test adding documents to the RAG system"""
        # Add documents
        rag_system.add_documents(sample_documents)
        
        # Check that documents were added
        collection_count = rag_system.collection.count()
        assert collection_count > 0
    
    def test_add_documents_with_metadata(self, rag_system, sample_documents):
        """Test adding documents with metadata"""
        metadata = [
            {"title": "ML Doc", "category": "basics"},
            {"title": "DL Doc", "category": "advanced"},
            {"title": "NLP Doc", "category": "applications"}
        ]
        
        # Add documents with metadata
        rag_system.add_documents(sample_documents, metadata)
        
        # Check that documents were added
        collection_count = rag_system.collection.count()
        assert collection_count > 0
    
    def test_search(self, rag_system, sample_documents):
        """Test searching for relevant documents"""
        # Add documents first
        rag_system.add_documents(sample_documents)
        
        # Search for relevant documents
        results = rag_system.search("What is machine learning?", top_k=2)
        
        assert len(results) <= 2
        assert len(results) > 0
        
        # Check result structure
        for result in results:
            assert 'id' in result
            assert 'document' in result
            assert 'metadata' in result
            assert isinstance(result['document'], str)
    
    def test_search_empty_collection(self, rag_system):
        """Test searching in an empty collection"""
        results = rag_system.search("test query")
        assert len(results) == 0
    
    def test_generate_response(self, rag_system):
        """Test response generation"""
        query = "What is artificial intelligence?"
        context_docs = [
            "Artificial intelligence is the simulation of human intelligence in machines.",
            "AI systems can learn, reason, and make decisions."
        ]
        
        response = rag_system.generate_response(query, context_docs)
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert query in response
    
    def test_config_validation(self):
        """Test configuration validation"""
        # Test default configuration
        config = RAGConfig()
        assert config.chunk_size > 0
        assert config.chunk_overlap >= 0
        assert config.top_k > 0
        assert config.embedding_model is not None
    
    def test_text_splitting(self, rag_system):
        """Test text splitting functionality"""
        long_text = "This is a very long document. " * 50  # Create long text
        
        # Add the long document
        rag_system.add_documents([long_text])
        
        # Verify that chunks were created
        collection_count = rag_system.collection.count()
        assert collection_count > 1  # Should be split into multiple chunks
    
    def test_search_similarity_scores(self, rag_system, sample_documents):
        """Test that search returns reasonable similarity scores"""
        # Add documents
        rag_system.add_documents(sample_documents)
        
        # Search with a query similar to one of the documents
        results = rag_system.search("machine learning algorithms")
        
        assert len(results) > 0
        # The first result should be reasonably similar
        if 'distance' in results[0] and results[0]['distance'] is not None:
            assert results[0]['distance'] < 1.0  # Cosine distance should be < 1


@pytest.mark.integration
class TestRAGIntegration:
    """Integration tests for the RAG system"""
    
    def test_end_to_end_workflow(self, tmp_path):
        """Test complete RAG workflow"""
        # Create config with temporary directory
        config = RAGConfig(
            chunk_size=200,
            chunk_overlap=50,
            top_k=3,
            persist_directory=str(tmp_path)
        )
        
        # Initialize system
        rag = SimpleRAG(config)
        rag.initialize()
        
        # Sample documents about AI topics
        documents = [
            """
            Artificial Intelligence (AI) is a broad field of computer science concerned with 
            building smart machines capable of performing tasks that typically require human intelligence.
            """,
            """
            Machine Learning is a subset of AI that enables computers to learn and improve from 
            experience without being explicitly programmed.
            """,
            """
            Deep Learning is a subset of machine learning that uses neural networks with multiple 
            layers to model complex patterns in data.
            """
        ]
        
        metadata = [
            {"topic": "AI", "difficulty": "beginner"},
            {"topic": "ML", "difficulty": "intermediate"},
            {"topic": "DL", "difficulty": "advanced"}
        ]
        
        # Add documents
        rag.add_documents(documents, metadata)
        
        # Test queries
        test_queries = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "Explain deep learning"
        ]
        
        for query in test_queries:
            # Search for relevant documents
            results = rag.search(query, top_k=2)
            assert len(results) > 0
            
            # Generate response
            context_docs = [result['document'] for result in results]
            response = rag.generate_response(query, context_docs)
            
            assert isinstance(response, str)
            assert len(response) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])