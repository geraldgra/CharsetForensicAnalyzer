from pathlib import Path
from urllib.parse import urlparse
import tempfile
import requests
from core.logger import info, blank
from models import DownloadResult

USER_AGENT = (
    "Charset Forensic Analyzer/1.5 "
    "(Python Requests)"
)

def download(source, destination):

    with requests.get(
        source,
        headers={
            "User-Agent": USER_AGENT
        },
        stream=True,
        timeout=60,
        allow_redirects=True
    ) as response:
        response.raise_for_status()

        with open(destination, "wb") as f:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

        return {
            "url": source,
            "final_url": response.url,
            "http_status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "content_length": response.headers.get("Content-Length"),
            "redirects": len(response.history)
        }


def get_local_path(source):
    """
    Devuelve una ruta local.

    Si 'source' es una URL HTTP/HTTPS se descarga a un
    directorio temporal.

    Si es cualquier otra cosa, se considera un archivo local.
    """

    parsed = urlparse(source)

    #
    # URL HTTP / HTTPS
    #

    if parsed.scheme.lower() in ("http", "https"):

        #
        # Intentar conservar el nombre original
        #

        filename = Path(parsed.path).name

        if not filename:
            filename = "download"

        destination = (
            Path(tempfile.gettempdir())
            / filename
        )

        blank()
        info("Descargando archivo...")

        metadata = download(
            source,
            destination
        )

        info("")
        info("Archivo descargado correctamente.")
        info(str(destination))

        return DownloadResult(
            local_path=destination,
            original_source=source,
            metadata=metadata
        )

    #
    # Cualquier otro caso se considera un archivo local.
    #
    # Esto permite:
    #
    # C:\...
    # D:\...
    # \\Servidor\...
    # /home/...
    # ./archivo.txt
    #

    return DownloadResult(
        local_path=Path(source),
        original_source=source
    )