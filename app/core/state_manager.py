"""
Order State Management Module

Handles session-based state tracking for order collection.
Each session maintains its own state with required order fields.
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Define the schema of what we need to collect
REQUIRED_SLOTS = [
    "full_name", 
    "email", 
    "phone", 
    "address", 
    "product_interest", 
    "quantity"
]


class OrderStateManager:
    """
    Manages in-memory state for order collection across sessions.
    
    Each session has its own state dictionary tracking required fields.
    """
    
    def __init__(self):
        """Initialize the state manager with empty storage."""
        # In-memory store: { session_id: { slot_name: value } }
        self.states: Dict[str, Dict[str, Optional[str]]] = {}

    def get_state(self, session_id: str) -> Dict[str, Optional[str]]:
        """
        Get the current state for a session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Dictionary of slot names to values (None if not filled)
        """
        if session_id not in self.states:
            self.states[session_id] = {slot: None for slot in REQUIRED_SLOTS}
        return self.states[session_id]

    def update_state(self, session_id: str, updates: dict) -> Dict[str, Optional[str]]:
        """
        Update the state for a session with new values.
        
        Args:
            session_id: Unique session identifier
            updates: Dictionary of slot names to new values
            
        Returns:
            Updated state dictionary
        """
        current = self.get_state(session_id)
        current.update(updates)
        self.states[session_id] = current
        logger.info(f"Session {session_id}: Updated state with {list(updates.keys())}")
        return current

    def get_missing_slots(self, session_id: str) -> List[str]:
        """
        Get list of slots that haven't been filled yet.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            List of slot names that are still None
        """
        state = self.get_state(session_id)
        return [slot for slot, val in state.items() if val is None]
    
    def is_complete(self, session_id: str) -> bool:
        """
        Check if all required slots are filled.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if all slots have values, False otherwise
        """
        return len(self.get_missing_slots(session_id)) == 0
    
    def reset_state(self, session_id: str) -> None:
        """
        Reset the state for a session.
        
        Args:
            session_id: Unique session identifier
        """
        if session_id in self.states:
            del self.states[session_id]
            logger.info(f"Session {session_id}: State reset")


# Global singleton instance
state_manager = OrderStateManager()
