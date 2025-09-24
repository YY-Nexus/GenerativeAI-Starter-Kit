"""
Sample Data Generator for GenerativeAI Starter Kit
==================================================

This module provides sample datasets for testing and demonstration purposes.
Includes data for RAG, multimodal, and fine-tuning examples.

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import json
import os
from typing import List, Dict, Tuple, Any
import random


def generate_ai_documents() -> List[Dict[str, Any]]:
    """Generate sample AI-related documents for RAG demonstrations"""

    documents = [
        {
            "title": "Introduction to Machine Learning",
            "content": """
            Machine Learning (ML) is a subset of artificial intelligence that focuses on algorithms
            and statistical models that enable computer systems to improve their performance on a
            specific task through experience. Unlike traditional programming where explicit
            instructions are provided, ML systems learn patterns from data to make predictions
            or decisions. The three main types of machine learning are supervised learning,
            unsupervised learning, and reinforcement learning. Supervised learning uses labeled
            data to train models, unsupervised learning finds patterns in unlabeled data, and
            reinforcement learning learns through interaction with an environment.
            """,
            "category": "basics",
            "tags": [
                "machine learning",
                "AI",
                "algorithms",
                "supervised",
                "unsupervised",
            ],
        },
        {
            "title": "Deep Learning Fundamentals",
            "content": """
            Deep Learning is a specialized subset of machine learning that uses artificial neural
            networks with multiple layers (hence "deep") to model and understand complex patterns
            in data. These networks are inspired by the structure and function of the human brain,
            consisting of interconnected nodes (neurons) organized in layers. Each layer transforms
            the input data through weighted connections and activation functions. Deep learning has
            revolutionized fields such as computer vision, natural language processing, and speech
            recognition. Popular frameworks include TensorFlow, PyTorch, and Keras, which provide
            tools for building and training deep neural networks.
            """,
            "category": "advanced",
            "tags": [
                "deep learning",
                "neural networks",
                "TensorFlow",
                "PyTorch",
                "computer vision",
            ],
        },
        {
            "title": "Natural Language Processing Overview",
            "content": """
            Natural Language Processing (NLP) is a branch of artificial intelligence that helps
            computers understand, interpret, and generate human language in a valuable way. NLP
            combines computational linguistics—rule-based modeling of human language—with statistical,
            machine learning, and deep learning models. Key NLP tasks include text classification,
            sentiment analysis, named entity recognition, machine translation, question answering,
            and text summarization. Modern NLP heavily relies on transformer architectures like
            BERT, GPT, and T5, which have achieved state-of-the-art results across various language
            understanding and generation tasks.
            """,
            "category": "applications",
            "tags": [
                "NLP",
                "language processing",
                "BERT",
                "GPT",
                "transformers",
                "text analysis",
            ],
        },
        {
            "title": "Computer Vision Applications",
            "content": """
            Computer Vision is a field of artificial intelligence that trains computers to interpret
            and understand visual information from the world. It involves acquiring, processing,
            analyzing, and understanding digital images and videos to extract high-dimensional data
            from the real world. Common applications include image classification, object detection,
            facial recognition, medical image analysis, autonomous vehicles, and augmented reality.
            Convolutional Neural Networks (CNNs) are the foundation of most modern computer vision
            systems, with architectures like ResNet, VGG, and EfficientNet achieving remarkable
            performance on various visual recognition tasks.
            """,
            "category": "applications",
            "tags": [
                "computer vision",
                "CNN",
                "image classification",
                "object detection",
                "ResNet",
            ],
        },
        {
            "title": "Reinforcement Learning Basics",
            "content": """
            Reinforcement Learning (RL) is a type of machine learning where an agent learns to make
            decisions by performing actions in an environment to maximize cumulative reward. Unlike
            supervised learning, RL doesn't require labeled training data. Instead, the agent learns
            through trial and error, receiving feedback in the form of rewards or penalties. Key
            concepts include states, actions, rewards, policies, and value functions. Popular RL
            algorithms include Q-learning, policy gradients, and actor-critic methods. RL has shown
            remarkable success in game playing (like AlphaGo), robotics, autonomous vehicles, and
            recommendation systems.
            """,
            "category": "advanced",
            "tags": [
                "reinforcement learning",
                "Q-learning",
                "policy gradients",
                "AlphaGo",
                "robotics",
            ],
        },
        {
            "title": "Generative AI and Large Language Models",
            "content": """
            Generative AI refers to artificial intelligence systems capable of creating new content,
            including text, images, code, and other media. Large Language Models (LLMs) like GPT-3,
            GPT-4, and ChatGPT are prominent examples that can generate human-like text for various
            tasks including writing, coding, and question answering. These models are trained on
            vast amounts of text data using transformer architectures and techniques like
            self-attention. The emergence of generative AI has sparked discussions about creativity,
            ethics, and the future of work, while opening new possibilities for content creation,
            education, and human-AI collaboration.
            """,
            "category": "emerging",
            "tags": [
                "generative AI",
                "LLM",
                "GPT",
                "ChatGPT",
                "transformers",
                "content creation",
            ],
        },
    ]

    return documents


def generate_sentiment_data() -> Tuple[List[str], List[str]]:
    """Generate sample sentiment analysis data"""

    positive_texts = [
        "I absolutely love this product! It exceeded my expectations.",
        "Amazing quality and fantastic customer service.",
        "This is the best purchase I've made this year.",
        "Excellent build quality and beautiful design.",
        "Outstanding performance and great value for money.",
        "Perfect for my needs, highly recommended!",
        "Incredible features and user-friendly interface.",
        "Top-notch quality and fast delivery.",
        "Superb craftsmanship and attention to detail.",
        "Wonderful experience from start to finish.",
    ]

    negative_texts = [
        "Terrible quality, complete waste of money.",
        "Horrible customer service and defective product.",
        "This is the worst thing I've ever bought.",
        "Poor build quality and doesn't work as advertised.",
        "Extremely disappointed with this purchase.",
        "Awful experience, would not recommend to anyone.",
        "Cheaply made and broke after one use.",
        "Useless product with terrible design.",
        "Overpriced and underdelivered on promises.",
        "Regret buying this, total disappointment.",
    ]

    neutral_texts = [
        "The product is okay, nothing special but functional.",
        "Average quality, meets basic requirements.",
        "It's fine for the price, not amazing but decent.",
        "Reasonable product with some pros and cons.",
        "Acceptable quality, could be better but workable.",
        "Standard features, nothing extraordinary.",
        "Adequate for basic use, room for improvement.",
        "Decent product with average performance.",
        "Fair quality, gets the job done.",
        "Ordinary product, meets minimum expectations.",
    ]

    texts = positive_texts + negative_texts + neutral_texts
    labels = (
        ["positive"] * len(positive_texts)
        + ["negative"] * len(negative_texts)
        + ["neutral"] * len(neutral_texts)
    )

    # Shuffle the data
    combined = list(zip(texts, labels))
    random.shuffle(combined)
    texts, labels = zip(*combined)

    return list(texts), list(labels)


def generate_qa_pairs() -> List[Dict[str, str]]:
    """Generate sample question-answer pairs"""

    qa_pairs = [
        {
            "question": "What is machine learning?",
            "answer": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
        },
        {
            "question": "How does deep learning work?",
            "answer": "Deep learning uses artificial neural networks with multiple layers to automatically learn patterns and features from data.",
        },
        {
            "question": "What are the main types of machine learning?",
            "answer": "The three main types are supervised learning, unsupervised learning, and reinforcement learning.",
        },
        {
            "question": "What is natural language processing?",
            "answer": "NLP is a field of AI that helps computers understand, interpret, and generate human language.",
        },
        {
            "question": "What are transformers in AI?",
            "answer": "Transformers are a type of neural network architecture that uses self-attention mechanisms and are particularly effective for language tasks.",
        },
        {
            "question": "How does computer vision work?",
            "answer": "Computer vision uses algorithms and neural networks to identify and analyze visual content in images and videos.",
        },
        {
            "question": "What is reinforcement learning used for?",
            "answer": "Reinforcement learning is used for game playing, robotics, autonomous vehicles, and decision-making systems.",
        },
        {
            "question": "What are large language models?",
            "answer": "Large language models are AI systems trained on vast amounts of text data to understand and generate human-like text.",
        },
    ]

    return qa_pairs


def generate_multimodal_data() -> List[Dict[str, Any]]:
    """Generate sample multimodal data descriptions"""

    image_descriptions = [
        {
            "filename": "cat_on_table.jpg",
            "description": "A fluffy orange cat sitting on a wooden table next to a window",
            "tags": ["cat", "animal", "table", "indoor", "pet"],
            "objects": ["cat", "table", "window"],
            "scene": "indoor",
        },
        {
            "filename": "sunset_mountain.jpg",
            "description": "Beautiful sunset over snow-capped mountains with orange and pink sky",
            "tags": ["sunset", "mountain", "landscape", "nature", "sky"],
            "objects": ["mountains", "sky", "clouds"],
            "scene": "outdoor",
        },
        {
            "filename": "city_street.jpg",
            "description": "Busy city street with people walking, cars, and tall buildings",
            "tags": ["city", "street", "urban", "people", "buildings"],
            "objects": ["people", "cars", "buildings", "street"],
            "scene": "urban",
        },
        {
            "filename": "beach_waves.jpg",
            "description": "Ocean waves crashing on a sandy beach with blue sky and white clouds",
            "tags": ["beach", "ocean", "waves", "sand", "nature"],
            "objects": ["waves", "beach", "sand", "sky"],
            "scene": "outdoor",
        },
    ]

    return image_descriptions


def save_sample_data():
    """Save all sample data to JSON files"""

    # Create datasets directory if it doesn't exist
    datasets_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(datasets_dir, exist_ok=True)

    # Generate and save AI documents
    ai_docs = generate_ai_documents()
    with open(
        os.path.join(datasets_dir, "ai_documents.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(ai_docs, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(ai_docs)} AI documents")

    # Generate and save sentiment data
    texts, labels = generate_sentiment_data()
    sentiment_data = [
        {"text": text, "label": label} for text, label in zip(texts, labels)
    ]
    with open(
        os.path.join(datasets_dir, "sentiment_data.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(sentiment_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(sentiment_data)} sentiment examples")

    # Generate and save QA pairs
    qa_pairs = generate_qa_pairs()
    with open(os.path.join(datasets_dir, "qa_pairs.json"), "w", encoding="utf-8") as f:
        json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(qa_pairs)} QA pairs")

    # Generate and save multimodal data
    multimodal_data = generate_multimodal_data()
    with open(
        os.path.join(datasets_dir, "multimodal_data.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(multimodal_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(multimodal_data)} multimodal examples")

    print("🎉 All sample data generated successfully!")


if __name__ == "__main__":
    save_sample_data()
