# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import logging
from app.controllers import api_controller, auth_controller
from app.controllers import event_controller
from app.controllers import match_controller
from app.controllers import club_controller
from app.core.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)

app = FastAPI(title="CampusBall API", version="1.0")

app.include_router(api_controller.router)
app.include_router(auth_controller.router)
app.include_router(event_controller.router)
app.include_router(match_controller.router)
app.include_router(club_controller.router)

settings = get_settings()
os.makedirs(settings.files_dir, exist_ok=True)
app.mount("/files", StaticFiles(directory=settings.files_dir), name="files")

 