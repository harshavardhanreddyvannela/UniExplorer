from fastapi import FastAPI

from .config import settings
from .routes import router
from .schemas import HealthcheckResponse


app = FastAPI(title=settings.app_name)
app.include_router(router, prefix=settings.api_prefix)


@app.get("/", response_model=HealthcheckResponse)
def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(status="ok", service=settings.app_name)
