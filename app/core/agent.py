from typing import Dict, Any, List
import logging
import re
import json

from app.core.state_manager import state_manager
from app.core.prompts import get_system_prompt
from app.services.groq_service import GroqService
from app.services.product_service import ProductService
from app.utils.parsers import extract_json_from_text, extract_action_commands
from app.utils.field_validators import validate_order_data, get_corrected_state

logger = logging.getLogger(__name__)

class OrderAgent:
    def __init__(self, groq_service: GroqService):
        self.groq_service = groq_service
        self.product_service = ProductService()
    
    async def process_message(
        self, session_id: str, user_text: str, conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        try:
            # --- 1. PROACTIVE FORM VALIDATION (Interception) ---
            if "```json" in user_text:
                json_data = extract_json_from_text(user_text)
                if json_data:
                    # Validate using Python
                    val_result = validate_order_data(json_data)
                    
                    # Update State: Persist VALID inputs, Clear INVALID ones
                    # 1. Update valid fields (so they don't disappear)
                    if val_result.valid_fields:
                        state_manager.update_state(session_id, val_result.valid_fields)
                    
                    # 2. Clear invalid fields (set to None explicitly)
                    invalid_updates = {field: None for field in val_result.invalid_fields}
                    if invalid_updates:
                        state_manager.update_state(session_id, invalid_updates)
                    
                    # If INVALID: show form with errors
                    if not val_result.is_valid:
                        return {
                            "response_text": val_result.get_feedback_message(),
                            "updates": json_data,
                            "show_form": True,
                            "should_submit": False,
                            "final_data": None
                        }
                    
                    # If VALID: Check if this is a confirmation
                    is_confirmed = json_data.get("confirmed", False)
                    if not is_confirmed:
                        # First time valid -> Request Confirmation
                        return {
                            "response_text": "Details valid. Please review carefully and press Confirm Order.",
                            "updates": json_data,
                            "show_form": True,
                            "should_submit": False,
                            "final_data": None,
                            "meta": {"form_mode": "confirm"} # Signal frontend to show "Confirm" button
                        }
                    
                    # If confirmed and valid -> Let it fall through to submission logic
                    # We return early here to mimic the "submit_order" action behavior
                    return {
                        "response_text": "Order confirmed! Processing now...",
                        "updates": json_data,
                        "show_form": False,
                        "should_submit": True,
                        "final_data": state_manager.get_state(session_id)
                    }

            # --- 2. REGULAR AI LOGIC ---
            current_state = state_manager.get_state(session_id)
            system_prompt = get_system_prompt(current_state)
            messages = [{"role": "system", "content": system_prompt}] + conversation_history
            
            bot_raw_response = await self.groq_service.get_completion(messages)
            
            response_text, updates = self._parse_llm_response(bot_raw_response, session_id)
            actions = extract_action_commands(response_text)
            
            clean_text = response_text.replace("ACTION_SHOW_FORM", "").replace("ACTION_SUBMIT_ORDER", "").strip()
            
            return {
                "response_text": clean_text,
                "updates": updates,
                "show_form": actions["show_form"],
                "should_submit": actions["submit_order"],
                "final_data": state_manager.get_state(session_id) if actions["submit_order"] else None
            }
            
        except Exception as e:
            logger.error(f"Agent processing error: {e}", exc_info=True)
            return {"response_text": "System Error. Please try again.", "show_form": False}

    def _parse_llm_response(self, bot_raw_response: str, session_id: str) -> tuple:
        updates = {}
        response_text = bot_raw_response
        if "```" in bot_raw_response:
            response_text = re.sub(r"```[\w]*.*?```", "", bot_raw_response, flags=re.DOTALL | re.MULTILINE).strip()
        if "```json" in bot_raw_response:
            json_data = extract_json_from_text(bot_raw_response)
            if json_data:
                updates = json_data
                state_manager.update_state(session_id, updates)
        
        response_text = self._handle_product_detection(response_text, session_id)
        return response_text, updates

    def _handle_product_detection(self, response_text: str, session_id: str) -> str:
        try:
            current_state = state_manager.get_state(session_id)
            known_products = self.product_service.get_all_products()
            products_mentioned = [p for p in known_products if p.lower() in response_text.lower()]
            choice_indicators = ["great choice", "excellent choice", "perfect choice", "good choice", "selected"]
            has_choice_indicator = any(ind in response_text.lower() for ind in choice_indicators)
            
            if len(products_mentioned) == 1 or (products_mentioned and has_choice_indicator):
                detected_product = products_mentioned[0]
                state_manager.update_state(session_id, {'product_interest': detected_product})
                if "ACTION_SHOW_FORM" not in response_text:
                    response_text += " ACTION_SHOW_FORM"
        except Exception:
            pass
        return response_text