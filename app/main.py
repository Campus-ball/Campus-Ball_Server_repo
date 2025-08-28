# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.controllers import api_controller
from app.core.settings import get_settings

app = FastAPI(title="CampusBall API", version="1.0")

app.include_router(api_controller.router)

settings = get_settings()
os.makedirs(settings.files_dir, exist_ok=True)
app.mount("/files", StaticFiles(directory=settings.files_dir), name="files")
