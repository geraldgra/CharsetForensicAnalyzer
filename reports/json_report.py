import json
from pathlib import Path

from core.logger import info


def save(result):
    """
    Guarda el análisis en un archivo JSON.
    """

    destination = Path(result.file_path).with_suffix(".json")

    with open(destination, "w", encoding="utf-8") as f:

        json.dump(
            result.to_dict(),
            f,
            indent=4,
            ensure_ascii=False
        )

    info("")
    info(f"Reporte JSON generado: {destination}")


def show(result):
    """
    Imprime el análisis en formato JSON por consola.
    """

    print(
        result.to_json()
    )