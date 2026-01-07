"""
Chat-related Data Models

Defines schemas for chat interactions.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatMessage(BaseModel):
    """
    Schema for incoming chat messages.
    """
    message: str = Field(..., min_length=1, description="User's message text")
    session_id: str = Field(..., description="Unique session identifier")


class ChatResponse(BaseModel):
    """
    Schema for chat response.
    """
    response: str = Field(..., description="Agent's response text")
    state: Optional[Dict[str, Any]] = Field(default=None, description="Current order state")
    should_submit: Optional[bool] = Field(default=False, description="Whether to submit order")
    show_form: Optional[bool] = Field(default=False, description="Whether to trigger the UI form")
    meta: Optional[Dict[str, Any]] = Field(default=None, description="Metadata for frontend actions")
