#!/usr/bin/env python3#!/usr/bin/env python3# type: ignore# type: ignore# type: ignore# type: ignore# type: ignore# type: ignore



def demo():# -*- coding: utf-8 -*-

    print("Text Classification Demo")

    print("=" * 30)"""

    

    # Sample data"""

    texts = [

        "I love this product!",Text Classification ExampleText Classification Fine-tuning Example"""

        "This is terrible.",

        "It's okay.",==========================

        "Great quality!",

        "Poor product."Simple text classification demo for GenerativeAI-Starter-Kit======================================

    ]

    """

    labels = ["positive", "negative", "neutral", "positive", "negative"]

    文本分类微调示例"""

    # Simple classification

    def classify(text):def create_sample_data():

        if "love" in text.lower() or "great" in text.lower():

            return "positive"    """Create sample texts and labels"""This example demonstrates text classification using pre-trained models

        elif "terrible" in text.lower() or "poor" in text.lower():

            return "negative"    texts = [

        else:

            return "neutral"        "I love this product! Amazing quality.",Simple rule-based classification for demonstration==============

    

    # Test classification        "This is terrible. Don't buy it.",

    correct = 0

    for text, true_label in zip(texts, labels):        "The item is okay, nothing special.",

        pred = classify(text)

        is_correct = pred == true_label        "Great product, highly recommended!",

        print(f"Text: '{text}' -> True: {true_label}, Pred: {pred} {'✓' if is_correct else '✗'}")

        if is_correct:        "Waste of money. Poor quality."Author: GenerativeAI-Starter-Kit文本分类示例 - 完全无错误版本"""

            correct += 1

        ]

    print(f"\nAccuracy: {correct}/{len(texts)} = {correct/len(texts):.1%}")

    print("Demo completed!")    License: MIT



if __name__ == "__main__":    labels = ["positive", "negative", "neutral", "positive", "negative"]

    demo()
    """这个示例演示如何微调预训练语言模型进行文本分类

    return texts, labels





def simple_classify(text):import os使用BERT类型的模型进行情感分析========================

    """Simple rule-based text classifier"""

    positive_words = ["love", "amazing", "great", "excellent", "recommended"]import json

    negative_words = ["terrible", "waste", "poor", "bad", "awful"]

    from typing import List, Dict, Tuple, Optional

    text_lower = text.lower()

    from dataclasses import dataclass

    pos_score = sum(1 for word in positive_words if word in text_lower)

    neg_score = sum(1 for word in negative_words if word in text_lower)作者: GenerativeAI-Starter-Kit文本分类微调示例 - 零错误简化版本""""""

    

    if pos_score > neg_score:# Optional dependency check

        return "positive"

    elif neg_score > pos_score:try:许可: MIT

        return "negative"

    else:    import torch

        return "neutral"

    import numpy as np"""简化的文本分类演示，避免复杂依赖



def run_demo():    import pandas as pd

    """Run classification demo"""

    print("Text Classification Demo")    from sklearn.model_selection import train_test_split

    print("=" * 40)

        from sklearn.metrics import accuracy_score, classification_report

    texts, true_labels = create_sample_data()

        import os展示文本分类的基本概念和流程==============================

    correct = 0

    total = len(texts)    from transformers import (

    

    for i, (text, true_label) in enumerate(zip(texts, true_labels), 1):        AutoTokenizer,import json

        predicted_label = simple_classify(text)

        is_correct = predicted_label == true_label        AutoModelForSequenceClassification,

        

        print(f"{i}. Text: '{text}'")        TrainingArguments,from typing import List, Dict, Tuple, Optional

        print(f"   True: {true_label}")

        print(f"   Predicted: {predicted_label}")        Trainer,

        print(f"   Result: {'✓ Correct' if is_correct else '✗ Incorrect'}")

        print()        DataCollatorWithPadding,from dataclasses import dataclass

        

        if is_correct:    )

            correct += 1

        作者: GenerativeAI-Starter-Kit文本分类微调示例 - 零错误版本文本分类微调示例 - 零错误版本

    accuracy = correct / total

    print(f"Final Results:")    from datasets import Dataset

    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")

    print("Demo completed successfully!")    import matplotlib.pyplot as plt# 可选依赖检查



    DEPENDENCIES_AVAILABLE = True

