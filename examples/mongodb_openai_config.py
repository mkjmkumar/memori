"""
Configuration for MongoDB + OpenAI + Memori Integration

This module provides configuration utilities for the MongoDB OpenAI example.
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class MongoDBOpenAIConfig:
    """Configuration class for MongoDB OpenAI integration"""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 500
    
    # MongoDB Configuration
    mongodb_uri: str
    database_name: str = "memori"
    collection_prefix: str = "memories"
    
    # Memori Configuration
    namespace: str = "openai_assistant"
    auto_ingest: bool = True
    conscious_ingest: bool = True
    verbose: bool = True
    
    # Chat Configuration
    max_conversation_history: int = 10
    max_memory_context: int = 5
    memory_search_limit: int = 5

def load_config() -> MongoDBOpenAIConfig:
    """
    Load configuration from environment variables with sensible defaults
    """
    return MongoDBOpenAIConfig(
        # Required environment variables
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        mongodb_uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017/memori"),
        
        # Optional configurations with defaults
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "500")),
        
        database_name=os.getenv("MONGODB_DATABASE", "memori"),
        namespace=os.getenv("MEMORI_NAMESPACE", "openai_assistant"),
        
        auto_ingest=os.getenv("MEMORI_AUTO_INGEST", "true").lower() == "true",
        conscious_ingest=os.getenv("MEMORI_CONSCIOUS_INGEST", "true").lower() == "true",
        verbose=os.getenv("MEMORI_VERBOSE", "true").lower() == "true",
    )

def validate_config(config: MongoDBOpenAIConfig) -> bool:
    """
    Validate that all required configuration is present
    """
    if not config.openai_api_key:
        print("❌ OPENAI_API_KEY is required")
        return False
    
    if not config.mongodb_uri:
        print("❌ MONGODB_URI is required")
        return False
    
    if config.openai_api_key == "your-api-key-here":
        print("❌ Please set a real OpenAI API key")
        return False
    
    return True

# Example configurations for different use cases
CONFIGS = {
    "development": {
        "mongodb_uri": "mongodb://localhost:27017/memori_dev",
        "verbose": True,
        "auto_ingest": True,  # Enable for development
    },
    
    "production": {
        "mongodb_uri": "mongodb+srv://cluster.mongodb.net/memori",
        "verbose": False,
        "auto_ingest": True,  # Enable for production
        "openai_model": "gpt-4o",  # Better model for production
    },
    
    "testing": {
        "mongodb_uri": "mongodb://localhost:27017/memori_test",
        "namespace": "test_session",
        "auto_ingest": False,  # Manual memory control for testing
        "verbose": True,
    }
}

def get_config_for_environment(env: str = "development") -> MongoDBOpenAIConfig:
    """
    Get configuration for a specific environment
    """
    base_config = load_config()
    env_overrides = CONFIGS.get(env, {})
    
    # Apply environment-specific overrides
    for key, value in env_overrides.items():
        if hasattr(base_config, key):
            setattr(base_config, key, value)
    
    return base_config