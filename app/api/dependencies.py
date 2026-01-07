"""
API Dependencies Module

Provides dependency injection for API routes.
"""
from typing import Generator
import os
import logging
from app.services.groq_service import GroqService
from app.core.state_manager import state_manager
from app.db.storage import order_storage, conversation_storage
from app.core.agent import OrderAgent

logger = logging.getLogger(__name__)

# Initialize Groq service
_groq_service = None


def get_groq_service() -> GroqService:
    """
    Get or create Groq service instance.
    
    Returns:
        GroqService instance
        
    Raises:
        Exception: If Groq API key is not configured
    """
    global _groq_service
    
    if _groq_service is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("GROQ_API_KEY not configured")
        _groq_service = GroqService(api_key=api_key)
        logger.info("Groq service initialized")
    
    return _groq_service


def get_order_agent() -> OrderAgent:
    """
    Get Order Agent instance.
    
    Returns:
        OrderAgent instance
    """
    groq_service = get_groq_service()
    return OrderAgent(groq_service=groq_service)


def get_state_manager():
    """
    Get state manager instance.
    
    Returns:
        OrderStateManager instance
    """
    return state_manager


def get_order_storage():
    """
    Get order storage instance.
    
    Returns:
        OrderStorage instance
    """
    return order_storage


def get_conversation_storage():
    """
    Get conversation storage instance.
    
    Returns:
        ConversationStorage instance
    """
    return conversation_storage
