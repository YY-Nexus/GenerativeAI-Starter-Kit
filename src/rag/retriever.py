"""
Document retriever for RAG pipeline
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
from .vector_store import VectorStoreManager


class DocumentRetriever:
    """Document retriever that finds relevant documents for queries"""
    
    def __init__(self, vector_store: VectorStoreManager, 
                 top_k: int = 5, 
                 similarity_threshold: float = 0.7):
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: The query string
            k: Number of documents to retrieve (defaults to self.top_k)
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        k = k or self.top_k
        
        # Search for similar documents
        results = self.vector_store.search(query, k=k)
        
        # Filter by similarity threshold
        filtered_results = [
            result for result in results 
            if (1 - result.get('distance', 1)) >= self.similarity_threshold
        ]
        
        # Add relevance scores
        for i, result in enumerate(filtered_results):
            result['rank'] = i + 1
            result['relevance_score'] = 1 - result.get('distance', 1)
        
        return filtered_results
    
    def retrieve_with_metadata_filter(self, query: str, 
                                    metadata_filter: Dict[str, Any],
                                    k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve documents with metadata filtering
        
        Args:
            query: The query string
            metadata_filter: Dictionary of metadata key-value pairs to filter by
            k: Number of documents to retrieve
            
        Returns:
            Filtered list of relevant documents
        """
        # Get all results first
        all_results = self.retrieve(query, k=k*2 if k else self.top_k*2)
        
        # Filter by metadata
        filtered_results = []
        for result in all_results:
            metadata = result.get('metadata', {})
            if all(metadata.get(key) == value for key, value in metadata_filter.items()):
                filtered_results.append(result)
                if k and len(filtered_results) >= k:
                    break
        
        return filtered_results[:k] if k else filtered_results
    
    def get_context_window(self, query: str, 
                          window_size: int = 3,
                          k: Optional[int] = None) -> str:
        """
        Get a context window of relevant documents formatted as a single string
        
        Args:
            query: The query string
            window_size: Maximum number of documents to include in context
            k: Number of documents to retrieve
            
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, k=k or window_size)
        
        if not results:
            return "No relevant documents found."
        
        context_parts = []
        for i, result in enumerate(results[:window_size]):
            doc_text = result['document']
            source = result.get('metadata', {}).get('source', f'Document {i+1}')
            context_parts.append(f"[Source: {source}]\n{doc_text}")
        
        return "\n\n".join(context_parts)
    
    def explain_retrieval(self, query: str, k: Optional[int] = None) -> Dict[str, Any]:
        """
        Get detailed explanation of retrieval process
        
        Args:
            query: The query string
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with retrieval explanation and results
        """
        results = self.retrieve(query, k=k)
        
        explanation = {
            'query': query,
            'total_results': len(results),
            'threshold_used': self.similarity_threshold,
            'top_k': k or self.top_k,
            'results': results,
            'summary': {
                'highest_score': max([r['relevance_score'] for r in results]) if results else 0,
                'lowest_score': min([r['relevance_score'] for r in results]) if results else 0,
                'average_score': sum([r['relevance_score'] for r in results]) / len(results) if results else 0
            }
        }
        
        return explanation


class MultiQueryRetriever(DocumentRetriever):
    """Enhanced retriever that uses multiple query variations"""
    
    def __init__(self, vector_store: VectorStoreManager, 
                 top_k: int = 5, 
                 similarity_threshold: float = 0.7,
                 query_variations: int = 3):
        super().__init__(vector_store, top_k, similarity_threshold)
        self.query_variations = query_variations
    
    def generate_query_variations(self, query: str) -> List[str]:
        """
        Generate variations of the query for better retrieval
        This is a simple implementation - in practice, you might use an LLM
        """
        variations = [query]  # Original query
        
        # Simple variations (in practice, use LLM for better variations)
        words = query.lower().split()
        
        # Add question variations
        if not query.endswith('?'):
            variations.append(f"What is {query}?")
            variations.append(f"How does {query} work?")
        
        # Add more specific versions
        if len(words) > 2:
            variations.append(' '.join(words[:len(words)//2]))
            variations.append(' '.join(words[len(words)//2:]))
        
        return variations[:self.query_variations]
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve using multiple query variations and merge results
        """
        variations = self.generate_query_variations(query)
        all_results = {}  # Use dict to avoid duplicates
        
        for variation in variations:
            results = super().retrieve(variation, k=k)
            for result in results:
                doc_id = hash(result['document'])  # Simple deduplication
                if doc_id not in all_results or result['relevance_score'] > all_results[doc_id]['relevance_score']:
                    all_results[doc_id] = result
        
        # Sort by relevance score and return top k
        sorted_results = sorted(all_results.values(), 
                              key=lambda x: x['relevance_score'], 
                              reverse=True)
        
        return sorted_results[:k or self.top_k]


if __name__ == "__main__":
    # Example usage
    from .vector_store import VectorStoreManager
    
    # Initialize vector store and add documents
    vector_store = VectorStoreManager(store_type="chroma", collection_name="test_retriever")
    
    documents = [
        "Machine learning is a method of data analysis that automates analytical model building.",
        "Deep learning is a subset of machine learning that uses neural networks with multiple layers.",
        "Natural language processing (NLP) is a branch of AI that deals with human language.",
        "Computer vision is a field of AI that trains computers to interpret visual information.",
        "Reinforcement learning is a type of machine learning where agents learn through interaction."
    ]
    
    metadata = [
        {"source": "ml_basics.txt", "topic": "machine_learning"},
        {"source": "deep_learning.txt", "topic": "deep_learning"},
        {"source": "nlp_guide.txt", "topic": "nlp"},
        {"source": "cv_intro.txt", "topic": "computer_vision"},
        {"source": "rl_tutorial.txt", "topic": "reinforcement_learning"}
    ]
    
    vector_store.add_documents(documents, metadata)
    
    # Test retriever
    retriever = DocumentRetriever(vector_store, top_k=3, similarity_threshold=0.3)
    
    query = "What is deep learning?"
    results = retriever.retrieve(query)
    
    print(f"Query: {query}")
    print(f"Found {len(results)} relevant documents:")
    for result in results:
        print(f"- Score: {result['relevance_score']:.3f}")
        print(f"  Document: {result['document'][:100]}...")
        print(f"  Source: {result['metadata']['source']}")
        print()
    
    # Test context window
    context = retriever.get_context_window(query, window_size=2)
    print("Context window:")
    print(context)