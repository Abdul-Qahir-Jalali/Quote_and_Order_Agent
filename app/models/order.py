"""
Order-related Data Models

Defines schemas for order submission and validation.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class OrderSchema(BaseModel):
    """
    Schema for order submission.
    
    All fields are required for a complete order.
    """
    full_name: str = Field(..., min_length=2, description="Customer's full name")
    email: EmailStr = Field(..., description="Customer's email address")
    phone: str = Field(..., min_length=10, description="Customer's phone number")
    address: str = Field(..., min_length=5, description="Delivery address")
    product_interest: str = Field(..., description="Product name")
    quantity: int = Field(..., ge=1, description="Order quantity")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number has at least 10 digits."""
        digits = re.sub(r'\D', '', v)
        if len(digits) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v
    
    @validator('full_name')
    def validate_name(cls, v):
        """Validate name is not empty after stripping."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class OrderState(BaseModel):
    """
    Internal state representation for order collection.
    
    Fields can be None if not yet collected.
    """
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    product_interest: Optional[str] = None
    quantity: Optional[int] = None
    
    def to_dict(self):
        """Convert to dictionary."""
        return self.dict()
    
    def is_complete(self) -> bool:
        """Check if all fields are filled."""
        return all([
            self.full_name,
            self.email,
            self.phone,
            self.address,
            self.product_interest,
            self.quantity
        ])
