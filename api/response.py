from datetime import datetime, UTC
from http import HTTPStatus
from uuid import uuid4
import time
from app import (
    APP_NAME,
    APP_VERSION
)

SERVICE_NAME = APP_NAME
SERVICE_VERSION = APP_VERSION


def _utc_now():

    return (
        datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def success(
    request,
    data
):

    return {
        "Service": SERVICE_NAME,
        "Version": SERVICE_VERSION,
        "TransactionId": transaction_id(request),
        "TimestampUtc": _utc_now(),
        "ExecutionTimeMs": execution_time(request),
        "Data": data,
        "Status": {
            "Code": 200,
            "Value": HTTPStatus(200).phrase
        }
    }


def error(
    request,
    status_code,
    code,
    message,
    details=None,
    status_value=None
):
    """
    Construye una respuesta de error uniforme para toda la API.
    """

    if status_value is None:
        status_value = HTTPStatus(status_code).phrase

    payload = {
        "Service": SERVICE_NAME,
        "Version": SERVICE_VERSION,
        "TransactionId": transaction_id(request),
        "TimestampUtc": _utc_now(),
        "ExecutionTimeMs": execution_time(request),
        "Error": {
            "Code": code,
            "Message": message
        },
        "Status": {
            "Code": status_code,
            "Value": status_value
        }
    }

    if details is not None:
        payload["Error"]["Details"] = details

    return payload

def execution_time(request):

    started = request.scope.get("started_at")

    if started is None:
        return None

    return round(
        (time.perf_counter() - started) * 1000,
        2
    )


def transaction_id(request):

    return request.scope.get(
        "transaction_id",
        str(uuid4())
    )