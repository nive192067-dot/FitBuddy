from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db
from .routes import router


settings = get_settings()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    init_db()

    yield


app = FastAPI(

    title=(
        "FitBuddy – AI Fitness "
        "Plan Generator"
    ),

    description=(
        "AI-powered 7-day fitness "
        "planning application."
    ),

    version="1.0.0",

    debug=settings.debug,

    lifespan=lifespan,
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=(
        settings.cors_origin_list
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static",
)


app.include_router(router)


@app.get("/health")
def health():

    return {

        "status": "ok",

        "service": "FitBuddy",
    }