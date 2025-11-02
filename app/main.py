from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import engine, Base
from app.api.routes import projects_router, tasks_router
from app.utils.logger import setup_logger
from app.schemas.response import StandardResponse, ErrorResponse

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="PM API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail, message=str(exc.detail)).model_dump()
    )


@app.get("/")
def root():
    return StandardResponse(data={"version": "1.0.0"}, message="PM API")


@app.get("/health", response_model=StandardResponse[dict])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return StandardResponse(data={"status": "healthy", "database": "connected"}, message="system is working normally")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        error = ErrorResponse(error="database is unavailable", message="failed to connect to database")
        raise HTTPException(status_code=500, detail=error.model_dump())

