"""
Configuration settings for the GenerativeAI Starter Kit
"""
import os
from pathlib import Path
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    google_api_key: str = Field(default="", env="GOOGLE_API_KEY")
    
    # Vector Database Configuration
    pinecone_api_key: str = Field(default="", env="PINECONE_API_KEY")
    pinecone_environment: str = Field(default="", env="PINECONE_ENVIRONMENT")
    weaviate_url: str = Field(default="http://localhost:8080", env="WEAVIATE_URL")
    qdrant_url: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    
    # Model Configuration
    default_llm_model: str = Field(default="gpt-3.5-turbo", env="DEFAULT_LLM_MODEL")
    default_embedding_model: str = Field(default="text-embedding-ada-002", env="DEFAULT_EMBEDDING_MODEL")
    max_tokens: int = Field(default=4096, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    
    # Application Settings
    app_name: str = Field(default="GenerativeAI-Starter-Kit", env="APP_NAME")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Paths
    data_dir: Path = Field(default=Path("./data"), env="DATA_DIR")
    vector_store_dir: Path = Field(default=Path("./data/vector_stores"), env="VECTOR_STORE_DIR")
    sample_data_dir: Path = Field(default=Path("./data/sample_datasets"), env="SAMPLE_DATA_DIR")
    
    # Fine-tuning Settings
    wandb_project: str = Field(default="generative-ai-starter", env="WANDB_PROJECT")
    wandb_api_key: str = Field(default="", env="WANDB_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_model_config(model_type: str = "default") -> Dict[str, Any]:
    """Get model configuration based on type"""
    configs = {
        "default": {
            "model": settings.default_llm_model,
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
        },
        "creative": {
            "model": settings.default_llm_model,
            "temperature": 0.9,
            "max_tokens": settings.max_tokens,
        },
        "precise": {
            "model": settings.default_llm_model,
            "temperature": 0.1,
            "max_tokens": settings.max_tokens,
        },
        "embedding": {
            "model": settings.default_embedding_model,
        }
    }
    return configs.get(model_type, configs["default"])


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        settings.data_dir,
        settings.vector_store_dir,
        settings.sample_data_dir,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_directories()
    print(f"Settings loaded for {settings.app_name}")
    print(f"Debug mode: {settings.debug}")