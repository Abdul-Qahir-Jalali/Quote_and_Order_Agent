"""
Text Parsing Utilities

Helper functions for extracting structured data from text.
"""
import re
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse JSON from text containing code blocks.
    
    Args:
        text: Text potentially containing ```json ... ``` blocks
        
    Returns:
        Parsed JSON dictionary or None if not found/invalid
    """
    try:
        # Look for ```json ... ``` blocks
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {e}")
    
    return None


def remove_code_blocks(text: str) -> str:
    """
    Remove all code blocks (``` ... ```) from text.
    
    Args:
        text: Text potentially containing code blocks
        
    Returns:
        Text with code blocks removed
    """
    return re.sub(r"```[\w]*.*?```", "", text, flags=re.DOTALL | re.MULTILINE).strip()


def extract_action_commands(text: str) -> Dict[str, bool]:
    """
    Extract action commands from text.
    
    Args:
        text: Text potentially containing action commands
        
    Returns:
        Dictionary of action flags
    """
    return {
        "show_form": "ACTION_SHOW_FORM" in text,
        "submit_order": "ACTION_SUBMIT_ORDER" in text
    }


def clean_response_text(text: str) -> str:
    """
    Clean response text by removing code blocks and extra whitespace.
    
    Args:
        text: Raw response text
        
    Returns:
        Cleaned text
    """
    # Remove code blocks
    text = remove_code_blocks(text)
    
    # Remove action commands from visible text
    text = text.replace("ACTION_SHOW_FORM", "")
    text = text.replace("ACTION_SUBMIT_ORDER", "")
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
    text = text.strip()
    
    return text
