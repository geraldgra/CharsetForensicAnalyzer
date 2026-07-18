from pathlib import Path
from fastapi import UploadFile
import shutil
import tempfile


def save_upload(file: UploadFile) -> Path:
    """
    Guarda un UploadFile en un archivo temporal.

    Devuelve la ruta del archivo creado.
    """

    suffix = ""

    if file.filename and "." in file.filename:
        suffix = Path(file.filename).suffix

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp.close()

    with open(temp.name, "wb") as out:
        shutil.copyfileobj(
            file.file,
            out
        )

    return Path(temp.name)