if __name__ == "__main__":

    run_demo()except ImportError:try:"""

    print("Warning: Some dependencies not installed, running simplified version")

    DEPENDENCIES_AVAILABLE = False    import torch



    import numpy as np这个示例演示文本分类的基本概念和流程

@dataclass

class FineTuningConfig:    import pandas as pd

    """Fine-tuning configuration class"""

    model_name: str = "distilbert-base-uncased"    from sklearn.model_selection import train_test_splitfrom typing import List, Dict, Tuple

    num_labels: int = 2

    max_length: int = 512    from sklearn.metrics import accuracy_score, classification_report

    batch_size: int = 16

    learning_rate: float = 2e-5    使用简化的方法避免复杂的依赖问题==================================================

    num_epochs: int = 3

    warmup_steps: int = 500    from transformers import (

    weight_decay: float = 0.01

    output_dir: str = "./fine_tuned_models"        AutoTokenizer,

    save_steps: int = 500

    eval_steps: int = 500        AutoModelForSequenceClassification,

    logging_steps: int = 100

        TrainingArguments,def create_sample_data() -> Tuple[List[str], List[str]]:



def create_sample_data() -> Tuple[List[str], List[str]]:        Trainer,

    """Create sample data for demonstration"""

    texts = [        DataCollatorWithPadding,    """创建示例数据"""

        "I love this product! It's amazing.",

        "This is terrible, don't recommend it.",    )

        "The product is okay, nothing special.",

        "Great quality, worth buying!",        texts = [作者: GenerativeAI-Starter-Kit

        "Completely useless, waste of money."

    ]    from datasets import Dataset

    

    labels = ["positive", "negative", "neutral", "positive", "negative"]    import matplotlib.pyplot as plt        "我喜欢这个产品！非常棒。",

    

    return texts, labels    DEPENDENCIES_AVAILABLE = True



except ImportError:        "这东西很糟糕，不推荐。",许可: MIT

def simple_classify(text: str) -> str:

    """Simple rule-based classifier"""    print("⚠️ 部分依赖未安装，将运行简化版本")

    positive_words = ["love", "amazing", "great", "worth", "excellent"]

    negative_words = ["terrible", "useless", "waste", "bad", "awful"]    DEPENDENCIES_AVAILABLE = False        "产品还可以，一般般。",

    

    text_lower = text.lower()

    pos_count = sum(1 for word in positive_words if word in text_lower)

    neg_count = sum(1 for word in negative_words if word in text_lower)        "质量很好，值得购买！","""这个示例演示如何微调预训练语言模型进行文本分类这个示例演示如何微调预训练语言模型进行文本分类

    

    if pos_count > neg_count:@dataclass

        return "positive"

    elif neg_count > pos_count:class FineTuningConfig:        "完全没用，浪费钱。"

        return "negative"

    else:    """微调配置类"""

        return "neutral"

    model_name: str = "distilbert-base-uncased"    ]



def demo_classification():    num_labels: int = 2

    """Demonstrate classification process"""

    print("Text Classification Demo")    max_length: int = 512    

    print("=" * 30)

        batch_size: int = 16

    texts, labels = create_sample_data()

        learning_rate: float = 2e-5    labels = ["positive", "negative", "neutral", "positive", "negative"]import os使用BERT类型的模型进行情感分析或自定义分类任务使用BERT类型的模型进行情感分析或自定义分类任务

    print(f"Data: {len(texts)} samples")

    print()    num_epochs: int = 3

    

    correct = 0    warmup_steps: int = 500    

    for text, true_label in zip(texts, labels):

        pred_label = simple_classify(text)    weight_decay: float = 0.01

        is_correct = pred_label == true_label

            output_dir: str = "./fine_tuned_models"    return texts, labelsimport json

        print(f"Text: '{text}'")

        print(f"True: {true_label} | Predicted: {pred_label} {'✓' if is_correct else '✗'}")    save_steps: int = 500

        print()

            eval_steps: int = 500

        if is_correct:

            correct += 1    logging_steps: int = 100

    

    accuracy = correct / len(texts)from typing import List, Dict, Tuple, Optional

    print(f"Accuracy: {accuracy:.3f} ({correct}/{len(texts)})")

    print("Demo completed!")



def create_sample_data() -> Tuple[List[str], List[str]]:def simple_classify(text: str) -> str:

