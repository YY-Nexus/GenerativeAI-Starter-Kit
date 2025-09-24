"""
Simple RAG (Retrieval-Augmented Generation) Example
==================================================

This example demonstrates how to build a basic RAG system using:
- Document chunking and embedding
- Vector database for similarity search
- Language model for response generation

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import os
import yaml
from typing import List, Dict, Any
from dataclasses import dataclass

# Core libraries
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Text processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


@dataclass
class RAGConfig:
    """Configuration for RAG system"""

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    collection_name: str = "rag_documents"
    persist_directory: str = "./chroma_db"


class SimpleRAG:
    """A simple RAG (Retrieval-Augmented Generation) system"""

    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.embedding_model = None
        self.vector_db = None
        self.collection = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
        )

    def initialize(self):
        """Initialize the RAG system"""
        print("🚀 Initializing RAG system...")

        # Load embedding model
        print(f"📊 Loading embedding model: {self.config.embedding_model}")
        self.embedding_model = SentenceTransformer(self.config.embedding_model)

        # Initialize vector database
        print("🗄️ Initializing vector database...")
        self.vector_db = chromadb.PersistentClient(
            path=self.config.persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )

        # Get or create collection
        try:
            self.collection = self.vector_db.get_collection(self.config.collection_name)
            print(f"✅ Found existing collection: {self.config.collection_name}")
        except Exception:
            self.collection = self.vector_db.create_collection(
                self.config.collection_name
            )
            print(f"✅ Created new collection: {self.config.collection_name}")

    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector database"""
        if not self.collection:
            raise ValueError("RAG system not initialized. Call initialize() first.")

        print(f"📝 Processing {len(documents)} documents...")

        # Split documents into chunks
        all_chunks = []
        all_metadata = []

        for i, doc in enumerate(documents):
            chunks = self.text_splitter.split_text(doc)
            all_chunks.extend(chunks)

            # Add metadata for each chunk
            doc_metadata = metadata[i] if metadata and i < len(metadata) else {}
            for j, chunk in enumerate(chunks):
                chunk_metadata = {
                    **doc_metadata,
                    "doc_id": i,
                    "chunk_id": j,
                    "chunk_text": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                }
                all_metadata.append(chunk_metadata)

        print(f"📄 Created {len(all_chunks)} chunks")

        # Generate embeddings
        print("🔢 Generating embeddings...")
        embeddings = self.embedding_model.encode(all_chunks, show_progress_bar=True)

        # Add to vector database
        print("💾 Adding to vector database...")
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]

        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=all_chunks,
            metadatas=all_metadata,
            ids=ids,
        )

        print(f"✅ Added {len(all_chunks)} chunks to the database")

    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if not self.collection:
            raise ValueError("RAG system not initialized. Call initialize() first.")

        top_k = top_k or self.config.top_k

        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])

        # Search in vector database
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(), n_results=top_k
        )

        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            result = {
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": (
                    results["distances"][0][i] if "distances" in results else None
                ),
            }
            formatted_results.append(result)

        return formatted_results

    def generate_response(self, query: str, context_docs: List[str]) -> str:
        """Generate response using retrieved context (simplified version)"""
        # This is a simplified version - in practice, you'd use a proper LLM
        context = "\n\n".join(context_docs[:3])  # Use top 3 documents

        response = f"""Based on the provided context, here's what I found:

Query: {query}

Relevant Information:
{context}

Note: This is a simplified response. In a full implementation, this would be generated by a language model like GPT, Claude, or open-source alternatives."""

        return response


def demo_rag():
    """Demonstrate the RAG system with sample data"""
    print("🎯 RAG System Demo")
    print("=" * 50)

    # Sample documents
    sample_docs = [
        """
        Artificial Intelligence (AI) is a broad field of computer science concerned with building
        smart machines capable of performing tasks that typically require human intelligence.
        AI systems can learn, reason, and make decisions. Machine learning is a subset of AI
        that enables computers to learn and improve from experience without being explicitly programmed.
        """,
        """
        Machine Learning (ML) is a method of data analysis that automates analytical model building.
        It is a branch of artificial intelligence based on the idea that systems can learn from data,
        identify patterns and make decisions with minimal human intervention. Common types include
        supervised learning, unsupervised learning, and reinforcement learning.
        """,
        """
        Deep Learning is a subset of machine learning that uses neural networks with multiple layers
        to model and understand complex patterns in data. It's particularly effective for tasks like
        image recognition, natural language processing, and speech recognition. Popular frameworks
        include TensorFlow, PyTorch, and Keras.
        """,
        """
        Natural Language Processing (NLP) is a branch of artificial intelligence that helps computers
        understand, interpret and manipulate human language. NLP combines computational linguistics
        with statistical, machine learning, and deep learning models. Applications include chatbots,
        translation services, and sentiment analysis.
        """,
    ]

    metadata = [
        {"title": "Introduction to AI", "topic": "artificial_intelligence"},
        {"title": "Machine Learning Basics", "topic": "machine_learning"},
        {"title": "Deep Learning Overview", "topic": "deep_learning"},
        {"title": "NLP Fundamentals", "topic": "nlp"},
    ]

    # Initialize RAG system
    rag = SimpleRAG()
    rag.initialize()

    # Add documents
    rag.add_documents(sample_docs, metadata)

    # Test queries
    test_queries = [
        "What is machine learning?",
        "How does deep learning work?",
        "What are the applications of NLP?",
        "Explain artificial intelligence",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 30)

        # Search for relevant documents
        results = rag.search(query, top_k=2)

        # Extract context
        context_docs = [result["document"] for result in results]

        # Generate response
        response = rag.generate_response(query, context_docs)
        print(response)
        print("\n" + "=" * 50)


if __name__ == "__main__":
    demo_rag()
