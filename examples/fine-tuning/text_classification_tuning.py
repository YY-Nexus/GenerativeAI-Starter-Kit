"""
Text Classification Fine-tuning Example
=======================================

This example demonstrates how to fine-tune a pre-trained model for text classification.
We'll use a BERT-based model and adapt it for sentiment analysis or custom classification tasks.

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import os
import json
import torch
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Transformers for model and tokenizer
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)

# Datasets for handling data
from datasets import Dataset
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class FineTuningConfig:
    """Configuration for fine-tuning"""
    model_name: str = "distilbert-base-uncased"
    num_labels: int = 2
    max_length: int = 512
    batch_size: int = 16
    learning_rate: float = 2e-5
    num_epochs: int = 3
    warmup_steps: int = 500
    weight_decay: float = 0.01
    output_dir: str = "./fine_tuned_models"
    save_steps: int = 500
    eval_steps: int = 500
    logging_steps: int = 100


class TextClassificationTrainer:
    """Fine-tune models for text classification"""
    
    def __init__(self, config: FineTuningConfig = None):
        self.config = config or FineTuningConfig()
        self.tokenizer = None
        self.model = None
        self.trainer = None
        self.label_to_id = {}
        self.id_to_label = {}
    
    def initialize(self):
        """Initialize tokenizer and model"""
        print("🚀 Initializing fine-tuning setup...")
        
        # Load tokenizer
        print(f"📖 Loading tokenizer: {self.config.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        
        # Load model
        print(f"🧠 Loading model: {self.config.model_name}")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.config.model_name,
            num_labels=self.config.num_labels
        )
        
        print("✅ Initialization complete")
    
    def prepare_data(self, texts: List[str], labels: List[str], test_size: float = 0.2) -> Tuple[Dataset, Dataset]:
        """Prepare and tokenize data for training"""
        print("📊 Preparing data for training...")
        
        # Create label mappings
        unique_labels = list(set(labels))
        self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}
        
        print(f"Labels: {self.label_to_id}")
        
        # Convert string labels to numeric
        numeric_labels = [self.label_to_id[label] for label in labels]
        
        # Split data
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, numeric_labels, test_size=test_size, random_state=42, stratify=numeric_labels
        )
        
        print(f"Training samples: {len(train_texts)}")
        print(f"Validation samples: {len(val_texts)}")
        
        # Tokenize data
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                truncation=True,
                padding=True,
                max_length=self.config.max_length
            )
        
        # Create datasets
        train_dataset = Dataset.from_dict({
            'text': train_texts,
            'labels': train_labels
        })
        
        val_dataset = Dataset.from_dict({
            'text': val_texts,
            'labels': val_labels
        })
        
        # Tokenize
        train_dataset = train_dataset.map(tokenize_function, batched=True)
        val_dataset = val_dataset.map(tokenize_function, batched=True)
        
        return train_dataset, val_dataset
    
    def compute_metrics(self, eval_pred):
        """Compute metrics for evaluation"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        accuracy = accuracy_score(labels, predictions)
        
        return {
            'accuracy': accuracy,
        }
    
    def train(self, train_dataset: Dataset, val_dataset: Dataset):
        """Train the model"""
        print("🏋️ Starting model training...")
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            warmup_steps=self.config.warmup_steps,
            weight_decay=self.config.weight_decay,
            logging_dir=f"{self.config.output_dir}/logs",
            logging_steps=self.config.logging_steps,
            evaluation_strategy="steps",
            eval_steps=self.config.eval_steps,
            save_steps=self.config.save_steps,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
            report_to="none",  # Disable wandb/tensorboard
        )
        
        # Data collator
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        
        # Initialize trainer
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
        )
        
        # Train
        train_result = self.trainer.train()
        
        # Save the model
        self.trainer.save_model()
        
        print("✅ Training completed!")
        print(f"Training loss: {train_result.training_loss:.4f}")
        
        return train_result
    
    def evaluate(self, test_dataset: Dataset) -> Dict:
        """Evaluate the model"""
        if not self.trainer:
            raise ValueError("Model not trained yet. Call train() first.")
        
        print("📊 Evaluating model...")
        eval_result = self.trainer.evaluate(test_dataset)
        
        print(f"Evaluation accuracy: {eval_result['eval_accuracy']:.4f}")
        
        return eval_result
    
    def predict(self, texts: List[str]) -> List[Dict]:
        """Make predictions on new texts"""
        if not self.model or not self.tokenizer:
            raise ValueError("Model not initialized. Call initialize() first.")
        
        predictions = []
        
        for text in texts:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=self.config.max_length
            )
            
            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits, dim=-1)
                predicted_class = torch.argmax(logits, dim=-1).item()
            
            # Format result
            result = {
                'text': text,
                'predicted_label': self.id_to_label[predicted_class],
                'confidence': probabilities[0][predicted_class].item(),
                'all_probabilities': {
                    self.id_to_label[i]: prob.item() 
                    for i, prob in enumerate(probabilities[0])
                }
            }
            
            predictions.append(result)
        
        return predictions
    
    def save_model(self, path: str):
        """Save the trained model"""
        if not self.model or not self.tokenizer:
            raise ValueError("Model not trained yet.")
        
        os.makedirs(path, exist_ok=True)
        
        # Save model and tokenizer
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        
        # Save label mappings
        with open(os.path.join(path, "label_mappings.json"), "w") as f:
            json.dump({
                "label_to_id": self.label_to_id,
                "id_to_label": self.id_to_label
            }, f, indent=2)
        
        print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str):
        """Load a trained model"""
        print(f"📖 Loading model from {path}")
        
        # Load model and tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        
        # Load label mappings
        with open(os.path.join(path, "label_mappings.json"), "r") as f:
            mappings = json.load(f)
            self.label_to_id = mappings["label_to_id"]
            self.id_to_label = {int(k): v for k, v in mappings["id_to_label"].items()}
        
        print("✅ Model loaded successfully")