if DEPENDENCIES_AVAILABLE:

    class TextClassificationTrainer:    """创建示例数据"""

        """Text classification fine-tuner"""

            texts = [    """简单的基于规则的分类"""

        def __init__(self, config: Optional[FineTuningConfig] = None):

            self.config = config or FineTuningConfig()        "我喜欢这个产品！非常棒。",

            self.tokenizer = None

            self.model = None        "这东西很糟糕，不推荐。",    positive_words = ["喜欢", "棒", "好", "推荐", "值得"]

            self.trainer = None

            self.label_to_id = {}        "产品还可以，一般般。",

            self.id_to_label = {}

                "质量很好，值得购买！",    negative_words = ["糟糕", "没用", "浪费", "不推荐"]作者: GenerativeAI-Starter-Kit作者: GenerativeAI-Starter-Kit

        def initialize(self):

            """Initialize tokenizer and model"""        "完全没用，浪费钱。"

            print("Initializing fine-tuning setup...")

                ]    

            # Load tokenizer

            print(f"Loading tokenizer: {self.config.model_name}")    

            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)

                labels = ["positive", "negative", "neutral", "positive", "negative"]    pos_count = sum(1 for word in positive_words if word in text)def create_sample_data() -> Tuple[List[str], List[str]]:

            # Load model

            print(f"Loading model: {self.config.model_name}")    

            self.model = AutoModelForSequenceClassification.from_pretrained(

                self.config.model_name,     return texts, labels    neg_count = sum(1 for word in negative_words if word in text)

                num_labels=self.config.num_labels

            )

            

            print("Initialization complete")        """创建示例数据用于演示"""许可: MIT许可: MIT

        

        def predict(self, texts: List[str]) -> List[Dict]:def simple_classify(text: str) -> str:

            """Make predictions on new texts"""

            if not self.model or not self.tokenizer:    """简单的基于规则的分类"""    if pos_count > neg_count:

                raise ValueError("Model not initialized")

                positive_words = ["喜欢", "棒", "好", "推荐", "值得"]

            predictions = []

                negative_words = ["糟糕", "没用", "浪费", "不推荐"]        return "positive"    texts = [

            for text in texts:

                # Tokenize    

                inputs = self.tokenizer(

                    text,    pos_count = sum(1 for word in positive_words if word in text)    elif neg_count > pos_count:

                    return_tensors="pt",

                    truncation=True,    neg_count = sum(1 for word in negative_words if word in text)

                    padding=True,

                    max_length=self.config.max_length,            return "negative"        "我喜欢这个产品！非常棒，效果很好。",""""""

                )

                    if pos_count > neg_count:

                # Predict

                with torch.no_grad():        return "positive"    else:

                    outputs = self.model(**inputs)

                    logits = outputs.logits    elif neg_count > pos_count:

                    probabilities = torch.nn.functional.softmax(logits, dim=-1)

                    predicted_class = torch.argmax(logits, dim=-1).item()        return "negative"        return "neutral"        "这是我买过最糟糕的东西。完全没用。",

                

                # Format result    else:

                result = {

                    "text": text,        return "neutral"

                    "predicted_label": self.id_to_label[predicted_class],

                    "confidence": probabilities[0][predicted_class].item()

                }

                        "产品还可以，没什么特别但能用。",

                predictions.append(result)

            def demo_classification():

            return predictions

    """演示分类过程"""def demo_classification():



def main():    print("🎯 文本分类演示")

    """Main function"""

    if DEPENDENCIES_AVAILABLE:    print("=" * 30)    """演示分类过程"""        "质量很好，客服也不错。强烈推荐！",

        print("Full version available - includes deep learning features")

        demo_classification()    

        print("\nTip: Use TextClassificationTrainer for advanced fine-tuning")

    else:    texts, labels = create_sample_data()    print("🎯 文本分类演示")

        print("Simplified version - rule-based classification")

        demo_classification()    

        print("\nInstall dependencies for full functionality:")

        print("pip install torch transformers datasets pandas scikit-learn")    print(f"📊 数据: {len(texts)} 个样本")    print("=" * 30)        "糟糕的体验。产品用了一天就坏了。",import osimport os



    print()

if __name__ == "__main__":

    main()        

    correct = 0

    for text, true_label in zip(texts, labels):    texts, labels = create_sample_data()        "性价比不错。会再次购买。",

        pred_label = simple_classify(text)

        is_correct = pred_label == true_label    

        

        print(f"文本: '{text}'")    print(f"📊 数据: {len(texts)} 个样本")        "不值这个价格。很失望。",import jsonimport json

        print(f"真实: {true_label} | 预测: {pred_label} {'✓' if is_correct else '✗'}")

        print()    print()

        

        if is_correct:            "质量优秀，发货很快。",

            correct += 1

        correct = 0

    accuracy = correct / len(texts)

    print(f"📈 准确率: {accuracy:.3f} ({correct}/{len(texts)})")    for text, true_label in zip(texts, labels):        "产品不错但还有改进空间。",from typing import List, Dict, Tuple, Optionalfrom typing import List, Dict, Tuple, Optional

    print("✅ 演示完成!")

        pred_label = simple_classify(text)



if DEPENDENCIES_AVAILABLE:        is_correct = pred_label == true_label        "太棒了！超出了我的期望。"

    class TextClassificationTrainer:

        """文本分类微调器"""        

        

        def __init__(self, config: Optional[FineTuningConfig] = None):        print(f"文本: '{text}'")    ]from dataclasses import dataclassfrom dataclasses import dataclass

            self.config = config or FineTuningConfig()

            self.tokenizer = None        print(f"真实: {true_label} | 预测: {pred_label} {'✓' if is_correct else '✗'}")

            self.model = None

            self.trainer = None        print()

            self.label_to_id = {}

            self.id_to_label = {}        

        

        def initialize(self):        if is_correct:    labels = [

            """初始化分词器和模型"""

            print("🚀 初始化微调设置...")            correct += 1

            

            # 加载分词器            "positive",

            print(f"📖 加载分词器: {self.config.model_name}")

            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)    accuracy = correct / len(texts)

            

            # 加载模型    print(f"📈 准确率: {accuracy:.3f} ({correct}/{len(texts)})")        "negative", # 注意：以下依赖需要单独安装# 注意：以下依赖需要单独安装

            print(f"🧠 加载模型: {self.config.model_name}")

            self.model = AutoModelForSequenceClassification.from_pretrained(    print("✅ 演示完成!")

                self.config.model_name, 

                num_labels=self.config.num_labels        "neutral",

            )

            

            print("✅ 初始化完成")

        if __name__ == "__main__":        "positive",# pip install torch transformers datasets pandas scikit-learn matplotlib seaborn# pip install torch transformers datasets pandas scikit-learn matplotlib seaborn

        def predict(self, texts: List[str]) -> List[Dict]:

            """对新文本进行预测"""    demo_classification()

            if not self.model or not self.tokenizer:        "negative",

                raise ValueError("模型未初始化")

                    "positive",

            predictions = []

                    "negative",

            for text in texts:

                # 分词        "positive",try:try:

                inputs = self.tokenizer(

                    text,        "neutral", 

                    return_tensors="pt",

                    truncation=True,        "positive"    import torch    import torch

                    padding=True,

                    max_length=self.config.max_length,    ]

                )

                    import numpy as np    import numpy as np

                # 预测

                with torch.no_grad():    return texts, labels

                    outputs = self.model(**inputs)

                    logits = outputs.logits    import pandas as pd    import pandas as pd

                    probabilities = torch.nn.functional.softmax(logits, dim=-1)

                    predicted_class = torch.argmax(logits, dim=-1).item()

                

                # 格式化结果def analyze_data(texts: List[str], labels: List[str]) -> Dict:    from sklearn.model_selection import train_test_split    from sklearn.model_selection import train_test_split

                result = {

                    "text": text,    """分析数据的基本统计"""

                    "predicted_label": self.id_to_label[predicted_class],

                    "confidence": probabilities[0][predicted_class].item()    # 统计标签分布    from sklearn.metrics import accuracy_score, classification_report    from sklearn.metrics import accuracy_score, classification_report

                }

                    label_counts = {}

                predictions.append(result)

                for label in labels:        

            return predictions

        label_counts[label] = label_counts.get(label, 0) + 1



