#!/usr/bin/env python3
"""
Automated installation script for GenerativeAI Starter Kit

This script:
1. Checks system requirements
2. Creates virtual environment
3. Installs Python dependencies
4. Sets up configuration files
5. Downloads sample data
6. Validates installation
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil
import urllib.request
import json


class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_colored(message: str, color: str = Colors.OKGREEN):
    """Print colored message"""
    print(f"{color}{message}{Colors.ENDC}")


def run_command(command: str, description: str = "") -> bool:
    """Run shell command and return success status"""
    if description:
        print(f"🔧 {description}")
    
    try:
        result = subprocess.run(
            command, shell=True, check=True, 
            capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error: {e}", Colors.FAIL)
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print_colored("🐍 Checking Python version...", Colors.HEADER)
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored(f"❌ Python 3.8+ required, found {version.major}.{version.minor}", Colors.FAIL)
        return False
    
    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} found", Colors.OKGREEN)
    return True


def check_system_requirements():
    """Check system requirements"""
    print_colored("🖥️  Checking system requirements...", Colors.HEADER)
    
    # Check OS
    os_name = platform.system()
    print(f"Operating System: {os_name}")
    
    # Check if git is available
    if shutil.which("git") is None:
        print_colored("⚠️  Git not found. Some features may not work.", Colors.WARNING)
    else:
        print_colored("✅ Git found", Colors.OKGREEN)
    
    # Check available disk space (rough estimate)
    try:
        statvfs = os.statvfs('.')
        free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
        if free_space_gb < 2:
            print_colored("⚠️  Low disk space. At least 2GB recommended.", Colors.WARNING)
        else:
            print_colored(f"✅ Available disk space: {free_space_gb:.1f}GB", Colors.OKGREEN)
    except:
        print("Could not check disk space")
    
    return True


def create_virtual_environment():
    """Create and activate virtual environment"""
    print_colored("🏗️  Setting up virtual environment...", Colors.HEADER)
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
        return False
    
    print_colored("✅ Virtual environment created", Colors.OKGREEN)
    return True


def get_pip_command():
    """Get the correct pip command for the virtual environment"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip"
    else:
        return "venv/bin/pip"


def install_dependencies():
    """Install Python dependencies"""
    print_colored("📦 Installing Python dependencies...", Colors.HEADER)
    
    pip_cmd = get_pip_command()
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install base requirements
    req_files = [
        "requirements/base.txt",
        "requirements/optional.txt"
    ]
    
    for req_file in req_files:
        if Path(req_file).exists():
            print(f"Installing from {req_file}...")
            if not run_command(f"{pip_cmd} install -r {req_file}", f"Installing {req_file}"):
                if "optional" in req_file:
                    print_colored("⚠️  Some optional dependencies failed to install", Colors.WARNING)
                else:
                    return False
    
    # Install additional commonly needed packages
    additional_packages = [
        "jupyter",
        "notebook",
        "ipywidgets",
        "python-dotenv",
        "pydantic-settings"
    ]
    
    for package in additional_packages:
        run_command(f"{pip_cmd} install {package}", f"Installing {package}")
    
    print_colored("✅ Dependencies installed", Colors.OKGREEN)
    return True


