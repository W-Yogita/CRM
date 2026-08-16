from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import database
import models
from routes import tickets

# 1. Dynamically resolve the absolute path to the directory containing main.py
BASE_DIR = Path(__file__).resolve().parent

# 2. Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Datastraw Support CRM")

# 3. Mount static folder (if you have local CSS/JS files)
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 4. Attach API routes (/api/tickets)
app.include_router(tickets.router)

# -------------------------------------------------------------------
# FRONTEND HTML ROUTES (Dynamic Absolute Pathing)
# -------------------------------------------------------------------

@app.get("/", response_class=FileResponse)
def home_page():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

@app.get("/create", response_class=FileResponse)
def create_page():
    return FileResponse(BASE_DIR / "frontend" / "create.html")

@app.get("/ticket/{ticket_id}", response_class=FileResponse)
def detail_page(ticket_id: str):
    return FileResponse(BASE_DIR / "frontend" / "detail.html")