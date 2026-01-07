"""
Groq API Service Module

Handles all interactions with the Groq LLM API.
"""
from typing import List, Dict
import os
import logging
from groq import AsyncGroq

logger = logging.getLogger(__name__)


class GroqService:
    """
    Service for interacting with Groq API for LLM completions.
    """
    
    def __init__(self, api_key: str = None, model: str = "llama-3.1-8b-instant"):
        """
        Initialize the Groq service.
        
        Args:
            api_key: Groq API key (defaults to env variable)
            model: Model to use for completions
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            self.client = AsyncGroq(api_key=self.api_key)
            logger.info(f"Groq service initialized with model: {self.model}")
        else:
            logger.warning("Groq API key not provided")
    
    async def get_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.6, 
        max_tokens: int = 500
    ) -> str:
        """
        Get a completion from the Groq API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from the LLM
            
        Raises:
            Exception: If API key is not set or API call fails
        """
        if not self.client:
            raise Exception("Groq client not initialized. API key missing.")
        
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response_text = completion.choices[0].message.content
            logger.info(f"Groq completion successful ({len(response_text)} chars)")
            return response_text
            
        except Exception as e:
            logger.error(f"Groq API error: {e}", exc_info=True)
            raise
    
    def is_available(self) -> bool:
        """
        Check if the Groq service is available.
        
        Returns:
            True if client is initialized, False otherwise
        """
        return self.client is not None
