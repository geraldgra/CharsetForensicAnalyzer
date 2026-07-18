

import tempfile
import shutil

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import FileResponse

from pathlib import Path

from app import APP_NAME, APP_VERSION

from api.schemas import UrlRequest, AnalyzeResponse
from api.response import success

from api.upload import save_upload
from api.tempfiles import delete_temp_file

from services.analyzer_service import analyze
from services.converter_service import convert_to_utf8

from storage.manager import StorageManager

router = APIRouter()
storage = StorageManager()

@router.get("/")
def home():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.get("/version")
def version():
    return {
        "application": APP_NAME,
        "version": APP_VERSION
    }


@router.post(
    "/analyze/url",
    response_model=AnalyzeResponse,
    summary="Analyze a file from a URL.",
    tags=["Analysis"]
)
def analyze_url(
    request: Request,
    body: UrlRequest
):

    result = analyze(
        str(body.url),
        read_first_bytes=True
    )

    return success(
        request,
        result.to_dict()
    )


@router.post(
    "/analyze/file",
    response_model=AnalyzeResponse,
    summary="Analyze an uploaded file.",
    tags=["Analysis"]
)
def analyze_file(
    request: Request,
    file: UploadFile = File(...)
):

    temp_file = save_upload(file)

    try:

        result = analyze(
            str(temp_file),
            read_first_bytes=True
        )

        return success(
            request,
            result.to_dict()
        )

    finally:

        delete_temp_file(temp_file)


@router.post(
    "/convert/url",
    summary="Convert a file in URL to UTF-8 encoding.",
    tags=["Conversion"]
)
def convert_url(
    request: Request,
    body: UrlRequest
):

    result = analyze(
        str(body.url),
        read_first_bytes=False
    )

    download_info = convert_to_utf8(result)

    if download_info is None:
        raise ValueError(
            "The file could not be converted to UTF-8."
        )

    return success(
        request,
        {
            "encoding": "UTF-8",
            "download": download_info
        }
    )


@router.post(
    "/convert/file",
    summary="Convert a file to UTF-8 encoding.",
    tags=["Conversion"]
)
def convert_file(
    request: Request,
    file: UploadFile = File(...)
):

    temp_file = save_upload(file)

    try:

        result = analyze(
            str(temp_file),
            read_first_bytes=False
        )

        download_info = convert_to_utf8(result)

        if download_info is None:
            raise ValueError(
                "The file could not be converted to UTF-8."
            )

        return success(
            request,
            {
                "encoding": "UTF-8",
                "download": download_info
            }
        )

    finally:

        delete_temp_file(temp_file)


@router.get(
    "/download/{file_id}",
    summary="Download a file using its unique identifier.",
    tags=["Storage"]
)
def download_file(
    request: Request,
    file_id: str
):

    storage_file = storage.get_file(
        file_id
    )

    return FileResponse(
        path=storage_file,
        filename=storage_file.name,
        media_type="application/octet-stream"
    )
