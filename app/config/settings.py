"""
Application Configuration and Settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    
    # Model Configuration
    groq_model: str = "llama-3.1-8b-instant"
    temperature: float = 0.6
    max_tokens: int = 500
    
    # Product Catalog
    known_products: List[str] = [
        "The Cloud Sofa",
        "Classic Chesterfield",
        "Artisan Oak Table",
        "Velvet Armchair"
    ]
    
    # Required Order Fields
    required_slots: List[str] = [
        "full_name",
        "email",
        "phone",
        "address",
        "product_interest",
        "quantity"
    ]
    
    # Choice Indicators for Product Selection
    choice_indicators: List[str] = [
        "great choice",
        "excellent choice",
        "perfect choice",
        "good choice",
        "i've selected",
        "you've chosen"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
