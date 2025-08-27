# app/main.py
from fastapi import FastAPI

app = FastAPI(title="CampusBall API", version="1.0")

# app.include_router(auth_controller.router, prefix="/api/v1")
# app.include_router(users_controller.router, prefix="/api/v1")
# app.include_router(colleges_controller.router, prefix="/api/v1")
# app.include_router(clubs_controller.router, prefix="/api/v1")
# app.include_router(availability_controller.router, prefix="/api/v1")
# app.include_router(matches_controller.router, prefix="/api/v1")
# app.include_router(events_controller.router, prefix="/api/v1")