def main():        from transformers import (    from transformers import (

    """主函数"""

    if DEPENDENCIES_AVAILABLE:    # 统计文本长度

        print("🚀 完整版本可用 - 包含深度学习功能")

        demo_classification()    text_lengths = [len(text) for text in texts]        AutoTokenizer,        AutoTokenizer,

        print("\n💡 提示: 可以使用 TextClassificationTrainer 进行高级微调")

    else:    avg_length = sum(text_lengths) / len(text_lengths)

        print("📝 简化版本 - 基于规则的分类")

        demo_classification()            AutoModelForSequenceClassification,        AutoModelForSequenceClassification,

        print("\n💡 安装依赖以使用完整功能:")

        print("pip install torch transformers datasets pandas scikit-learn")    return {



        "total_samples": len(texts),        TrainingArguments,        TrainingArguments,

if __name__ == "__main__":

    main()        "label_distribution": label_counts,

        "average_text_length": avg_length,        Trainer,        Trainer,

        "min_length": min(text_lengths),

        "max_length": max(text_lengths)        DataCollatorWithPadding,        DataCollatorWithPadding,

    }

    )    )



def simple_word_features(text: str) -> Dict[str, int]:        

    """提取简单的词汇特征"""

    # 情感词汇    from datasets import Dataset    from datasets import Dataset

    positive_words = ["喜欢", "棒", "好", "推荐", "优秀", "快", "满意", "不错"]

    negative_words = ["糟糕", "没用", "失望", "差", "坏", "浪费"]    import matplotlib.pyplot as plt    import matplotlib.pyplot as plt

    neutral_words = ["还可以", "还行", "一般", "普通"]

        DEPENDENCIES_AVAILABLE = True    DEPENDENCIES_AVAILABLE = True

    text_lower = text.lower()

    except ImportError as e:except ImportError as e:

    features = {

        "positive_count": sum(1 for word in positive_words if word in text_lower),    print(f"⚠️ 缺少依赖包: {e}")    print(f"⚠️ 缺少依赖包: {e}")

        "negative_count": sum(1 for word in negative_words if word in text_lower),

        "neutral_count": sum(1 for word in neutral_words if word in text_lower),    print("请运行: pip install torch transformers datasets pandas scikit-learn matplotlib seaborn")    print("请运行: pip install torch transformers datasets pandas scikit-learn matplotlib seaborn")

        "text_length": len(text),

        "exclamation_count": text.count("!"),    DEPENDENCIES_AVAILABLE = False    DEPENDENCIES_AVAILABLE = False

        "question_count": text.count("?")

    }

    

    return features



@dataclass@dataclass

def simple_classify(text: str) -> Dict[str, any]:

    """简单的基于规则的分类器"""class FineTuningConfig:class FineTuningConfig:

    features = simple_word_features(text)

        """微调配置类"""    """微调配置类"""

    # 简单的分类逻辑

    positive_score = features["positive_count"] + features["exclamation_count"] * 0.5    model_name: str = "distilbert-base-uncased"    model_name: str = "distilbert-base-uncased"

    negative_score = features["negative_count"]

    neutral_score = features["neutral_count"]    num_labels: int = 2    num_labels: int = 2

    

    scores = {    max_length: int = 512    max_length: int = 512

        "positive": positive_score,

        "negative": negative_score,    batch_size: int = 16    batch_size: int = 16

        "neutral": neutral_score

    }    learning_rate: float = 2e-5    learning_rate: float = 2e-5

    

    # 选择最高分的标签    num_epochs: int = 3    num_epochs: int = 3

    predicted_label = max(scores, key=scores.get)

        warmup_steps: int = 500    warmup_steps: int = 500

    # 如果所有分数都是0，默认为neutral

    if all(score == 0 for score in scores.values()):    weight_decay: float = 0.01    weight_decay: float = 0.01

        predicted_label = "neutral"

        output_dir: str = "./fine_tuned_models"    output_dir: str = "./fine_tuned_models"

    return {

        "text": text,    save_steps: int = 500    save_steps: int = 500

        "predicted_label": predicted_label,

        "scores": scores,    eval_steps: int = 500    eval_steps: int = 500

        "features": features

    }    logging_steps: int = 100    logging_steps: int = 100





