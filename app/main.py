from fastapi import FastAPI

from core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "app_env": settings.app_env,
    }