def create_sample_data() -> Tuple[List[str], List[str]]:
    """Create sample data for demonstration"""
    texts = [
        "I love this product! It's amazing and works perfectly.",
        "This is the worst thing I've ever bought. Completely useless.",
        "The item is okay, nothing special but does the job.",
        "Fantastic quality and great customer service. Highly recommended!",
        "Terrible experience. The product broke after one day.",
        "Good value for money. Would buy again.",
        "Not worth the price. Very disappointed.",
        "Excellent build quality and fast shipping.",
        "The product is fine but could be better.",
        "Outstanding! Exceeded my expectations completely.",
        "Poor quality materials and bad design.",
        "Decent product with room for improvement.",
        "Amazing features and user-friendly interface.",
        "Waste of money. Don't buy this.",
        "Solid product with good performance.",
        "Absolutely love it! Best purchase ever.",
        "Not impressed. Expected much better.",
        "Great product at a reasonable price.",
        "Horrible quality and poor support.",
        "Perfect for my needs. Very satisfied."
    ]
    
    labels = [
        "positive", "negative", "neutral", "positive", "negative",
        "positive", "negative", "positive", "neutral", "positive",
        "negative", "neutral", "positive", "negative", "positive",
        "positive", "negative", "positive", "negative", "positive"
    ]
    
    return texts, labels


def demo_fine_tuning():
    """Demonstrate the fine-tuning process"""
    print("🎯 Text Classification Fine-tuning Demo")
    print("=" * 50)
    
    # Create sample data
    texts, labels = create_sample_data()
    print(f"📊 Created {len(texts)} sample texts with {len(set(labels))} classes")
    
    # Initialize trainer
    config = FineTuningConfig(
        num_labels=len(set(labels)),
        num_epochs=2,  # Reduced for demo
        batch_size=8   # Reduced for demo
    )
    
    trainer = TextClassificationTrainer(config)
    trainer.initialize()
    
    # Prepare data
    train_dataset, val_dataset = trainer.prepare_data(texts, labels)
    
    # Train model
    print("\n🏋️ Training model (this may take a few minutes)...")
    try:
        train_result = trainer.train(train_dataset, val_dataset)
        
        # Evaluate
        eval_result = trainer.evaluate(val_dataset)
        
        # Test predictions
        test_texts = [
            "This is an amazing product!",
            "I hate this thing.",
            "It's okay, I guess."
        ]
        
        print("\n🔮 Testing predictions:")
        predictions = trainer.predict(test_texts)
        
        for pred in predictions:
            print(f"Text: '{pred['text']}'")
            print(f"Predicted: {pred['predicted_label']} (confidence: {pred['confidence']:.3f})")
            print()
        
        # Save model
        save_path = "./demo_model"
        trainer.save_model(save_path)
        
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        print("This might be due to limited resources. Try reducing batch_size or num_epochs.")


if __name__ == "__main__":
    demo_fine_tuning()