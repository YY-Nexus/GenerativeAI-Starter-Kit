"""
Complete RAG pipeline implementation
"""
from typing import List, Dict, Any, Optional, Union
import os
from pathlib import Path
import json
import time
from datetime import datetime

from .vector_store import VectorStoreManager
from .retriever import DocumentRetriever, MultiQueryRetriever
from .generator import ResponseGenerator, OpenAILLM, HuggingFaceLLM


class RAGPipeline:
    """Complete RAG pipeline orchestrating retrieval and generation"""
    
    def __init__(self, 
                 vector_store_type: str = "chroma",
                 llm_provider: str = "openai",
                 collection_name: str = "rag_documents",
                 top_k: int = 5,
                 similarity_threshold: float = 0.7,
                 llm_model: str = None,
                 **kwargs):
        """
        Initialize RAG pipeline
        
        Args:
            vector_store_type: Type of vector store ("chroma", "faiss")
            llm_provider: LLM provider ("openai", "huggingface")
            collection_name: Name for vector store collection
            top_k: Number of documents to retrieve
            similarity_threshold: Minimum similarity for retrieval
            llm_model: Specific model name
            **kwargs: Additional arguments for components
        """
        self.collection_name = collection_name
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        
        # Initialize vector store
        self.vector_store = VectorStoreManager(
            store_type=vector_store_type,
            collection_name=collection_name,
            **kwargs.get('vector_store_kwargs', {})
        )
        
        # Initialize retriever
        retriever_type = kwargs.get('retriever_type', 'standard')
        if retriever_type == 'multi_query':
            self.retriever = MultiQueryRetriever(
                self.vector_store,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
        else:
            self.retriever = DocumentRetriever(
                self.vector_store,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
        
        # Initialize LLM
        self.llm = self._initialize_llm(llm_provider, llm_model, **kwargs)
        
        # Initialize generator
        self.generator = ResponseGenerator(
            self.llm,
            response_template=kwargs.get('response_template')
        )
        
        # Conversation history for multi-turn conversations
        self.conversation_history = []
        
        # Performance tracking
        self.query_history = []
    
    def _initialize_llm(self, provider: str, model: str, **kwargs) -> Union[OpenAILLM, HuggingFaceLLM]:
        """Initialize LLM based on provider"""
        if provider == "openai":
            model = model or "gpt-3.5-turbo"
            return OpenAILLM(
                model=model,
                api_key=kwargs.get('openai_api_key')
            )
        elif provider == "huggingface":
            model = model or "microsoft/DialoGPT-small"
            return HuggingFaceLLM(model_name=model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def add_documents(self, documents: List[str], 
                     metadata: List[Dict[str, Any]] = None,
                     chunk_size: int = 1000,
                     chunk_overlap: int = 200) -> Dict[str, Any]:
        """
        Add documents to the vector store with optional chunking
        
        Args:
            documents: List of document texts
            metadata: List of metadata dictionaries
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            Dictionary with operation results
        """
        start_time = time.time()
        
        # Handle chunking if documents are large
        if chunk_size and any(len(doc) > chunk_size for doc in documents):
            chunked_docs, chunked_metadata = self._chunk_documents(
                documents, metadata, chunk_size, chunk_overlap
            )
        else:
            chunked_docs, chunked_metadata = documents, metadata
        
        # Add to vector store
        self.vector_store.add_documents(chunked_docs, chunked_metadata)
        
        end_time = time.time()
        
        return {
            "status": "success",
            "documents_added": len(documents),
            "chunks_created": len(chunked_docs),
            "processing_time": end_time - start_time,
            "timestamp": datetime.now().isoformat()
        }
    
    def _chunk_documents(self, documents: List[str], 
                        metadata: List[Dict[str, Any]] = None,
                        chunk_size: int = 1000,
                        chunk_overlap: int = 200) -> tuple:
        """Chunk large documents into smaller pieces"""
        chunked_docs = []
        chunked_metadata = []
        
        for i, doc in enumerate(documents):
            if len(doc) <= chunk_size:
                chunked_docs.append(doc)
                if metadata:
                    chunked_metadata.append(metadata[i])
                else:
                    chunked_metadata.append({"source": f"doc_{i}", "chunk": 0})
            else:
                # Split into chunks
                chunks = []
                start = 0
                chunk_num = 0
                
                while start < len(doc):
                    end = start + chunk_size
                    chunk = doc[start:end]
                    chunks.append(chunk)
                    
                    # Create metadata for chunk
                    chunk_meta = metadata[i].copy() if metadata else {"source": f"doc_{i}"}
                    chunk_meta["chunk"] = chunk_num
                    chunk_meta["chunk_start"] = start
                    chunk_meta["chunk_end"] = min(end, len(doc))
                    chunked_metadata.append(chunk_meta)
                    
                    start = end - chunk_overlap
                    chunk_num += 1
                
                chunked_docs.extend(chunks)
        
        return chunked_docs, chunked_metadata
    
    def query(self, question: str, 
             include_sources: bool = True,
             conversation_mode: bool = False,
             **generation_kwargs) -> Dict[str, Any]:
        """
        Main query method for the RAG pipeline
        
        Args:
            question: User's question
            include_sources: Whether to include source citations
            conversation_mode: Whether to use conversation history
            **generation_kwargs: Arguments for text generation
            
        Returns:
            Dictionary with answer and metadata
        """
        start_time = time.time()
        
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(question, k=self.top_k)
        
        if not retrieved_docs:
            return {
                "question": question,
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": [],
                "context_used": "",
                "retrieval_time": time.time() - start_time,
                "generation_time": 0,
                "total_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
        
        retrieval_time = time.time() - start_time
        generation_start = time.time()
        
        # Generate response
        if include_sources:
            result = self.generator.generate_with_citations(
                question, retrieved_docs, **generation_kwargs
            )
        elif conversation_mode:
            context = self.retriever.get_context_window(question, window_size=self.top_k)
            result = self.generator.generate_conversational(
                question, context, self.conversation_history, **generation_kwargs
            )
        else:
            context = self.retriever.get_context_window(question, window_size=self.top_k)
            result = self.generator.generate_response(
                question, context, **generation_kwargs
            )
        
        generation_time = time.time() - generation_start
        total_time = time.time() - start_time
        
        # Update conversation history if in conversation mode
        if conversation_mode:
            self.conversation_history.append({
                "question": question,
                "answer": result["answer"],
                "timestamp": datetime.now().isoformat()
            })
            # Keep only last 10 exchanges
            self.conversation_history = self.conversation_history[-10:]
        
        # Add performance metrics
        result.update({
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time,
            "retrieved_docs_count": len(retrieved_docs),
            "timestamp": datetime.now().isoformat()
        })
        
        # Track query for analytics
        self.query_history.append({
            "question": question,
            "response_length": len(result["answer"]),
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": total_time,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def batch_query(self, questions: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Process multiple queries in batch"""
        results = []
        for question in questions:
            result = self.query(question, **kwargs)
            results.append(result)
        return results
    
    def explain_query(self, question: str) -> Dict[str, Any]:
        """Get detailed explanation of query processing"""
        retrieval_explanation = self.retriever.explain_retrieval(question)
        
        return {
            "question": question,
            "retrieval_analysis": retrieval_explanation,
            "pipeline_config": {
                "vector_store_type": self.vector_store.store_type,
                "llm_model": getattr(self.llm, 'model', 'unknown'),
                "top_k": self.top_k,
                "similarity_threshold": self.similarity_threshold
            },
            "suggestions": self._get_query_suggestions(question, retrieval_explanation)
        }
    
    def _get_query_suggestions(self, question: str, retrieval_explanation: Dict) -> List[str]:
        """Generate suggestions for improving query results"""
        suggestions = []
        
        if retrieval_explanation['total_results'] == 0:
            suggestions.append("Try using different keywords or synonyms")
            suggestions.append("Check if relevant documents have been added to the knowledge base")
        elif retrieval_explanation['total_results'] < 3:
            suggestions.append("Try using broader or more general terms")
            suggestions.append("Consider breaking complex questions into simpler parts")
        
        avg_score = retrieval_explanation['summary']['average_score']
        if avg_score < 0.5:
            suggestions.append("Results have low relevance scores - try rephrasing your question")
            suggestions.append("Add more context or specific details to your question")
        
        return suggestions
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about pipeline usage"""
        if not self.query_history:
            return {"message": "No queries processed yet"}
        
        total_queries = len(self.query_history)
        avg_retrieval_time = sum(q["retrieval_time"] for q in self.query_history) / total_queries
        avg_generation_time = sum(q["generation_time"] for q in self.query_history) / total_queries
        avg_total_time = sum(q["total_time"] for q in self.query_history) / total_queries
        avg_response_length = sum(q["response_length"] for q in self.query_history) / total_queries
        
        return {
            "total_queries": total_queries,
            "average_retrieval_time": avg_retrieval_time,
            "average_generation_time": avg_generation_time,
            "average_total_time": avg_total_time,
            "average_response_length": avg_response_length,
            "conversation_turns": len(self.conversation_history)
        }
    
    def save_state(self, filepath: str):
        """Save pipeline state to file"""
        state = {
            "conversation_history": self.conversation_history,
            "query_history": self.query_history,
            "config": {
                "collection_name": self.collection_name,
                "top_k": self.top_k,
                "similarity_threshold": self.similarity_threshold
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load pipeline state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.conversation_history = state.get("conversation_history", [])
        self.query_history = state.get("query_history", [])
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def clear_documents(self):
        """Clear all documents from vector store"""
        self.vector_store.delete_collection()


if __name__ == "__main__":
    # Example usage
    import os
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable to run this example")
        exit(1)
    
    # Initialize pipeline
    pipeline = RAGPipeline(
        vector_store_type="chroma",
        llm_provider="openai",
        collection_name="test_pipeline",
        top_k=3
    )
    
    # Add sample documents
    documents = [
        "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence (AI) based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.",
        "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised.",
        "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data.",
        "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos. From the perspective of engineering, it seeks to understand and automate tasks that the human visual system can do."
    ]
    
    metadata = [
        {"source": "ml_intro.txt", "topic": "machine_learning", "author": "AI Research Team"},
        {"source": "deep_learning.txt", "topic": "deep_learning", "author": "Neural Network Lab"},
        {"source": "nlp_guide.txt", "topic": "natural_language_processing", "author": "Language AI Team"},
        {"source": "cv_basics.txt", "topic": "computer_vision", "author": "Vision Research Group"}
    ]
    
    # Add documents to pipeline
    result = pipeline.add_documents(documents, metadata)
    print(f"Added documents: {result}")
    print()
    
    # Query the pipeline
    questions = [
        "What is machine learning?",
        "How does deep learning relate to machine learning?",
        "What are the applications of computer vision?"
    ]
    
    for question in questions:
        print(f"Question: {question}")
        response = pipeline.query(question, include_sources=True)
        print(f"Answer: {response['answer']}")
        print(f"Sources: {[s['name'] for s in response.get('sources', [])]}")
        print(f"Processing time: {response['total_time']:.3f}s")
        print("-" * 50)
    
    # Get analytics
    analytics = pipeline.get_analytics()
    print(f"Analytics: {analytics}")