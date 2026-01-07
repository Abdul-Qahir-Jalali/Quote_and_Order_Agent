"""
Chat Interaction Routes

Handles chat endpoint for agent interactions.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.models.chat import ChatMessage, ChatResponse
from app.api.dependencies import (
    get_order_agent,
    get_state_manager,
    get_order_storage,
    get_conversation_storage
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_req: ChatMessage):
    """
    Handle chat messages and return agent responses.
    
    Args:
        chat_req: Chat message with user text and session ID
        
    Returns:
        Agent response with state information
    """
    user_msg = chat_req.message
    session_id = chat_req.session_id
    
    # Get dependencies
    agent = get_order_agent()
    state_mgr = get_state_manager()
    conv_storage = get_conversation_storage()
    order_storage = get_order_storage()
    
    # Get conversation history
    conversation_history = conv_storage.get_history(session_id)
    
    # Add user message to history
    conv_storage.add_message(session_id, "user", user_msg)
    
    try:
        # Process message with agent
        result = await agent.process_message(
            session_id=session_id,
            user_text=user_msg,
            conversation_history=conversation_history
        )
        
        bot_text = result["response_text"]
        should_submit = result.get("should_submit", False)
        show_form = result.get("show_form", False)
        meta = result.get("meta", None)
        
        # Store bot message in history
        conv_storage.add_message(session_id, "assistant", bot_text)
        
        # Process order submission if needed
        if should_submit and result.get("final_data"):
            data = result["final_data"]
            order_id = order_storage.add_order(data)
            bot_text += f"\n\n[SYSTEM]: Order successfully submitted to system! (Order ID: {order_id})"
        
        # Get current state for frontend
        current_state = state_mgr.get_state(session_id)
        
        return ChatResponse(
            response=bot_text,
            state=current_state,
            should_submit=should_submit,
            show_form=show_form,
            meta=meta
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing chat message"
        )
