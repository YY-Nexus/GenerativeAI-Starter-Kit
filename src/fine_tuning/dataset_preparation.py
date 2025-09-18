"""
Dataset preparation utilities for model fine-tuning
"""
import json
import csv
from typing import List, Dict, Any, Optional, Union, Tuple
from pathlib import Path
import random
from dataclasses import dataclass
import re


@dataclass
class TrainingExample:
    """Single training example structure"""
    instruction: str
    input: Optional[str] = None
    output: str = ""
    metadata: Optional[Dict[str, Any]] = None


class DatasetPreparator:
    """Prepare datasets for fine-tuning various model types"""
    
    def __init__(self):
        self.supported_formats = ["alpaca", "chatml", "instructional", "qa_pairs"]
    
    def load_raw_data(self, 
                     file_path: Union[str, Path],
                     format_type: str = "auto") -> List[Dict[str, Any]]:
        """
        Load raw data from various file formats
        
        Args:
            file_path: Path to data file
            format_type: Format type ("json", "csv", "txt", "auto")
            
        Returns:
            List of raw data records
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Auto-detect format if needed
        if format_type == "auto":
            format_type = file_path.suffix.lower().lstrip('.')
        
        if format_type == "json":
            return self._load_json_data(file_path)
        elif format_type == "csv":
            return self._load_csv_data(file_path)
        elif format_type == "txt":
            return self._load_text_data(file_path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _load_json_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single dict and list of dicts
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("JSON file must contain a dict or list of dicts")
    
    def _load_csv_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from CSV file"""
        data = []
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data
    
    def _load_text_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from text file (assume each line is a separate example)"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line:
                    data.append({
                        "id": i,
                        "text": line
                    })
        return data
    
    def create_instruction_dataset(self,
                                 raw_data: List[Dict[str, Any]],
                                 instruction_field: str = "instruction",
                                 input_field: Optional[str] = "input",
                                 output_field: str = "output") -> List[TrainingExample]:
        """
        Create instruction-following dataset
        
        Args:
            raw_data: Raw data records
            instruction_field: Field containing instructions
            input_field: Field containing input (optional)
            output_field: Field containing expected output
            
        Returns:
            List of training examples
        """
        examples = []
        
        for record in raw_data:
            try:
                instruction = record.get(instruction_field, "")
                input_text = record.get(input_field, "") if input_field else None
                output = record.get(output_field, "")
                
                if not instruction or not output:
                    continue
                
                example = TrainingExample(
                    instruction=instruction,
                    input=input_text,
                    output=output,
                    metadata={k: v for k, v in record.items() 
                            if k not in [instruction_field, input_field, output_field]}
                )
                examples.append(example)
                
            except Exception as e:
                print(f"Error processing record: {record}. Error: {e}")
                continue
        
        return examples
    
    def create_qa_dataset(self,
                         raw_data: List[Dict[str, Any]],
                         question_field: str = "question",
                         answer_field: str = "answer",
                         context_field: Optional[str] = None) -> List[TrainingExample]:
        """
        Create question-answering dataset
        
        Args:
            raw_data: Raw data records
            question_field: Field containing questions
            answer_field: Field containing answers
            context_field: Field containing context (optional)
            
        Returns:
            List of training examples
        """
        examples = []
        
        for record in raw_data:
            try:
                question = record.get(question_field, "")
                answer = record.get(answer_field, "")
                context = record.get(context_field, "") if context_field else None
                
                if not question or not answer:
                    continue
                
                # Format as instruction
                instruction = "Answer the following question."
                input_text = question
                if context:
                    input_text = f"Context: {context}\n\nQuestion: {question}"
                
                example = TrainingExample(
                    instruction=instruction,
                    input=input_text,
                    output=answer,
                    metadata={k: v for k, v in record.items() 
                            if k not in [question_field, answer_field, context_field]}
                )
                examples.append(example)
                
            except Exception as e:
                print(f"Error processing QA record: {record}. Error: {e}")
                continue
        
        return examples
    
    def create_chat_dataset(self,
                           conversations: List[List[Dict[str, str]]]) -> List[TrainingExample]:
        """
        Create chat/conversation dataset
        
        Args:
            conversations: List of conversations, each conversation is a list of messages
                          Each message should have 'role' and 'content' fields
            
        Returns:
            List of training examples
        """
        examples = []
        
        for conv_id, conversation in enumerate(conversations):
            if len(conversation) < 2:
                continue
            
            # Extract user messages and assistant responses
            for i in range(len(conversation) - 1):
                current_msg = conversation[i]
                next_msg = conversation[i + 1]
                
                if (current_msg.get('role') == 'user' and 
                    next_msg.get('role') == 'assistant'):
                    
                    # Build context from previous messages
                    context_msgs = conversation[:i]
                    context = self._format_conversation_context(context_msgs)
                    
                    input_text = current_msg.get('content', '')
                    if context:
                        input_text = f"{context}\n\nUser: {input_text}"
                    
                    example = TrainingExample(
                        instruction="Continue the conversation as a helpful assistant.",
                        input=input_text,
                        output=next_msg.get('content', ''),
                        metadata={'conversation_id': conv_id, 'turn': i}
                    )
                    examples.append(example)
        
        return examples
    
    def _format_conversation_context(self, messages: List[Dict[str, str]]) -> str:
        """Format conversation history as context"""
        if not messages:
            return ""
        
        formatted = []
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            formatted.append(f"{role.title()}: {content}")
        
        return "\n".join(formatted)
    
    def augment_dataset(self,
                       examples: List[TrainingExample],
                       augmentation_methods: List[str] = None) -> List[TrainingExample]:
        """
        Augment dataset with additional examples
        
        Args:
            examples: Original training examples
            augmentation_methods: List of augmentation methods to apply
            
        Returns:
            Augmented training examples
        """
        if not augmentation_methods:
            augmentation_methods = ["paraphrase", "variation"]
        
        augmented = examples.copy()
        
        for method in augmentation_methods:
            if method == "paraphrase":
                augmented.extend(self._paraphrase_examples(examples))
            elif method == "variation":
                augmented.extend(self._create_variations(examples))
            elif method == "reverse":
                augmented.extend(self._reverse_examples(examples))
        
        return augmented
    
    def _paraphrase_examples(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Create paraphrased versions (simple rule-based approach)"""
        paraphrased = []
        
        paraphrase_patterns = [
            (r'\bHow (.*?)\?', r'What is the way to \1?'),
            (r'\bWhat is (.*?)\?', r'Can you explain \1?'),
            (r'\bExplain (.*)', r'Tell me about \1'),
            (r'\bDescribe (.*)', r'What is \1?'),
        ]
        
        for example in examples[:len(examples)//4]:  # Paraphrase 25% of examples
            for pattern, replacement in paraphrase_patterns:
                new_instruction = re.sub(pattern, replacement, example.instruction, flags=re.IGNORECASE)
                if new_instruction != example.instruction:
                    paraphrased.append(TrainingExample(
                        instruction=new_instruction,
                        input=example.input,
                        output=example.output,
                        metadata={**(example.metadata or {}), 'augmented': 'paraphrase'}
                    ))
                    break
        
        return paraphrased
    
    def _create_variations(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Create variations with slight modifications"""
        variations = []
        
        variation_prefixes = [
            "Please help me understand: ",
            "I need to know: ",
            "Could you clarify: ",
            "I'm wondering about: "
        ]
        
        for example in examples[:len(examples)//5]:  # Create variations for 20%
            prefix = random.choice(variation_prefixes)
            new_instruction = prefix + example.instruction.lower()
            
            variations.append(TrainingExample(
                instruction=new_instruction,
                input=example.input,
                output=example.output,
                metadata={**(example.metadata or {}), 'augmented': 'variation'}
            ))
        
        return variations
    
    def _reverse_examples(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Create reverse examples (answer -> question)"""
        reversed_examples = []
        
        for example in examples[:len(examples)//10]:  # Reverse 10%
            if len(example.output.split()) < 20:  # Only for short answers
                reversed_examples.append(TrainingExample(
                    instruction="Generate a question that would result in this answer.",
                    input=example.output,
                    output=example.instruction + (f" {example.input}" if example.input else ""),
                    metadata={**(example.metadata or {}), 'augmented': 'reverse'}
                ))
        
        return reversed_examples
    
    def validate_dataset(self, examples: List[TrainingExample]) -> Dict[str, Any]:
        """
        Validate dataset quality and provide statistics
        
        Args:
            examples: Training examples to validate
            
        Returns:
            Validation report
        """
        if not examples:
            return {"error": "No examples provided"}
        
        # Basic statistics
        total_examples = len(examples)
        
        instruction_lengths = [len(ex.instruction.split()) for ex in examples]
        output_lengths = [len(ex.output.split()) for ex in examples]
        
        # Check for duplicates
        unique_instructions = len(set(ex.instruction for ex in examples))
        unique_outputs = len(set(ex.output for ex in examples))
        
        # Check for empty fields
        empty_instructions = sum(1 for ex in examples if not ex.instruction.strip())
        empty_outputs = sum(1 for ex in examples if not ex.output.strip())
        
        # Language detection (simple)
        languages = self._detect_languages(examples)
        
        report = {
            "total_examples": total_examples,
            "unique_instructions": unique_instructions,
            "unique_outputs": unique_outputs,
            "duplicate_instructions": total_examples - unique_instructions,
            "duplicate_outputs": total_examples - unique_outputs,
            "empty_instructions": empty_instructions,
            "empty_outputs": empty_outputs,
            "instruction_length": {
                "min": min(instruction_lengths),
                "max": max(instruction_lengths),
                "avg": sum(instruction_lengths) / len(instruction_lengths)
            },
            "output_length": {
                "min": min(output_lengths),
                "max": max(output_lengths),
                "avg": sum(output_lengths) / len(output_lengths)
            },
            "languages_detected": languages,
            "quality_score": self._calculate_quality_score(examples),
            "recommendations": self._get_recommendations(examples)
        }
        
        return report
    
    def _detect_languages(self, examples: List[TrainingExample]) -> Dict[str, int]:
        """Simple language detection based on character patterns"""
        languages = {"english": 0, "chinese": 0, "other": 0}
        
        for example in examples[:100]:  # Sample first 100
            text = example.instruction + " " + example.output
            
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            english_chars = len(re.findall(r'[a-zA-Z]', text))
            
            if chinese_chars > english_chars:
                languages["chinese"] += 1
            elif english_chars > 0:
                languages["english"] += 1
            else:
                languages["other"] += 1
        
        return languages
    
    def _calculate_quality_score(self, examples: List[TrainingExample]) -> float:
        """Calculate overall dataset quality score"""
        score = 1.0
        
        # Penalize duplicates
        unique_ratio = len(set(ex.instruction for ex in examples)) / len(examples)
        score *= unique_ratio
        
        # Penalize empty fields
        empty_ratio = sum(1 for ex in examples if not ex.instruction.strip() or not ex.output.strip()) / len(examples)
        score *= (1 - empty_ratio)
        
        # Penalize extreme length imbalances
        output_lengths = [len(ex.output.split()) for ex in examples]
        if max(output_lengths) > 10 * min(output_lengths):
            score *= 0.9
        
        return max(0.0, min(1.0, score))
    
    def _get_recommendations(self, examples: List[TrainingExample]) -> List[str]:
        """Get recommendations for improving dataset quality"""
        recommendations = []
        
        # Check duplicates
        unique_instructions = len(set(ex.instruction for ex in examples))
        if unique_instructions < len(examples) * 0.9:
            recommendations.append("Consider removing duplicate instructions")
        
        # Check length distribution
        output_lengths = [len(ex.output.split()) for ex in examples]
        avg_length = sum(output_lengths) / len(output_lengths)
        
        if avg_length < 10:
            recommendations.append("Consider adding more detailed outputs")
        elif avg_length > 200:
            recommendations.append("Consider breaking down long outputs")
        
        # Check for empty fields
        empty_count = sum(1 for ex in examples if not ex.instruction.strip() or not ex.output.strip())
        if empty_count > 0:
            recommendations.append(f"Remove {empty_count} examples with empty fields")
        
        # Check variety
        if len(examples) < 100:
            recommendations.append("Consider adding more examples for better training")
        
        return recommendations
    
    def split_dataset(self,
                     examples: List[TrainingExample],
                     train_ratio: float = 0.8,
                     val_ratio: float = 0.1,
                     test_ratio: float = 0.1,
                     shuffle: bool = True) -> Tuple[List[TrainingExample], List[TrainingExample], List[TrainingExample]]:
        """
        Split dataset into train/validation/test sets
        
        Args:
            examples: Training examples to split
            train_ratio: Ratio for training set
            val_ratio: Ratio for validation set
            test_ratio: Ratio for test set
            shuffle: Whether to shuffle before splitting
            
        Returns:
            Tuple of (train, validation, test) examples
        """
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
            raise ValueError("Ratios must sum to 1.0")
        
        examples_copy = examples.copy()
        if shuffle:
            random.shuffle(examples_copy)
        
        total = len(examples_copy)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        train_set = examples_copy[:train_end]
        val_set = examples_copy[train_end:val_end]
        test_set = examples_copy[val_end:]
        
        return train_set, val_set, test_set
    
    def export_dataset(self,
                      examples: List[TrainingExample],
                      output_path: Union[str, Path],
                      format_type: str = "alpaca") -> bool:
        """
        Export dataset in specified format
        
        Args:
            examples: Training examples to export
            output_path: Output file path
            format_type: Export format ("alpaca", "chatml", "jsonl")
            
        Returns:
            True if successful
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type == "alpaca":
                return self._export_alpaca_format(examples, output_path)
            elif format_type == "chatml":
                return self._export_chatml_format(examples, output_path)
            elif format_type == "jsonl":
                return self._export_jsonl_format(examples, output_path)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
        except Exception as e:
            print(f"Error exporting dataset: {e}")
            return False
    
    def _export_alpaca_format(self, examples: List[TrainingExample], output_path: Path) -> bool:
        """Export in Alpaca format"""
        data = []
        for example in examples:
            record = {
                "instruction": example.instruction,
                "output": example.output
            }
            if example.input:
                record["input"] = example.input
            if example.metadata:
                record.update(example.metadata)
            data.append(record)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def _export_chatml_format(self, examples: List[TrainingExample], output_path: Path) -> bool:
        """Export in ChatML format"""
        data = []
        for example in examples:
            messages = [
                {"role": "system", "content": example.instruction}
            ]
            if example.input:
                messages.append({"role": "user", "content": example.input})
            messages.append({"role": "assistant", "content": example.output})
            
            data.append({"messages": messages})
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def _export_jsonl_format(self, examples: List[TrainingExample], output_path: Path) -> bool:
        """Export in JSONL format"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                record = {
                    "instruction": example.instruction,
                    "output": example.output
                }
                if example.input:
                    record["input"] = example.input
                if example.metadata:
                    record.update(example.metadata)
                
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return True


if __name__ == "__main__":
    # Example usage
    prep = DatasetPreparator()
    
    # Create sample data
    sample_data = [
        {
            "instruction": "Explain machine learning",
            "output": "Machine learning is a method of data analysis that automates analytical model building."
        },
        {
            "instruction": "What is deep learning?",
            "output": "Deep learning is a subset of machine learning that uses neural networks with multiple layers."
        },
        {
            "question": "How does AI work?",
            "answer": "AI works by processing data through algorithms to make decisions or predictions."
        }
    ]
    
    # Create instruction dataset
    instruction_examples = prep.create_instruction_dataset(
        sample_data[:2],
        instruction_field="instruction",
        output_field="output"
    )
    
    # Create QA dataset
    qa_examples = prep.create_qa_dataset(
        sample_data[2:],
        question_field="question",
        answer_field="answer"
    )
    
    # Combine datasets
    all_examples = instruction_examples + qa_examples
    
    # Validate dataset
    report = prep.validate_dataset(all_examples)
    print("Dataset Validation Report:")
    print(f"Total examples: {report['total_examples']}")
    print(f"Quality score: {report['quality_score']:.2f}")
    print(f"Recommendations: {report['recommendations']}")
    
    # Split dataset
    train, val, test = prep.split_dataset(all_examples, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1)
    print(f"\nDataset split: Train={len(train)}, Val={len(val)}, Test={len(test)}")
    
    # Export dataset
    output_file = Path("sample_dataset.json")
    if prep.export_dataset(all_examples, output_file, format_type="alpaca"):
        print(f"Dataset exported to {output_file}")
        
        # Clean up
        output_file.unlink()
        print("Cleaned up sample file")