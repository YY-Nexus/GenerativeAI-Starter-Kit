#!/usr/bin/env python3
"""
Basic RAG Example - Getting Started with Retrieval-Augmented Generation

This example demonstrates how to:
1. Set up a vector database
2. Add documents to the knowledge base
3. Query the system using natural language
4. Get responses with source citations

Requirements:
- OpenAI API key (set in .env file)
- Run: pip install -r requirements/base.txt
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from rag.pipeline import RAGPipeline
import json


def main():
    """Main example function"""
    print("🚀 Basic RAG Example - GenerativeAI Starter Kit")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        print("   Copy .env.example to .env and add your API key")
        return
    
    # Initialize RAG pipeline
    print("🔧 Initializing RAG pipeline...")
    pipeline = RAGPipeline(
        vector_store_type="chroma",      # Using ChromaDB for vector storage
        llm_provider="openai",           # Using OpenAI for text generation
        collection_name="basic_example", # Name your collection
        top_k=3,                        # Retrieve top 3 most relevant documents
        similarity_threshold=0.5        # Minimum similarity score
    )
    
    # Sample documents about AI and machine learning
    print("📚 Adding documents to knowledge base...")
    documents = [
        """
        Machine Learning Overview:
        Machine learning (ML) is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. ML algorithms build mathematical models based on training data to make predictions or decisions. There are three main types: supervised learning (with labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction with environment).
        """,
        
        """
        Deep Learning Fundamentals:
        Deep learning is a specialized subset of machine learning that uses artificial neural networks with multiple layers (hence "deep") to model and understand complex patterns in data. It's particularly effective for tasks like image recognition, natural language processing, and speech recognition. Deep learning has powered breakthroughs in computer vision, language translation, and game playing AI systems like AlphaGo.
        """,
        
        """
        Natural Language Processing (NLP):
        NLP is a branch of AI that focuses on the interaction between computers and human language. It combines computational linguistics with statistical, machine learning, and deep learning models to enable computers to process and analyze large amounts of natural language data. Key applications include sentiment analysis, machine translation, chatbots, text summarization, and question-answering systems.
        """,
        
        """
        Computer Vision Applications:
        Computer vision is an AI field that trains computers to interpret and understand visual information from the world. It uses deep learning models, particularly convolutional neural networks (CNNs), to analyze images and videos. Applications include facial recognition, medical image analysis, autonomous vehicles, quality control in manufacturing, and augmented reality systems.
        """,
        
        """
        Generative AI and Large Language Models:
        Generative AI refers to artificial intelligence systems that can create new content, including text, images, audio, and code. Large Language Models (LLMs) like GPT, Claude, and PaLM are trained on vast amounts of text data and can generate human-like text, answer questions, write code, and perform various language tasks. They represent a significant advancement in AI capabilities and have numerous practical applications.
        """,
    ]
    
    # Metadata for each document
    metadata = [
        {"source": "ML_Guide.pdf", "topic": "machine_learning", "author": "AI Research Team", "date": "2024"},
        {"source": "DL_Handbook.pdf", "topic": "deep_learning", "author": "Neural Networks Lab", "date": "2024"},
        {"source": "NLP_Tutorial.pdf", "topic": "natural_language_processing", "author": "Language AI Group", "date": "2024"},
        {"source": "CV_Applications.pdf", "topic": "computer_vision", "author": "Vision Research Team", "date": "2024"},
        {"source": "GenAI_Overview.pdf", "topic": "generative_ai", "author": "Modern AI Institute", "date": "2024"},
    ]
    
    # Add documents to the pipeline
    result = pipeline.add_documents(documents, metadata)
    print(f"✅ Successfully added {result['documents_added']} documents")
    print(f"   Created {result['chunks_created']} chunks")
    print(f"   Processing time: {result['processing_time']:.2f} seconds")
    print()
    
    # Example queries
    queries = [
        "What is machine learning and how does it work?",
        "What's the difference between machine learning and deep learning?",
        "How is NLP used in real-world applications?",
        "What are some applications of computer vision?",
        "Explain generative AI and its capabilities"
    ]
    
    print("🤖 Querying the RAG system...")
    print("=" * 50)
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 40)
        
        # Get response with sources
        response = pipeline.query(
            query,
            include_sources=True,
            temperature=0.7,
            max_tokens=300
        )
        
        print(f"🎯 Answer:")
        print(response['answer'])
        print()
        
        # Show sources
        if response.get('sources'):
            print(f"📚 Sources:")
            for source in response['sources']:
                print(f"   {source['id']} {source['name']} (Score: {source['relevance_score']:.3f})")
        
        print(f"⏱️  Response time: {response['total_time']:.2f}s")
        print("=" * 50)
    
    # Demonstrate conversation mode
    print("\n💬 Conversation Mode Example:")
    print("=" * 50)
    
    # Reset and use conversation mode
    pipeline.reset_conversation()
    
    conversation_queries = [
        "What is deep learning?",
        "How is it different from traditional machine learning?",
        "Can you give me some specific examples of its applications?"
    ]
    
    for query in conversation_queries:
        print(f"\n👤 User: {query}")
        response = pipeline.query(
            query,
            conversation_mode=True,
            include_sources=False,
            temperature=0.7,
            max_tokens=200
        )
        print(f"🤖 Assistant: {response['answer']}")
    
    # Show analytics
    print("\n📊 Pipeline Analytics:")
    print("=" * 50)
    analytics = pipeline.get_analytics()
    for key, value in analytics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")
    
    # Save example results
    results_file = Path(__file__).parent / "example_results.json"
    example_results = {
        "pipeline_config": {
            "vector_store": "chroma",
            "llm_provider": "openai",
            "documents_added": len(documents)
        },
        "sample_queries": queries,
        "analytics": analytics,
        "timestamp": response['timestamp']
    }
    
    with open(results_file, 'w') as f:
        json.dump(example_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    print("\n🎉 Basic RAG example completed successfully!")
    print("\nNext steps:")
    print("- Try the advanced RAG example with custom data")
    print("- Explore multimodal examples")
    print("- Check out the fine-tuning tutorials")


if __name__ == "__main__":
    main()