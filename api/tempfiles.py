from pathlib import Path


def delete_temp_file(path: Path):
    """
    Elimina un archivo temporal.

    No produce error si ya no existe.
    """

    if path is None:
        return

    Path(path).unlink(
        missing_ok=True
    )