def evaluate_simple_classifier(texts: List[str], true_labels: List[str]) -> Dict:

    """评估简单分类器的性能"""

    predictions = []

    correct = 0class TextClassificationTrainer:class TextClassificationTrainer:

    

    for text, true_label in zip(texts, true_labels):    """文本分类微调器"""    """文本分类微调器"""

        result = simple_classify(text)

        predictions.append(result)        

        

        if result["predicted_label"] == true_label:    def __init__(self, config: Optional[FineTuningConfig] = None):    def __init__(self, config: Optional[FineTuningConfig] = None):

            correct += 1

            self.config = config or FineTuningConfig()        self.config = config or FineTuningConfig()

    accuracy = correct / len(texts)

            self.tokenizer = None        self.tokenizer = None

    return {

        "accuracy": accuracy,        self.model = None        self.model = None

        "correct_predictions": correct,

        "total_predictions": len(texts),        self.trainer = None        self.trainer = None

        "predictions": predictions

    }        self.label_to_id = {}        self.label_to_id = {}



        self.id_to_label = {}        self.id_to_label = {}

def demo_text_classification():

    """演示文本分类过程"""        

    print("🎯 文本分类演示")

    print("=" * 40)    def check_dependencies(self) -> bool:    def check_dependencies(self) -> bool:

    

    # 创建示例数据        """检查依赖是否可用"""        """检查依赖是否可用"""

    texts, labels = create_sample_data()

    print(f"📊 创建了 {len(texts)} 个示例文本")        return DEPENDENCIES_AVAILABLE        return DEPENDENCIES_AVAILABLE

    

    # 分析数据        

    stats = analyze_data(texts, labels)

    print(f"\n📈 数据统计:")    def initialize(self):    def initialize(self):

    print(f"  总样本数: {stats['total_samples']}")

    print(f"  平均文本长度: {stats['average_text_length']:.1f} 字符")        """初始化分词器和模型"""        """初始化分词器和模型"""

    print(f"  标签分布:")

    for label, count in stats['label_distribution'].items():        if not self.check_dependencies():        if not self.check_dependencies():

        print(f"    {label}: {count} 个")

                raise ImportError("缺少必要的依赖包，请先安装")            raise ImportError("缺少必要的依赖包，请先安装")

    # 演示特征提取

    print(f"\n🔍 特征提取演示:")                

    example_text = texts[0]

    features = simple_word_features(example_text)        print("🚀 初始化微调设置...")        print("🚀 初始化微调设置...")

    print(f"  示例文本: '{example_text}'")

    print(f"  提取的特征: {features}")                

    

    # 演示分类        # 加载分词器        # 加载分词器

    print(f"\n🔮 分类演示:")

    for i in range(min(3, len(texts))):        print(f"📖 加载分词器: {self.config.model_name}")        print(f"📖 加载分词器: {self.config.model_name}")

        result = simple_classify(texts[i])

        print(f"  文本: '{result['text']}'")        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)

        print(f"  真实标签: {labels[i]}")

        print(f"  预测标签: {result['predicted_label']}")                

        print(f"  分数: {result['scores']}")

        print()        # 加载模型        # 加载模型

    

    # 评估性能        print(f"🧠 加载模型: {self.config.model_name}")        print(f"🧠 加载模型: {self.config.model_name}")

    print(f"📊 整体性能评估:")

    evaluation = evaluate_simple_classifier(texts, labels)        self.model = AutoModelForSequenceClassification.from_pretrained(        self.model = AutoModelForSequenceClassification.from_pretrained(

    print(f"  准确率: {evaluation['accuracy']:.3f}")

    print(f"  正确预测: {evaluation['correct_predictions']}/{evaluation['total_predictions']}")            self.config.model_name,             self.config.model_name, 

    

    print(f"\n✅ 演示完成!")            num_labels=self.config.num_labels            num_labels=self.config.num_labels

    print(f"💡 这是一个简化的文本分类示例")

    print(f"   实际应用中会使用更复杂的机器学习模型")        )        )



                

def show_ml_pipeline_info():

    """显示机器学习流水线信息"""        print("✅ 初始化完成")        print("✅ 初始化完成")

    print(f"\n🚀 机器学习文本分类流水线:")

    print(f"=" * 50)        

    

    pipeline_steps = [    def prepare_data(self, texts: List[str], labels: List[str], test_size: float = 0.2) -> Tuple[Dataset, Dataset]:    def prepare_data(self, texts: List[str], labels: List[str], test_size: float = 0.2) -> Tuple[Dataset, Dataset]:

        ("1. 数据收集", "收集带标签的文本数据"),

        ("2. 数据预处理", "清洗、分词、去除停用词"),        """准备和分词数据用于训练"""        """准备和分词数据用于训练"""

        ("3. 特征工程", "TF-IDF、词嵌入、BERT等"),

        ("4. 模型选择", "朴素贝叶斯、SVM、神经网络"),        print("📊 准备训练数据...")        print("📊 准备训练数据...")

        ("5. 模型训练", "使用训练数据训练模型"),

        ("6. 模型评估", "使用验证集评估性能"),                

        ("7. 超参数调优", "网格搜索、随机搜索"),

        ("8. 模型部署", "将模型部署到生产环境")        # 创建标签映射        # 创建标签映射

    ]

            unique_labels = list(set(labels))        unique_labels = list(set(labels))

    for step, description in pipeline_steps:

        print(f"{step}: {description}")        self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}        self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}

    

    print(f"\n🔧 常用工具和库:")        self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}        self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}

    tools = [

        "scikit-learn: 传统机器学习算法",                

        "transformers: 预训练语言模型",

        "torch/tensorflow: 深度学习框架",        print(f"标签: {self.label_to_id}")        print(f"标签: {self.label_to_id}")

        "pandas: 数据处理",

        "nltk/spacy: 自然语言处理"                

    ]

            # 将字符串标签转换为数字        # 转换字符串标签为数字

    for tool in tools:

        print(f"  • {tool}")        numeric_labels = [self.label_to_id[label] for label in labels]        numeric_labels = [self.label_to_id[label] for label in labels]



                

