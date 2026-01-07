import re
from typing import Dict, Any

class ValidationResult:
    def __init__(self):
        self.valid_fields = {}
        self.invalid_fields = {}
        self.is_valid = True

    def add_valid(self, field_name: str, value: Any):
        self.valid_fields[field_name] = value

    def add_invalid(self, field_name: str, value: Any, error_msg: str):
        self.invalid_fields[field_name] = error_msg
        self.is_valid = False

    def get_feedback_message(self) -> str:
        if self.is_valid:
            return "Details valid. Please review carefully and press Confirm Order."

        msg = "The following details need correction:\n\n"
        
        for field, error in self.invalid_fields.items():
            display_name = field.replace('_', ' ').title()
            msg += f"❌ **{display_name}**: {error}\n"
        
        msg += "\nPlease correct these fields in the form below."
        return msg

def validate_order_data(data: Dict[str, Any]) -> ValidationResult:
    result = ValidationResult()

    # Full Name
    name = str(data.get("full_name", "")).strip()
    if len(name) < 2:
        result.add_invalid("full_name", name, "Must be at least 2 characters")
    else:
        result.add_valid("full_name", name)

    # Email
    email = str(data.get("email", "")).strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        result.add_invalid("email", email, "Invalid email format")
    else:
        result.add_valid("email", email)

    # Phone (Strict Check)
    phone = str(data.get("phone", ""))
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 10:
        result.add_invalid("phone", phone, f"Must be at least 10 digits (found {len(digits)})")
    else:
        result.add_valid("phone", phone)

    # Address
    address = str(data.get("address", "")).strip()
    if len(address) < 5:
        result.add_invalid("address", address, "Must be at least 5 characters")
    else:
        result.add_valid("address", address)

    # Product & Quantity
    result.add_valid("product_interest", data.get("product_interest", "The Cloud Sofa"))
    try:
        qty = int(data.get("quantity", 1))
        if qty < 1: result.add_invalid("quantity", qty, "Must be at least 1")
        else: result.add_valid("quantity", qty)
    except:
        result.add_invalid("quantity", data.get("quantity"), "Must be a number")

    return result

def get_corrected_state(original_state: Dict[str, Any], validation_result: ValidationResult) -> Dict[str, Any]:
    new_state = original_state.copy()
    for field in validation_result.invalid_fields:
        new_state[field] = None # Clears the field in the form
    return new_state