"""
Vector store implementations for different databases
"""
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path


class BaseVectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store"""
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        pass
    
    @abstractmethod
    def delete_collection(self):
        """Delete the collection"""
        pass


class ChromaVectorStore(BaseVectorStore):
    """ChromaDB implementation of vector store"""
    
    def __init__(self, collection_name: str = "documents", 
                 persist_directory: str = "./data/vector_stores/chroma"):
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to ChromaDB"""
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(documents))]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Create IDs
        ids = [f"{self.collection_name}_{i}" for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
        
        print(f"Added {len(documents)} documents to {self.collection_name}")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else 0
            })
        
        return formatted_results
    
    def delete_collection(self):
        """Delete the collection"""
        self.client.delete_collection(name=self.collection_name)


class FAISSVectorStore(BaseVectorStore):
    """FAISS implementation of vector store"""
    
    def __init__(self, collection_name: str = "documents",
                 persist_directory: str = "./data/vector_stores/faiss"):
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        # Initialize FAISS index
        import faiss
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product
        self.documents = []
        self.metadata = []
        
        # Load existing index if available
        self._load_index()
    
    def _save_index(self):
        """Save FAISS index and metadata"""
        import faiss
        import pickle
        
        index_path = self.persist_directory / f"{self.collection_name}.index"
        metadata_path = self.persist_directory / f"{self.collection_name}_metadata.pkl"
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata and documents
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)
    
    def _load_index(self):
        """Load existing FAISS index and metadata"""
        import faiss
        import pickle
        
        index_path = self.persist_directory / f"{self.collection_name}.index"
        metadata_path = self.persist_directory / f"{self.collection_name}_metadata.pkl"
        
        if index_path.exists() and metadata_path.exists():
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load metadata and documents
            with open(metadata_path, 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to FAISS"""
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(documents))]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and metadata
        self.documents.extend(documents)
        self.metadata.extend(metadata)
        
        # Save to disk
        self._save_index()
        
        print(f"Added {len(documents)} documents to {self.collection_name}")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        if len(self.documents) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Format results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'distance': 1 - score  # Convert similarity to distance
                })
        
        return results
    
    def delete_collection(self):
        """Delete the collection"""
        import faiss
        
        # Reset index
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.metadata = []
        
        # Remove files
        index_path = self.persist_directory / f"{self.collection_name}.index"
        metadata_path = self.persist_directory / f"{self.collection_name}_metadata.pkl"
        
        if index_path.exists():
            index_path.unlink()
        if metadata_path.exists():
            metadata_path.unlink()


class VectorStoreManager:
    """Manager for different vector store implementations"""
    
    def __init__(self, store_type: str = "chroma", **kwargs):
        self.store_type = store_type
        
        if store_type == "chroma":
            self.store = ChromaVectorStore(**kwargs)
        elif store_type == "faiss":
            self.store = FAISSVectorStore(**kwargs)
        else:
            raise ValueError(f"Unsupported store type: {store_type}")
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store"""
        return self.store.add_documents(documents, metadata)
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        return self.store.search(query, k)
    
    def delete_collection(self):
        """Delete the collection"""
        return self.store.delete_collection()


if __name__ == "__main__":
    # Example usage
    store = VectorStoreManager(store_type="chroma", collection_name="test")
    
    # Add sample documents
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a versatile programming language.",
        "Machine learning is a subset of artificial intelligence.",
        "Vector databases are essential for RAG applications."
    ]
    
    store.add_documents(documents)
    
    # Search
    results = store.search("What is machine learning?", k=2)
    for result in results:
        print(f"Document: {result['document']}")
        print(f"Distance: {result['distance']:.4f}")
        print("---")