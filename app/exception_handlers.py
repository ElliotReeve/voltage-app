import logging

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

unhandled_logger = logging.getLogger(f"{__name__}.unhandled_logger")


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)

    return JSONResponse(
        {"error": {"message": exc.detail}, "status": "Error"},
        status_code=exc.status_code,
        headers=headers,
    )


async def handle_unhandled_exceptions(request: Request, exc: Exception):
    unhandled_logger.error(str(exc), exc_info=exc)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": "Internal server error"}, "status": "Error"},
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "\n".join(
                    f"{'.'.join(error['loc'][1:])}: {error['msg']}"
                    for error in exc.errors()
                ),
            },
            "status": "Error",
        },
    )
