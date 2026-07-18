from pathlib import Path
from datetime import datetime, timedelta


def cleanup(folder, hours=24):

    folder = Path(folder)

    limit = datetime.now() - timedelta(hours=hours)

    for file in folder.iterdir():

        if not file.is_file():
            continue

        modified = datetime.fromtimestamp(
            file.stat().st_mtime
        )

        if modified < limit:

            file.unlink(
                missing_ok=True
            )