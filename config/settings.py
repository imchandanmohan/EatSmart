"""
EatSmart Application Settings

This module handles all configuration settings for the EatSmart application.
Settings are loaded from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class MCPSettings(BaseModel):
    """MCP Server Configuration"""
    host: str = "localhost"
    port: int = 3000
    name: str = "eatsmart"


class EmailSettings(BaseModel):
    """Email Service Configuration"""
    # SMTP Settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    username: str = ""
    password: str = ""
    from_name: str = "EatSmart Assistant"
    
    # SendGrid Settings (alternative)
    sendgrid_api_key: Optional[str] = None
    sendgrid_from_email: Optional[str] = None


class OpenFoodFactsSettings(BaseModel):
    """OpenFoodFacts API Configuration"""
    base_url: str = "https://world.openfoodfacts.org"
    user_agent: str = "EatSmart/1.0.0"
    timeout: int = 30
    max_retries: int = 3


class VectorDBSettings(BaseModel):
    """Vector Database Configuration"""
    # ChromaDB (local)
    chromadb_path: str = "./data/chromadb"
    collection_name: str = "eatsmart_products"
    
    # Pinecone (cloud)
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "eatsmart-index"
    
    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384


class RAGSettings(BaseModel):
    """RAG Configuration"""
    top_k_results: int = 10
    similarity_threshold: float = 0.7
    max_context_length: int = 4000


class CacheSettings(BaseModel):
    """Caching Configuration"""
    enabled: bool = True
    ttl_seconds: int = 3600
    max_size: int = 1000
    redis_url: Optional[str] = None
    redis_password: Optional[str] = None


class ImageSettings(BaseModel):
    """Image Processing Configuration"""
    max_size: str = "1024x1024"
    quality: int = 85
    supported_formats: List[str] = ["jpg", "png", "webp"]


class NutritionSettings(BaseModel):
    """Nutrition Analysis Configuration"""
    health_score_weights: dict = {
        "sugar": 0.25,
        "salt": 0.25,
        "fat": 0.25,
        "additives": 0.25
    }


class SecuritySettings(BaseModel):
    """Security Configuration"""
    secret_key: str = "change-this-in-production"
    api_key_header: str = "X-API-Key"


class Settings(BaseSettings):
    """Main Application Settings"""
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    environment: str = "development"
    
    # MCP Configuration
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    
    # Email Configuration
    email: EmailSettings = Field(default_factory=EmailSettings)
    
    # OpenFoodFacts API
    openfoodfacts: OpenFoodFactsSettings = Field(default_factory=OpenFoodFactsSettings)
    
    # Vector Database
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    
    # RAG Configuration
    rag: RAGSettings = Field(default_factory=RAGSettings)
    
    # Cache Configuration
    cache: CacheSettings = Field(default_factory=CacheSettings)
    
    # Image Processing
    image: ImageSettings = Field(default_factory=ImageSettings)
    
    # Nutrition Analysis
    nutrition: NutritionSettings = Field(default_factory=NutritionSettings)
    
    # Security
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    
    # Rate Limiting
    api_rate_limit_per_minute: int = 60
    max_products_per_request: int = 50
    
    # Database
    database_url: str = "sqlite:///./data/eatsmart.db"
    database_echo: bool = False
    
    # Logging
    enable_structured_logging: bool = True
    log_file_path: str = "./logs/eatsmart.log"
    log_rotation_size: str = "10MB"
    log_retention_days: int = 30
    
    # Development
    reload_on_change: bool = True
    enable_cors: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # External AI Services (optional)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Nested model parsing
        env_nested_delimiter = "_"
        
        @classmethod
        def prepare_field_env(cls, field_name: str, model_config) -> List[str]:
            """Generate environment variable names for nested fields"""
            if field_name == "mcp":
                return [f"MCP_{key.upper()}" for key in ["host", "port", "name"]]
            elif field_name == "email":
                return [f"EMAIL_{key.upper()}" for key in [
                    "smtp_server", "smtp_port", "smtp_use_tls", 
                    "username", "password", "from_name",
                    "sendgrid_api_key", "sendgrid_from_email"
                ]]
            # Add more nested field mappings as needed
            return [field_name.upper()]


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance"""
    return settings


def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get data directory path"""
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_logs_dir() -> Path:
    """Get logs directory path"""
    logs_dir = get_project_root() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


# Environment-specific settings
def is_development() -> bool:
    """Check if running in development mode"""
    return settings.environment.lower() == "development"


def is_production() -> bool:
    """Check if running in production mode"""
    return settings.environment.lower() == "production"


def is_testing() -> bool:
    """Check if running in testing mode"""
    return settings.environment.lower() == "testing"