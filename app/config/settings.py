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
    product_catalog: List[dict] = [
        {
            "name": "The Cloud Sofa",
            "price": 2499,
            "description": "Experience the ultimate in comfort with our best-selling specialized foam blend.",
            "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "name": "Classic Chesterfield",
            "price": 3299,
            "description": "A timeless classic featuring deep button tufting and rich premium leather.",
            "image_url": "https://images.unsplash.com/photo-1550254478-ead40cc54513?auto=format&fit=crop&w=800&q=80"
        },
        {
            "name": "Artisan Oak Table",
            "price": 1299,
            "description": "Handcrafted from solid oak with a beautiful natural finish.",
            "image_url": "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "name": "Velvet Armchair",
            "price": 899,
            "description": "Add a touch of luxury with this plush velvet armchair in jewel tones.",
            "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=800&q=80"
        }
    ]

    @property
    def known_products(self) -> List[str]:
        """Backward compatibility for getting just product names"""
        return [p["name"] for p in self.product_catalog]
    
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
