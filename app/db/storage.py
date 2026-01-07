"""
In-Memory Storage Module

Provides storage abstraction for orders and conversation history.
Can be easily replaced with actual database implementation.
"""
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class OrderStorage:
    """
    In-memory storage for orders.
    
    Future: Can be replaced with SQLAlchemy/database implementation.
    """
    
    def __init__(self):
        """Initialize empty order storage."""
        self._orders: List[Dict[str, Any]] = []
    
    def add_order(self, order_data: Dict[str, Any]) -> int:
        """
        Add an order to storage.
        
        Args:
            order_data: Order data dictionary
            
        Returns:
            Order ID (1-indexed position in list)
        """
        self._orders.append(order_data)
        order_id = len(self._orders)
        logger.info(f"Order {order_id} added to storage")
        return order_id
    
    def get_all_orders(self) -> List[Dict[str, Any]]:
        """
        Get all orders.
        
        Returns:
            List of all orders
        """
        return self._orders.copy()
    
    def get_order_by_id(self, order_id: int) -> Dict[str, Any]:
        """
        Get a specific order by ID.
        
        Args:
            order_id: Order ID (1-indexed)
            
        Returns:
            Order data dictionary or None if not found
        """
        if 0 < order_id <= len(self._orders):
            return self._orders[order_id - 1]
        return None
    
    def count(self) -> int:
        """
        Get count of orders.
        
        Returns:
            Number of orders in storage
        """
        return len(self._orders)


class ConversationStorage:
    """
    In-memory storage for conversation history.
    
    Stores conversation history per session.
    """
    
    def __init__(self):
        """Initialize empty conversation storage."""
        self._conversations: Dict[str, List[Dict[str, str]]] = {}
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of message dictionaries
        """
        if session_id not in self._conversations:
            self._conversations[session_id] = []
        return self._conversations[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to conversation history.
        
        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        history = self.get_history(session_id)
        history.append({"role": role, "content": content})
        logger.debug(f"Message added to session {session_id}: {role}")
    
    def clear_history(self, session_id: str):
        """
        Clear conversation history for a session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._conversations:
            del self._conversations[session_id]
            logger.info(f"Conversation history cleared for session {session_id}")


# Global storage instances
order_storage = OrderStorage()
conversation_storage = ConversationStorage()
