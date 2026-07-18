from pathlib import Path
from uuid import uuid4
from datetime import datetime, UTC, timedelta
import shutil
import tempfile


class StorageManager:

    def __init__(self):

        self.root = (
            Path(tempfile.gettempdir())
            / "charset-storage"
        )

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        source_file,
        expires_hours=24
    ):

        if source_file is None:
            raise ValueError("No se generó ningún archivo para almacenar.")
        
        source = Path(source_file)
        extension = source.suffix
        file_id = f"{uuid4()}{extension}"
        destination = self.root / file_id
        shutil.copy2(
            source,
            destination
        )

        expires = (
            datetime.now(UTC)
            + timedelta(hours=expires_hours)
        ).replace(
            microsecond=0
        ).isoformat().replace(
            "+00:00",
            "Z"
        )

        return {
            "id": file_id,
            "path": str(destination),
            "download_url": f"/download/{file_id}",
            "size": destination.stat().st_size,
            "expires_at": expires
        }

    def get_file(
        self,
        file_id
    ):

        file = self.root / file_id

        if not file.exists():
            raise FileNotFoundError(file_id)

        return file