"""
Web Page Routes

Handles rendering of web pages.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.api.dependencies import get_order_storage

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def read_root(request: Request):
    """
    Serve the Landing Page.
    
    Returns:
        Rendered HTML template
    """
    from app.services.product_service import ProductService
    product_service = ProductService()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": product_service.get_catalog()
    })


@router.get("/admin")
async def admin_dashboard(request: Request):
    """
    Serve the Admin Dashboard.
    
    Returns:
        Rendered Admin HTML template
    """
    storage = get_order_storage()
    orders = storage.get_all_orders()
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "orders": orders
    })
