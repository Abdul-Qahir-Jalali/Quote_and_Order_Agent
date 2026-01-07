"""
Web Page Routes

Handles rendering of web pages.
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def read_root(request: Request):
    """
    Serve the Landing Page.
    
    Returns:
        Rendered HTML template
    """
    return templates.TemplateResponse("index.html", {"request": request})