def setup_configuration():
    """Set up configuration files"""
    print_colored("⚙️  Setting up configuration...", Colors.HEADER)
    
    # Copy .env.example to .env if it doesn't exist
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print_colored("✅ Created .env file from template", Colors.OKGREEN)
        print_colored("📝 Please edit .env file with your API keys", Colors.WARNING)
    elif env_file.exists():
        print("✅ .env file already exists")
    
    # Create necessary directories
    directories = [
        "data/sample_datasets",
        "data/vector_stores",
        "logs",
        "outputs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_colored("✅ Directories created", Colors.OKGREEN)
    return True


def download_sample_data():
    """Download sample datasets"""
    print_colored("📊 Setting up sample data...", Colors.HEADER)
    
    sample_dir = Path("data/sample_datasets")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample text documents
    sample_texts = {
        "ai_overview.txt": """
        Artificial Intelligence (AI) Overview
        
        Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving.
        
        Key areas of AI include:
        - Machine Learning: Algorithms that improve automatically through experience
        - Natural Language Processing: Interaction between computers and human language  
        - Computer Vision: Interpretation and understanding of visual information
        - Robotics: Design and operation of robots
        - Expert Systems: Computer systems that emulate decision-making abilities
        """,
        
        "ml_fundamentals.txt": """
        Machine Learning Fundamentals
        
        Machine Learning (ML) is a subset of artificial intelligence that focuses on algorithms that can learn from and make predictions or decisions based on data. Instead of being explicitly programmed for every task, ML systems improve their performance on a specific task through experience.
        
        Types of Machine Learning:
        1. Supervised Learning: Learning with labeled training data
        2. Unsupervised Learning: Finding patterns in data without labels
        3. Reinforcement Learning: Learning through interaction with environment
        4. Semi-supervised Learning: Combination of labeled and unlabeled data
        """,
        
        "deep_learning_intro.txt": """
        Introduction to Deep Learning
        
        Deep Learning is a subset of machine learning that uses artificial neural networks with multiple layers (hence 'deep') to model and understand complex patterns in data. It's inspired by the structure and function of the human brain.
        
        Key concepts:
        - Neural Networks: Networks of interconnected nodes (neurons)
        - Layers: Input, hidden, and output layers
        - Activation Functions: Functions that determine neuron output
        - Backpropagation: Method for training neural networks
        - Convolutional Neural Networks (CNNs): For image processing
        - Recurrent Neural Networks (RNNs): For sequence data
        """
    }
    
    for filename, content in sample_texts.items():
        file_path = sample_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    print_colored("✅ Sample data created", Colors.OKGREEN)
    return True


def validate_installation():
    """Validate that installation was successful"""
    print_colored("🧪 Validating installation...", Colors.HEADER)
    
    # Test imports
    test_imports = [
        "openai",
        "langchain", 
        "chromadb",
        "sentence_transformers",
        "transformers",
        "numpy",
        "pandas"
    ]
    
    python_cmd = "venv/bin/python" if platform.system() != "Windows" else "venv\\Scripts\\python"
    
    failed_imports = []
    for module in test_imports:
        try:
            result = subprocess.run(
                [python_cmd, "-c", f"import {module}"],
                capture_output=True, text=True, check=True
            )
            print(f"✅ {module}")
        except subprocess.CalledProcessError:
            failed_imports.append(module)
            print_colored(f"❌ {module}", Colors.FAIL)
    
    if failed_imports:
        print_colored(f"⚠️  Some imports failed: {failed_imports}", Colors.WARNING)
        print("You may need to install additional dependencies or check your Python environment")
    else:
        print_colored("✅ All core modules imported successfully", Colors.OKGREEN)
    
    return len(failed_imports) == 0


def main():
    """Main installation function"""
    print_colored("🚀 GenerativeAI Starter Kit - Installation Script", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_system_requirements():
        print_colored("⚠️  System check completed with warnings", Colors.WARNING)
    
    # Setup steps
    steps = [
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Configuration", setup_configuration),
        ("Sample Data", download_sample_data),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print_colored(f"❌ Failed at step: {step_name}", Colors.FAIL)
            sys.exit(1)
    
    # Validation
    print(f"\n{'='*20} Validation {'='*20}")
    validate_installation()
    
    # Success message
    print_colored("\n🎉 Installation completed successfully!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.HEADER)
    
    # Next steps
    print_colored("\n📋 Next Steps:", Colors.HEADER)
    print("1. Edit .env file with your API keys:")
    print("   - OPENAI_API_KEY (required for most examples)")
    print("   - Other API keys as needed")
    print()
    print("2. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print()
    print("3. Run example scripts:")
    print("   python examples/rag/basic_rag_example.py")
    print()
    print("4. Start Jupyter notebook:")
    print("   jupyter notebook notebooks/")
    print()
    print_colored("📚 Documentation: Check docs/ folder for detailed guides", Colors.OKCYAN)


if __name__ == "__main__":
    main()