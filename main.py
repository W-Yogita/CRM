from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import database
import models
from routes import tickets


BASE_DIR = Path(__file__).resolve().parent


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Datastraw Support CRM")


static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


app.include_router(tickets.router)





@app.get("/", response_class=FileResponse)
def home_page():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

@app.get("/create", response_class=FileResponse)
def create_page():
    return FileResponse(BASE_DIR / "frontend" / "create.html")

@app.get("/ticket/{ticket_id}", response_class=FileResponse)
def detail_page(ticket_id: str):
    return FileResponse(BASE_DIR / "frontend" / "detail.html")