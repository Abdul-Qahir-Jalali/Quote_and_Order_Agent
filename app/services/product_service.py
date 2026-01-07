"""
Product Catalog Service Module

Handles product catalog management and search functionality.
"""
from typing import List
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class ProductService:
    """
    Service for managing product catalog and product-related operations.
    """
    
    def __init__(self):
        """Initialize the product service with catalog from settings."""
        self.products = settings.known_products
        self.catalog = settings.product_catalog
        logger.info(f"Product service initialized with {len(self.products)} products")
    
    def get_all_products(self) -> List[str]:
        """
        Get all products in the catalog.
        
        Returns:
            List of product names
        """
        return self.products.copy()

    def get_catalog(self) -> List[dict]:
        """
        Get the full product catalog with metadata.
        
        Returns:
            List of product dictionaries
        """
        return self.catalog.copy()
    
    def search_products(self, keyword: str) -> List[str]:
        """
        Search for products matching a keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching product names
        """
        keyword = keyword.lower()
        matching = [p for p in self.products if keyword in p.lower()]
        logger.info(f"Product search '{keyword}': found {len(matching)} matches")
        return matching
    
    def normalize_product_name(self, user_input: str) -> str:
        """
        Normalize user input to a standard product name.
        
        Args:
            user_input: User's product description
            
        Returns:
            Normalized product name or original input if no match
        """
        user_input_lower = user_input.lower()
        
        # Try exact match first
        for product in self.products:
            if product.lower() == user_input_lower:
                return product
        
        # Try partial match
        for product in self.products:
            if user_input_lower in product.lower() or product.lower() in user_input_lower:
                return product
        
        # Return original if no match
        return user_input
    
    def is_valid_product(self, product_name: str) -> bool:
        """
        Check if a product name is valid.
        
        Args:
            product_name: Product name to validate
            
        Returns:
            True if product exists in catalog
        """
        return product_name in self.products
