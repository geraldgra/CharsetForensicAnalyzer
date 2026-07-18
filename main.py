from fastapi import FastAPI

from api.routes import router
from api.errors import (
    file_not_found_handler,
    value_error_handler,
    generic_handler,
    validation_handler,
    http_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.middleware import RequestContextMiddleware
from app import (
    APP_NAME,
    APP_VERSION,
    DESCRIPTION
)

app = FastAPI(
    title=APP_NAME,
    description=DESCRIPTION,
    version=APP_VERSION
)

app.include_router(router)


app.add_exception_handler(
    FileNotFoundError,
    file_not_found_handler
)

app.add_exception_handler(
    ValueError,
    value_error_handler
)

app.add_exception_handler(
    Exception,
    generic_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_handler
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_middleware(
    RequestContextMiddleware
)