if __name__ == "__main__":

    demo_text_classification()        # 分割数据        # 分割数据

    show_ml_pipeline_info()
        train_texts, val_texts, train_labels, val_labels = train_test_split(        train_texts, val_texts, train_labels, val_labels = train_test_split(

            texts, numeric_labels, test_size=test_size, random_state=42, stratify=numeric_labels            texts, numeric_labels, test_size=test_size, random_state=42, stratify=numeric_labels

        )        )

                

        print(f"训练样本: {len(train_texts)}")        print(f"训练样本: {len(train_texts)}")

        print(f"验证样本: {len(val_texts)}")        print(f"验证样本: {len(val_texts)}")

                

        # 分词函数        # 分词函数

        def tokenize_function(examples):        def tokenize_function(examples):

            return self.tokenizer(            return self.tokenizer(

                examples["text"],                examples["text"],

                truncation=True,                truncation=True,

                padding=True,                padding=True,

                max_length=self.config.max_length,                max_length=self.config.max_length,

            )            )

                

        # 创建数据集        # 创建数据集

        train_dataset = Dataset.from_dict({"text": train_texts, "labels": train_labels})        train_dataset = Dataset.from_dict({"text": train_texts, "labels": train_labels})

        val_dataset = Dataset.from_dict({"text": val_texts, "labels": val_labels})        val_dataset = Dataset.from_dict({"text": val_texts, "labels": val_labels})

                

        # 分词        # 分词

        train_dataset = train_dataset.map(tokenize_function, batched=True)        train_dataset = train_dataset.map(tokenize_function, batched=True)

        val_dataset = val_dataset.map(tokenize_function, batched=True)        val_dataset = val_dataset.map(tokenize_function, batched=True)

                

        return train_dataset, val_dataset        return train_dataset, val_dataset

        

    def compute_metrics(self, eval_pred):    def compute_metrics(self, eval_pred):

        """计算评估指标"""        """计算评估指标"""

        predictions, labels = eval_pred        predictions, labels = eval_pred

        predictions = np.argmax(predictions, axis=1)        predictions = np.argmax(predictions, axis=1)

        accuracy = accuracy_score(labels, predictions)        accuracy = accuracy_score(labels, predictions)

        return {"accuracy": accuracy}        return {"accuracy": accuracy}

        

    def train(self, train_dataset: Dataset, val_dataset: Dataset):    def train(self, train_dataset: Dataset, val_dataset: Dataset):

        """训练模型"""        """训练模型"""

        print("🏋️ 开始模型训练...")        print("🏋️ 开始模型训练...")

                

        # 训练参数        # 训练参数

        training_args = TrainingArguments(        training_args = TrainingArguments(

            output_dir=self.config.output_dir,            output_dir=self.config.output_dir,

            num_train_epochs=self.config.num_epochs,            num_train_epochs=self.config.num_epochs,

            per_device_train_batch_size=self.config.batch_size,            per_device_train_batch_size=self.config.batch_size,

            per_device_eval_batch_size=self.config.batch_size,            per_device_eval_batch_size=self.config.batch_size,

            warmup_steps=self.config.warmup_steps,            warmup_steps=self.config.warmup_steps,

            weight_decay=self.config.weight_decay,            weight_decay=self.config.weight_decay,

            logging_dir=f"{self.config.output_dir}/logs",            logging_dir=f"{self.config.output_dir}/logs",

            logging_steps=self.config.logging_steps,            logging_steps=self.config.logging_steps,

            evaluation_strategy="steps",            evaluation_strategy="steps",

            eval_steps=self.config.eval_steps,            eval_steps=self.config.eval_steps,

            save_steps=self.config.save_steps,            save_steps=self.config.save_steps,

            load_best_model_at_end=True,            load_best_model_at_end=True,

            metric_for_best_model="accuracy",            metric_for_best_model="accuracy",

            greater_is_better=True,            greater_is_better=True,

            report_to="none",  # 禁用wandb/tensorboard            report_to="none",

        )        )

                

        # 数据整理器        # 数据整理器

        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)

                

        # 初始化训练器        # 初始化训练器

        self.trainer = Trainer(        self.trainer = Trainer(

            model=self.model,            model=self.model,

            args=training_args,            args=training_args,

            train_dataset=train_dataset,            train_dataset=train_dataset,

            eval_dataset=val_dataset,            eval_dataset=val_dataset,

            tokenizer=self.tokenizer,            tokenizer=self.tokenizer,

            data_collator=data_collator,            data_collator=data_collator,

            compute_metrics=self.compute_metrics,            compute_metrics=self.compute_metrics,

        )        )

                

        # 训练        # 训练

        train_result = self.trainer.train()        train_result = self.trainer.train()

                

        # 保存模型        # 保存模型

        self.trainer.save_model()        self.trainer.save_model()

                

        print("✅ 训练完成!")        print("✅ 训练完成!")

        print(f"训练损失: {train_result.training_loss:.4f}")        print(f"训练损失: {train_result.training_loss:.4f}")

                

        return train_result        return train_result

        

    def evaluate(self, test_dataset: Dataset) -> Dict:    def predict(self, texts: List[str]) -> List[Dict]:

        """评估模型"""        """对新文本进行预测"""

        if not self.trainer:        if not self.model or not self.tokenizer:

            raise ValueError("模型尚未训练。请先调用 train() 方法。")            raise ValueError("模型未初始化，请先调用 initialize()")

                

        print("📊 评估模型...")        predictions = []

        eval_result = self.trainer.evaluate(test_dataset)        

                for text in texts:

        print(f"评估准确率: {eval_result['eval_accuracy']:.4f}")            # 分词

                    inputs = self.tokenizer(

        return eval_result                text,

                    return_tensors="pt",

    def predict(self, texts: List[str]) -> List[Dict]:                truncation=True,

        """对新文本进行预测"""                padding=True,

        if not self.model or not self.tokenizer:                max_length=self.config.max_length,

            raise ValueError("模型未初始化。请先调用 initialize() 方法。")            )

                    

        predictions = []            # 预测

                    with torch.no_grad():

        for text in texts:                outputs = self.model(**inputs)

            # 分词                logits = outputs.logits

            inputs = self.tokenizer(                probabilities = torch.nn.functional.softmax(logits, dim=-1)

                text,                predicted_class = torch.argmax(logits, dim=-1).item()

                return_tensors="pt",            

                truncation=True,            # 格式化结果

                padding=True,            result = {

                max_length=self.config.max_length,                "text": text,

            )                "predicted_label": self.id_to_label[predicted_class],

                            "confidence": probabilities[0][predicted_class].item(),

            # 预测                "all_probabilities": {

            with torch.no_grad():                    self.id_to_label[i]: prob.item()

                outputs = self.model(**inputs)                    for i, prob in enumerate(probabilities[0])

                logits = outputs.logits                },

                probabilities = torch.nn.functional.softmax(logits, dim=-1)            }

                predicted_class = torch.argmax(logits, dim=-1).item()            

                        predictions.append(result)

            # 格式化结果        

            result = {        return predictions

                "text": text,

                "predicted_label": self.id_to_label[predicted_class],

                "confidence": probabilities[0][predicted_class].item(),def create_sample_data() -> Tuple[List[str], List[str]]:

                "all_probabilities": {    """创建示例数据用于演示"""

                    self.id_to_label[i]: prob.item()    texts = [

                    for i, prob in enumerate(probabilities[0])        "我喜欢这个产品! 它很棒并且工作完美。",

                },        "这是我买过最糟糕的东西。完全没用。",

            }        "产品还可以，没什么特别的但能完成工作。",

                    "优秀的质量和很棒的客户服务。强烈推荐!",

            predictions.append(result)        "糟糕的体验。产品一天就坏了。",

                "物有所值。会再次购买。",

        return predictions        "不值这个价格。非常失望。",

            "出色的构建质量和快速发货。",

    def save_model(self, path: str):        "产品不错但可以更好。",

        """保存训练好的模型"""        "杰出的！完全超出我的期望。"

        if not self.model or not self.tokenizer:    ]

            raise ValueError("模型尚未训练。")    

            labels = [

        os.makedirs(path, exist_ok=True)        "positive", "negative", "neutral", "positive", "negative",

                "positive", "negative", "positive", "neutral", "positive"

        # 保存模型和分词器    ]

        self.model.save_pretrained(path)    

        self.tokenizer.save_pretrained(path)    return texts, labels

        

        # 保存标签映射

        with open(os.path.join(path, "label_mappings.json"), "w") as f:def demo_fine_tuning():

            json.dump(    """演示微调过程"""

                {"label_to_id": self.label_to_id, "id_to_label": self.id_to_label},    print("🎯 文本分类微调演示")

                f,    print("=" * 50)

                indent=2,    

            )    # 检查依赖

            if not DEPENDENCIES_AVAILABLE:

        print(f"✅ 模型已保存到 {path}")        print("❌ 缺少必要的依赖包")

            print("请运行: pip install torch transformers datasets pandas scikit-learn matplotlib")

    def load_model(self, path: str):        print("\n💡 使用简化版本演示代替:")

        """加载训练好的模型"""        print("python examples/fine-tuning/text_classification_demo.py")

        print(f"📖 从 {path} 加载模型")        return

            

        # 加载模型和分词器    # 创建示例数据

        self.model = AutoModelForSequenceClassification.from_pretrained(path)    texts, labels = create_sample_data()

        self.tokenizer = AutoTokenizer.from_pretrained(path)    print(f"📊 创建了 {len(texts)} 个示例文本，{len(set(labels))} 个类别")

            

        # 加载标签映射    # 初始化训练器

        with open(os.path.join(path, "label_mappings.json"), "r") as f:    config = FineTuningConfig(

            mappings = json.load(f)        num_labels=len(set(labels)),

            self.label_to_id = mappings["label_to_id"]        num_epochs=2,  # 演示用减少

            self.id_to_label = {int(k): v for k, v in mappings["id_to_label"].items()}        batch_size=8,  # 演示用减少

            )

        print("✅ 模型加载成功")    

    trainer = TextClassificationTrainer(config)

    

def create_sample_data() -> Tuple[List[str], List[str]]:    try:

    """创建示例数据用于演示"""        trainer.initialize()

    texts = [        

        "我喜欢这个产品！非常棒，效果很好。",        # 准备数据

        "这是我买过最糟糕的东西。完全没用。",        train_dataset, val_dataset = trainer.prepare_data(texts, labels)

        "产品还可以，没什么特别但能用。",        

        "质量很好，客服也不错。强烈推荐！",        # 训练模型

        "糟糕的体验。产品用了一天就坏了。",        print("\n🏋️ 训练模型 (这可能需要几分钟)...")

        "性价比不错。会再次购买。",        train_result = trainer.train(train_dataset, val_dataset)

        "不值这个价格。很失望。",        

        "质量优秀，发货很快。",        # 测试预测

        "产品不错但还有改进空间。",        test_texts = [

        "太棒了！超出了我的期望。",            "这是一个令人惊叹的产品!",

        "材料质量差，设计也不好。",            "我讨厌这个东西。",

        "还行，有改进的余地。",            "还可以吧，我想。",

        "功能很棒，界面友好。",        ]

        "浪费钱。不要买这个。",        

        "可靠的产品，性能不错。",        print("\n🔮 测试预测:")

        "绝对喜欢！最好的购买决定。",        predictions = trainer.predict(test_texts)

        "没有印象深刻。期望更好的。",        

        "价格合理的好产品。",        for pred in predictions:

        "质量糟糕，支持也不好。",            print(f"文本: '{pred['text']}'")

        "完美符合我的需求。非常满意。",            print(f"预测: {pred['predicted_label']} (置信度: {pred['confidence']:.3f})")

    ]            print()

        

    labels = [        print("✅ 演示成功完成!")

        "positive",        

        "negative",     except Exception as e:

        "neutral",        print(f"❌ 训练失败: {e}")

        "positive",        print("这可能是由于资源限制。尝试减少 batch_size 或 num_epochs。")

        "negative",

        "positive",

        "negative",if __name__ == "__main__":

        "positive",    demo_fine_tuning()
        "neutral", 
        "positive",
        "negative",
        "neutral",
        "positive",
        "negative",
        "positive",
        "positive",
        "negative",
        "positive", 
        "negative",
        "positive",
    ]

    return texts, labels


def demo_fine_tuning():
    """演示微调过程"""
    print("🎯 文本分类微调演示")
    print("=" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("❌ 缺少必要依赖，无法运行演示")
        print("请运行: pip install torch transformers datasets pandas scikit-learn matplotlib seaborn")
        return
    
    # 创建示例数据
    texts, labels = create_sample_data()
    print(f"📊 创建了 {len(texts)} 个示例文本，包含 {len(set(labels))} 个类别")
    
    # 初始化训练器
    config = FineTuningConfig(
        num_labels=len(set(labels)),
        num_epochs=2,  # 演示用，减少轮数
        batch_size=8,  # 演示用，减少批次大小
    )
    
    trainer = TextClassificationTrainer(config)
    trainer.initialize()
    
    # 准备数据
    train_dataset, val_dataset = trainer.prepare_data(texts, labels)
    
    # 训练模型
    print("\n🏋️ 训练模型（可能需要几分钟）...")
    try:
        train_result = trainer.train(train_dataset, val_dataset)
        
        # 评估
        eval_result = trainer.evaluate(val_dataset)
        
        # 测试预测
        test_texts = [
            "这个产品真的很棒！",
            "我讨厌这个东西。",
            "还可以吧，我觉得。",
        ]
        
        print("\n🔮 测试预测:")
        predictions = trainer.predict(test_texts)
        
        for pred in predictions:
            print(f"文本: '{pred['text']}'")
            print(f"预测: {pred['predicted_label']} (置信度: {pred['confidence']:.3f})")
            print()
        
        # 保存模型
        save_path = "./demo_model"
        trainer.save_model(save_path)
        
        print("✅ 演示完成!")
        
    except Exception as e:
        print(f"❌ 训练失败: {e}")
        print("这可能是由于资源限制。尝试减少 batch_size 或 num_epochs。")


def simple_demo():
    """简化演示版本（无需训练）"""
    print("🎯 文本分类简单演示")
    print("=" * 30)
    
    # 创建示例数据
    texts, labels = create_sample_data()
    print(f"📊 示例数据: {len(texts)} 个文本，{len(set(labels))} 个类别")
    
    # 显示数据分布
    label_counts = {}
    for label in labels:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    print("📈 标签分布:")
    for label, count in label_counts.items():
        print(f"  {label}: {count} 个样本")
    
    print("\n✅ 演示完成! 如需完整训练，请安装依赖并运行 demo_fine_tuning()")


if __name__ == "__main__":
    if DEPENDENCIES_AVAILABLE:
        demo_fine_tuning()
    else:
        simple_demo()