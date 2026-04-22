from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes.calculator import router
from app.utils.logger import logger

app = FastAPI(title="Distroless Calculator API")

app.include_router(router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        },
    )