#!/usr/bin/env python3
"""
Setup Validation Script
=======================

This script validates that the GenerativeAI Starter Kit is properly set up
and that core functionality works as expected.

Author: GenerativeAI-Starter-Kit
License: MIT
"""

import os
import sys
import importlib
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Requires Python 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_required_packages():
    """Check if required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        'torch',
        'transformers', 
        'sentence_transformers',
        'chromadb',
        'langchain',
        'fastapi',
        'uvicorn',
        'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_file_structure():
    """Check if all required files and directories exist"""
    print("\n📁 Checking file structure...")
    
    required_paths = [
        'examples/rag/simple_rag.py',
        'examples/multimodal/image_text_app.py',
        'examples/fine-tuning/text_classification_tuning.py',
        'automation/api_server.py',
        'automation/setup.sh',
        'configs/config.yaml',
        'datasets/sample_data.py',
        'tests/test_rag.py',
        'notebooks/01_rag_introduction.ipynb',
        'docs/en/README.md',
        'docs/zh/README.md',
        'requirements.txt',
        '.gitignore'
    ]
    
    missing_files = []
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - Missing")
            missing_files.append(path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {len(missing_files)}")
        return False
    
    return True

def check_sample_data():
    """Check if sample data was generated correctly"""
    print("\n💾 Checking sample data...")
    
    data_files = [
        'datasets/ai_documents.json',
        'datasets/sentiment_data.json', 
        'datasets/qa_pairs.json',
        'datasets/multimodal_data.json'
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {data_file} ({len(data)} items)")
            except Exception as e:
                print(f"❌ {data_file} - Error loading: {e}")
                return False
        else:
            print(f"❌ {data_file} - Missing")
            return False
    
    return True

def test_basic_imports():
    """Test that core modules can be imported"""
    print("\n🔍 Testing core module imports...")
    
    try:
        from examples.rag.simple_rag import SimpleRAG, RAGConfig
        print("✅ RAG module imports")
    except Exception as e:
        print(f"❌ RAG module import failed: {e}")
        return False
    
    try:
        from examples.multimodal.image_text_app import MultimodalApp
        print("✅ Multimodal module imports")
    except Exception as e:
        print(f"❌ Multimodal module import failed: {e}")
        return False
    
    try:
        from examples.fine_tuning.text_classification_tuning import TextClassificationTrainer
        print("✅ Fine-tuning module imports")
    except Exception as e:
        print(f"❌ Fine-tuning module import failed: {e}")
        return False
    
    return True

def test_config_loading():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration loading...")
    
    try:
        import yaml
        with open('configs/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['models', 'vector_db', 'rag']
        for key in required_keys:
            if key not in config:
                print(f"❌ Missing config key: {key}")
                return False
        
        print("✅ Configuration loads correctly")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def run_quick_functionality_test():
    """Run a quick test of core functionality"""
    print("\n🧪 Running quick functionality test...")
    
    try:
        # Test RAG basic functionality
        from examples.rag.simple_rag import SimpleRAG, RAGConfig
        
        config = RAGConfig(
            chunk_size=100,
            collection_name="validation_test",
            persist_directory="./validation_test_db"
        )
        
        print("  🔍 Testing RAG initialization...")
        rag = SimpleRAG(config)
        rag.initialize()
        
        print("  📝 Testing document addition...")
        test_docs = ["This is a test document about machine learning."]
        rag.add_documents(test_docs)
        
        print("  🔍 Testing search...")
        results = rag.search("machine learning", top_k=1)
        if len(results) > 0:
            print("  ✅ RAG basic functionality works")
        else:
            print("  ❌ RAG search returned no results")
            return False
            
        # Clean up test database
        import shutil
        if os.path.exists("./validation_test_db"):
            shutil.rmtree("./validation_test_db")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False

def main():
    """Main validation function"""
    print("🎯 GenerativeAI Starter Kit Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("File Structure", check_file_structure),
        ("Sample Data", check_sample_data),
        ("Module Imports", test_basic_imports),
        ("Configuration", test_config_loading),
        ("Basic Functionality", run_quick_functionality_test)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready to use.")
        print("\n🚀 Next steps:")
        print("  • Try: python examples/rag/simple_rag.py")
        print("  • Explore: jupyter notebook notebooks/01_rag_introduction.ipynb")
        print("  • Read: docs/en/README.md")
        return True
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
        print("💡 Try running: ./automation/setup.sh")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)