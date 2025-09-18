"""
Response generator for RAG pipeline using various LLM providers
"""
from typing import List, Dict, Any, Optional
import os
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass


class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


class HuggingFaceLLM(BaseLLM):
    """Hugging Face transformers LLM implementation"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        self.model_name = model_name
        
        try:
            from transformers import pipeline
            self.generator = pipeline("text-generation", model=model_name)
        except ImportError:
            raise ImportError("transformers package not installed. Run: pip install transformers")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Hugging Face model"""
        try:
            response = self.generator(
                prompt,
                max_length=kwargs.get("max_tokens", 200),
                temperature=kwargs.get("temperature", 0.7),
                do_sample=True,
                pad_token_id=50256
            )
            return response[0]['generated_text'][len(prompt):].strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"


class ResponseGenerator:
    """Main response generator that combines context and query"""
    
    def __init__(self, llm: BaseLLM, response_template: Optional[str] = None):
        self.llm = llm
        self.response_template = response_template or self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Get default response template"""
        return """You are a helpful AI assistant. Use the following context to answer the user's question. If the context doesn't contain relevant information, say so clearly.

Context:
{context}

Question: {question}

Answer: Please provide a comprehensive answer based on the context above. If the context doesn't contain sufficient information to answer the question, please state that clearly and provide what information you can."""
    
    def generate_response(self, question: str, context: str, **kwargs) -> Dict[str, Any]:
        """
        Generate response given question and context
        
        Args:
            question: User's question
            context: Retrieved context from documents
            **kwargs: Additional arguments for LLM generation
            
        Returns:
            Dictionary containing response and metadata
        """
        # Format prompt with template
        prompt = self.response_template.format(
            context=context,
            question=question
        )
        
        # Generate response
        response = self.llm.generate(prompt, **kwargs)
        
        return {
            "question": question,
            "answer": response,
            "context_used": context,
            "prompt": prompt,
            "model": getattr(self.llm, 'model', 'unknown'),
            "generation_params": kwargs
        }
    
    def generate_with_citations(self, question: str, 
                              retrieved_docs: List[Dict[str, Any]], 
                              **kwargs) -> Dict[str, Any]:
        """
        Generate response with citations to source documents
        
        Args:
            question: User's question
            retrieved_docs: List of retrieved documents with metadata
            **kwargs: Additional arguments for LLM generation
            
        Returns:
            Dictionary containing response with citations
        """
        # Build context with source references
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs):
            source_id = f"[{i+1}]"
            context_parts.append(f"{source_id} {doc['document']}")
            
            source_info = doc.get('metadata', {})
            source_name = source_info.get('source', f'Document {i+1}')
            sources.append({
                'id': source_id,
                'name': source_name,
                'relevance_score': doc.get('relevance_score', 0),
                'metadata': source_info
            })
        
        context = "\n\n".join(context_parts)
        
        # Enhanced template for citations
        citation_template = """You are a helpful AI assistant. Use the following numbered context sources to answer the user's question. When you reference information from the context, include the source number in brackets like [1] or [2].

Context Sources:
{context}

Question: {question}

Answer: Please provide a comprehensive answer based on the context sources above. Include source citations [1], [2], etc. when referencing specific information. If the context doesn't contain sufficient information, state that clearly."""
        
        prompt = citation_template.format(
            context=context,
            question=question
        )
        
        # Generate response
        response = self.llm.generate(prompt, **kwargs)
        
        return {
            "question": question,
            "answer": response,
            "sources": sources,
            "context_used": context,
            "prompt": prompt,
            "model": getattr(self.llm, 'model', 'unknown'),
            "generation_params": kwargs
        }
    
    def generate_conversational(self, question: str, context: str, 
                              conversation_history: List[Dict[str, str]] = None,
                              **kwargs) -> Dict[str, Any]:
        """
        Generate conversational response considering chat history
        
        Args:
            question: Current user question
            context: Retrieved context
            conversation_history: List of previous exchanges
            **kwargs: Additional arguments for LLM generation
            
        Returns:
            Dictionary containing conversational response
        """
        # Build conversation context
        conversation_context = ""
        if conversation_history:
            conv_parts = []
            for exchange in conversation_history[-3:]:  # Last 3 exchanges
                conv_parts.append(f"Human: {exchange.get('question', '')}")
                conv_parts.append(f"Assistant: {exchange.get('answer', '')}")
            conversation_context = "\n".join(conv_parts)
        
        # Enhanced template for conversation
        conv_template = """You are a helpful AI assistant engaged in a conversation. Use the following context and conversation history to provide a natural, conversational response.

Document Context:
{context}

Previous Conversation:
{conversation_context}

Current Question: {question}

Answer: Please provide a natural, conversational response that considers both the document context and the conversation history. Reference previous parts of the conversation when relevant."""
        
        prompt = conv_template.format(
            context=context,
            conversation_context=conversation_context,
            question=question
        )
        
        # Generate response
        response = self.llm.generate(prompt, **kwargs)
        
        return {
            "question": question,
            "answer": response,
            "context_used": context,
            "conversation_history": conversation_history,
            "prompt": prompt,
            "model": getattr(self.llm, 'model', 'unknown'),
            "generation_params": kwargs
        }


class MultiModalGenerator(ResponseGenerator):
    """Extended generator that can handle multimodal inputs"""
    
    def __init__(self, llm: BaseLLM, vision_model: Optional[str] = None):
        super().__init__(llm)
        self.vision_model = vision_model
    
    def generate_with_image(self, question: str, context: str, 
                           image_path: str, **kwargs) -> Dict[str, Any]:
        """
        Generate response considering both text context and image
        Note: This is a placeholder - actual implementation would depend on specific multimodal model
        """
        # For now, just add image reference to context
        enhanced_context = f"{context}\n\n[IMAGE PROVIDED: {image_path}]"
        
        enhanced_question = f"{question}\n\nNote: An image has been provided for context. Please consider both the text context and the image in your response."
        
        return self.generate_response(enhanced_question, enhanced_context, **kwargs)


if __name__ == "__main__":
    # Example usage
    import os
    
    # Test with different LLM providers
    if os.getenv("OPENAI_API_KEY"):
        print("Testing OpenAI LLM...")
        openai_llm = OpenAILLM(model="gpt-3.5-turbo")
        generator = ResponseGenerator(openai_llm)
        
        context = "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data."
        question = "What is machine learning?"
        
        result = generator.generate_response(question, context)
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print()
    
    # Test with citation generation
    retrieved_docs = [
        {
            "document": "Machine learning is a method of data analysis that automates analytical model building.",
            "metadata": {"source": "ml_basics.txt"},
            "relevance_score": 0.95
        },
        {
            "document": "Deep learning is a subset of machine learning that uses neural networks.",
            "metadata": {"source": "deep_learning.txt"},
            "relevance_score": 0.80
        }
    ]
    
    if os.getenv("OPENAI_API_KEY"):
        result_with_citations = generator.generate_with_citations(
            "What is the relationship between machine learning and deep learning?",
            retrieved_docs
        )
        print("With citations:")
        print(f"Answer: {result_with_citations['answer']}")
        print(f"Sources: {[s['name'] for s in result_with_citations['sources']]}")