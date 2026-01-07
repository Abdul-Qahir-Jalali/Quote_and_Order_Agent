import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.utils.logger import configure_app_logging
from app.api.routes import web, orders, chat

# Load environment variables
load_dotenv()

# Configure logging
configure_app_logging()

# Create FastAPI app
app = FastAPI(title="GOMWD Quote & Order Agent")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register routes
app.include_router(web.router)
app.include_router(orders.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    # reload=True taake code changes foran apply hon
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)