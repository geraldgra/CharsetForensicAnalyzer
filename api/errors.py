from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status
from api.response import error


async def file_not_found_handler(
    request: Request,
    exc: FileNotFoundError
):

    return JSONResponse(
        status_code=404,
        content=error(
            request=request,
            status_code=404,
            status_value="Not Found",
            code="FILE_NOT_FOUND",
            message=str(exc)
        )
    )

async def value_error_handler(
    request: Request,
    exc: ValueError
):

    return JSONResponse(
        status_code=400,
        content=error(
            request=request,
            status_code=400,
            status_value="Bad Request",
            code="INVALID_REQUEST",
            message=str(exc)
        )
    )

async def generic_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content=error(
            request=request,
            status_code=500,
            status_value="Internal Server Error",
            code="UNEXPECTED_ERROR",
            message=str(exc)
        )
    )

async def validation_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=422,
        content=error(
            request=request,
            status_code=422,
            status_value="Unprocessable Entity",
            code="VALIDATION_ERROR",
            message="The request is invalid.",
            details=exc.errors()
        )
    )

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):

    values = {
        401: ("UNAUTHORIZED", "Unauthorized"),
        403: ("FORBIDDEN", "Forbidden"),
        404: ("NOT_FOUND", "Not Found"),
        405: ("METHOD_NOT_ALLOWED", "Method Not Allowed")
    }

    code, value = values.get(
        exc.status_code,
        ("HTTP_ERROR", "HTTP Error")
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error(
            request=request,
            status_code=exc.status_code,
            status_value=value,
            code=code,
            message=str(exc.detail)
        )
    )