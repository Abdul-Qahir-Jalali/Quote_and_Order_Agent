"""
In-Memory Storage Module

Provides storage abstraction for orders and conversation history.
Can be easily replaced with actual database implementation.
"""
from typing import Dict, List, Any
import logging
import os

logger = logging.getLogger(__name__)


class OrderStorage:
    """
    File-based storage for orders using JSON.
    Simulates a database using data/orders.json.
    """
    
    def __init__(self, storage_file: str = "data/orders.json"):
        """
        Initialize order storage with file path.
        
        Args:
            storage_file: Path to JSON storage file
        """
        self.storage_file = storage_file
        self._ensure_storage_dir()
        self._load_orders()
        
    def _ensure_storage_dir(self):
        """Ensure storage directory exists."""
        dirname = os.path.dirname(self.storage_file)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
            
    def _load_orders(self):
        """Load orders from JSON file."""
        if os.path.exists(self.storage_file):
            try:
                import json
                with open(self.storage_file, 'r') as f:
                    self._orders = json.load(f)
                logger.info(f"Loaded {len(self._orders)} orders from {self.storage_file}")
            except Exception as e:
                logger.error(f"Error loading orders: {e}")
                self._orders = []
        else:
            self._orders = []
            
    def _save_orders(self):
        """Save orders to JSON file."""
        try:
            import json
            with open(self.storage_file, 'w') as f:
                json.dump(self._orders, f, indent=2)
            logger.info(f"Saved {len(self._orders)} orders to {self.storage_file}")
        except Exception as e:
            logger.error(f"Error saving orders: {e}")
    
    def add_order(self, order_data: Dict[str, Any]) -> int:
        """
        Add an order to storage and save to file.
        
        Args:
            order_data: Order data dictionary
            
        Returns:
            Order ID (1-indexed position in list)
        """
        self._orders.append(order_data)
        self._save_orders()
        
        order_id = len(self._orders)
        logger.info(f"Order {order_id} added and saved")
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
