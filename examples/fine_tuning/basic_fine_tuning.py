#!/usr/bin/env python3
"""
Basic Fine-tuning Example - Getting Started with Model Customization

This example demonstrates how to:
1. Prepare a custom dataset
2. Set up parameter-efficient fine-tuning (LoRA)
3. Train a model on your data
4. Evaluate and save the fine-tuned model

Note: This example provides the structure and workflow.
For actual training, you'll need to install additional packages:
- transformers
- peft
- torch
- datasets
"""

import sys
import os
from pathlib import Path
import json
from typing import Dict, Any, List

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from fine_tuning.dataset_preparation import DatasetPreparator, TrainingExample


class BasicFineTuningExample:
    """Basic fine-tuning workflow demonstration"""
    
    def __init__(self):
        self.dataset_prep = DatasetPreparator()
        self.model_name = "microsoft/DialoGPT-small"  # Small model for demo
        self.output_dir = Path("./fine_tuned_model")
    
    def create_sample_dataset(self) -> List[TrainingExample]:
        """Create a sample dataset for fine-tuning"""
        
        # Sample customer service training data
        raw_data = [
            {
                "instruction": "Respond as a helpful customer service agent",
                "input": "I can't log into my account",
                "output": "I'd be happy to help you with your login issue. Let me guide you through some troubleshooting steps. First, please try resetting your password by clicking 'Forgot Password' on the login page. If that doesn't work, please check if your caps lock is on or try clearing your browser cookies."
            },
            {
                "instruction": "Respond as a helpful customer service agent", 
                "input": "What are your business hours?",
                "output": "Our customer service team is available Monday through Friday from 9 AM to 6 PM EST. For urgent issues outside of business hours, you can submit a support ticket through our website and we'll respond within 24 hours."
            },
            {
                "instruction": "Respond as a helpful customer service agent",
                "input": "How do I cancel my subscription?",
                "output": "I understand you'd like to cancel your subscription. You can do this by logging into your account, going to Settings > Billing, and clicking 'Cancel Subscription'. Your account will remain active until the end of your current billing period. Is there anything specific that's prompting you to cancel? I'd be happy to help resolve any issues."
            },
            {
                "instruction": "Respond as a helpful customer service agent",
                "input": "The app keeps crashing on my phone",
                "output": "I'm sorry to hear you're experiencing crashes with our mobile app. Let's troubleshoot this together. First, try force-closing the app and reopening it. If that doesn't help, please try restarting your phone. You can also check if there's an app update available in your app store. What type of phone are you using?"
            },
            {
                "instruction": "Respond as a helpful customer service agent",
                "input": "I was charged twice this month",
                "output": "I apologize for the billing confusion. Double charges can be concerning, and I'll help you resolve this right away. This sometimes happens due to payment processing delays. I'll need to review your account details to investigate. Can you please provide me with the dates of both charges? In the meantime, I'll make sure you're not charged incorrectly again."
            },
            {
                "instruction": "Answer the technical question clearly and accurately",
                "input": "What is machine learning?",
                "output": "Machine learning is a subset of artificial intelligence (AI) that enables computers to learn and improve from experience without being explicitly programmed. It involves algorithms that automatically build mathematical models using training data to make predictions or decisions. There are three main types: supervised learning (with labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning through interaction)."
            },
            {
                "instruction": "Answer the technical question clearly and accurately",
                "input": "How does a neural network work?",
                "output": "A neural network is a computing system inspired by biological neural networks. It consists of interconnected nodes (neurons) organized in layers: input layer, hidden layers, and output layer. Each connection has a weight that adjusts during learning. Data flows forward through the network, and each neuron applies an activation function to its inputs. The network learns by adjusting weights through backpropagation, minimizing the difference between predicted and actual outputs."
            },
            {
                "instruction": "Explain the concept in simple terms",
                "input": "What is cloud computing?",
                "output": "Cloud computing is like renting computer resources (storage, processing power, software) over the internet instead of buying and maintaining your own physical hardware. Think of it like using electricity from a power company rather than generating your own power. You can access these resources on-demand, pay only for what you use, and scale up or down as needed. Examples include Google Drive for storage, Netflix for streaming, and Gmail for email."
            }
        ]
        
        # Convert to training examples
        examples = self.dataset_prep.create_instruction_dataset(
            raw_data,
            instruction_field="instruction",
            input_field="input", 
            output_field="output"
        )
        
        # Augment dataset to create more examples
        augmented_examples = self.dataset_prep.augment_dataset(
            examples,
            augmentation_methods=["paraphrase", "variation"]
        )
        
        print(f"Created {len(examples)} original examples")
        print(f"Augmented to {len(augmented_examples)} total examples")
        
        return augmented_examples
    
    def prepare_training_data(self, examples: List[TrainingExample]) -> Dict[str, Any]:
        """Prepare data for training"""
        
        # Validate dataset quality
        validation_report = self.dataset_prep.validate_dataset(examples)
        print("\n📊 Dataset Validation Report:")
        print(f"Total examples: {validation_report['total_examples']}")
        print(f"Quality score: {validation_report['quality_score']:.2f}")
        print(f"Average instruction length: {validation_report['instruction_length']['avg']:.1f} words")
        print(f"Average output length: {validation_report['output_length']['avg']:.1f} words")
        
        if validation_report['recommendations']:
            print("Recommendations:")
            for rec in validation_report['recommendations']:
                print(f"  • {rec}")
        
        # Split dataset
        train_examples, val_examples, test_examples = self.dataset_prep.split_dataset(
            examples,
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.1,
            shuffle=True
        )
        
        print(f"\n📂 Dataset Split:")
        print(f"Training: {len(train_examples)} examples")
        print(f"Validation: {len(val_examples)} examples") 
        print(f"Test: {len(test_examples)} examples")
        
        # Export datasets
        data_dir = Path("./training_data")
        data_dir.mkdir(exist_ok=True)
        
        self.dataset_prep.export_dataset(train_examples, data_dir / "train.json", "alpaca")
        self.dataset_prep.export_dataset(val_examples, data_dir / "val.json", "alpaca")
        self.dataset_prep.export_dataset(test_examples, data_dir / "test.json", "alpaca")
        
        print(f"✅ Datasets exported to {data_dir}")
        
        return {
            "train_examples": len(train_examples),
            "val_examples": len(val_examples),
            "test_examples": len(test_examples),
            "data_dir": str(data_dir),
            "validation_report": validation_report
        }
    
    def setup_training_config(self) -> Dict[str, Any]:
        """Set up training configuration"""
        
        config = {
            "model_name": self.model_name,
            "output_dir": str(self.output_dir),
            "learning_rate": 1e-4,
            "batch_size": 4,
            "num_epochs": 3,
            "warmup_steps": 100,
            "save_steps": 500,
            "eval_steps": 100,
            "logging_steps": 50,
            "max_length": 512,
            
            # LoRA configuration
            "use_lora": True,
            "lora_r": 16,
            "lora_alpha": 32,
            "lora_dropout": 0.1,
            "target_modules": ["q_proj", "v_proj"],
            
            # Training settings
            "gradient_accumulation_steps": 2,
            "fp16": True,
            "dataloader_num_workers": 2,
            "remove_unused_columns": False,
            
            # Evaluation
            "evaluation_strategy": "steps",
            "load_best_model_at_end": True,
            "metric_for_best_model": "eval_loss",
            "greater_is_better": False
        }
        
        print("🔧 Training Configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        return config
    
    def demonstrate_training_workflow(self):
        """Demonstrate the complete training workflow"""
        
        print("🚀 Fine-tuning Workflow Demonstration")
        print("=" * 50)
        
        # Note about requirements
        print("📋 Prerequisites:")
        print("This is a demonstration of the fine-tuning workflow.")
        print("For actual training, install additional packages:")
        print("  pip install transformers peft torch datasets accelerate")
        print("  pip install wandb  # for experiment tracking")
        print()
        
        # Step 1: Create dataset
        print("📚 Step 1: Creating and preparing dataset...")
        examples = self.create_sample_dataset()
        
        # Step 2: Prepare training data
        print("\n🔄 Step 2: Preparing training data...")
        data_info = self.prepare_training_data(examples)
        
        # Step 3: Set up configuration
        print("\n⚙️  Step 3: Setting up training configuration...")
        config = self.setup_training_config()
        
        # Step 4: Mock training process
        print("\n🏋️ Step 4: Training process (simulated)...")
        self.simulate_training_process(config, data_info)
        
        # Step 5: Evaluation and next steps
        print("\n📊 Step 5: Evaluation and next steps...")
        self.show_next_steps()
    
    def simulate_training_process(self, config: Dict[str, Any], data_info: Dict[str, Any]):
        """Simulate the training process"""
        
        print("Training simulation:")
        print(f"  Model: {config['model_name']}")
        print(f"  Training examples: {data_info['train_examples']}")
        print(f"  Epochs: {config['num_epochs']}")
        print(f"  Learning rate: {config['learning_rate']}")
        print(f"  Batch size: {config['batch_size']}")
        print()
        
        # Simulate training steps
        total_steps = (data_info['train_examples'] // config['batch_size']) * config['num_epochs']
        print(f"Estimated training steps: {total_steps}")
        
        # Mock training loop
        print("\nTraining progress (simulated):")
        for epoch in range(config['num_epochs']):
            print(f"  Epoch {epoch + 1}/{config['num_epochs']}")
            print(f"    Train Loss: {0.5 - epoch * 0.1:.3f}")
            print(f"    Eval Loss: {0.6 - epoch * 0.1:.3f}")
            print(f"    Learning Rate: {config['learning_rate'] * (0.9 ** epoch):.2e}")
        
        print("\n✅ Training completed (simulated)")
        print(f"Model would be saved to: {config['output_dir']}")
    
    def show_next_steps(self):
        """Show next steps for actual implementation"""
        
        print("🎯 Next Steps for Real Implementation:")
        print()
        
        print("1. 📦 Install Required Packages:")
        print("   pip install transformers>=4.30.0")
        print("   pip install peft>=0.5.0") 
        print("   pip install torch>=2.0.0")
        print("   pip install datasets>=2.14.0")
        print("   pip install accelerate>=0.21.0")
        print("   pip install wandb  # for experiment tracking")
        print()
        
        print("2. 🔧 Set Up Training Script:")
        print("   - Use HuggingFace Trainer or custom training loop")
        print("   - Implement LoRA with PEFT library")
        print("   - Add proper evaluation metrics")
        print("   - Set up experiment tracking with W&B")
        print()
        
        print("3. 💾 Prepare Your Data:")
        print("   - Use your own domain-specific data")
        print("   - Ensure data quality and diversity")
        print("   - Follow the format demonstrated above")
        print("   - Consider data privacy and licensing")
        print()
        
        print("4. 🚀 Training Tips:")
        print("   - Start with a small learning rate (1e-4 to 1e-5)")
        print("   - Use gradient accumulation for larger effective batch sizes")
        print("   - Monitor for overfitting with validation loss")
        print("   - Save checkpoints regularly")
        print("   - Use mixed precision (fp16) to save memory")
        print()
        
        print("5. 📊 Evaluation:")
        print("   - Test on held-out data")
        print("   - Use domain-specific metrics")
        print("   - Compare with base model performance")
        print("   - Get human evaluation for generation quality")
        print()
        
        print("6. 🔄 Deployment:")
        print("   - Export model for inference")
        print("   - Set up serving infrastructure")
        print("   - Monitor performance in production")
        print("   - Plan for model updates and retraining")
    
    def create_training_script_template(self):
        """Create a template training script"""
        
        template = '''#!/usr/bin/env python3
"""
Training Script Template for LoRA Fine-tuning
"""

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset
import wandb

def main():
    # Initialize wandb
    wandb.init(project="fine-tuning-demo")
    
    # Load model and tokenizer
    model_name = "microsoft/DialoGPT-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Add padding token if not present
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Configure LoRA
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj"]
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load dataset
    dataset = load_dataset("json", data_files={
        "train": "training_data/train.json",
        "validation": "training_data/val.json"
    })
    
    # Tokenize dataset
    def tokenize_function(examples):
        # Format prompt
        prompts = []
        for i in range(len(examples["instruction"])):
            instruction = examples["instruction"][i]
            input_text = examples.get("input", [None] * len(examples["instruction"]))[i]
            output = examples["output"][i]
            
            if input_text:
                prompt = f"Instruction: {instruction}\\nInput: {input_text}\\nResponse: {output}"
            else:
                prompt = f"Instruction: {instruction}\\nResponse: {output}"
            prompts.append(prompt)
        
        return tokenizer(prompts, truncation=True, padding=True, max_length=512)
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=100,
        learning_rate=1e-4,
        fp16=True,
        logging_steps=50,
        evaluation_strategy="steps",
        eval_steps=100,
        save_steps=500,
        load_best_model_at_end=True,
        report_to="wandb"
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=data_collator
    )
    
    # Train
    trainer.train()
    
    # Save model
    trainer.save_model()
    tokenizer.save_pretrained("./fine_tuned_model")

if __name__ == "__main__":
    main()
'''
        
        script_path = Path("train_lora.py")
        with open(script_path, 'w') as f:
            f.write(template)
        
        print(f"📝 Created training script template: {script_path}")
        print("Edit this script with your specific requirements before running.")


def main():
    """Run the fine-tuning demonstration"""
    
    example = BasicFineTuningExample()
    
    # Run the demonstration
    example.demonstrate_training_workflow()
    
    # Create training script template
    print("\n📝 Creating training script template...")
    example.create_training_script_template()
    
    print("\n🎉 Fine-tuning demonstration completed!")
    print("\nFiles created:")
    print("  - training_data/train.json")
    print("  - training_data/val.json") 
    print("  - training_data/test.json")
    print("  - train_lora.py (template)")
    print()
    print("Ready to start your fine-tuning journey! 🚀")


if __name__ == "__main__":
    main()