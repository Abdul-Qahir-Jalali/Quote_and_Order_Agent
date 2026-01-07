"""
Order Management Routes

Handles order submission and retrieval endpoints.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.models.order import OrderSchema
from app.api.dependencies import get_order_storage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["orders"])


@router.post("/submit_order")
async def submit_order(order: OrderSchema):
    """
    Receive and process order submissions.
    
    Args:
        order: Validated order data
        
    Returns:
        Success response with order ID
    """
    logger.info(f"Received Order: {order.dict()}")
    
    # Store order
    storage = get_order_storage()
    order_id = storage.add_order(order.dict())
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Order processed successfully",
            "order_id": order_id
        }
    )


@router.get("/orders")
async def get_orders():
    """
    Debug endpoint to retrieve all stored orders.
    
    Returns:
        List of all orders
    """
    storage = get_order_storage()
    return storage.get_all_orders()
