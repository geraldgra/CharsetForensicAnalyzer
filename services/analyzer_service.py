from pathlib import Path
import hashlib

from models import AnalysisResult

from core.analyzer_engine import AnalyzerEngine
from core.downloader import get_local_path

from detectors.bom import Detector as BomDetector
from detectors.frequency import Detector as FrequencyDetector
from detectors.utf8 import Detector as Utf8Detector
from detectors.latin import Detector as LatinDetector
from detectors.mojibake import Detector as MojibakeDetector
from detectors.spanish import Detector as SpanishDetector


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            block = f.read(1024 * 1024)

            if not block:
                break
            h.update(block)
    return h.hexdigest()

def create_engine():
    """
    Crea el motor de análisis con todos los detectores.
    """

    engine = AnalyzerEngine()

    engine.add_detector(BomDetector())
    engine.add_detector(FrequencyDetector())
    engine.add_detector(Utf8Detector())
    engine.add_detector(LatinDetector())
    engine.add_detector(MojibakeDetector())
    engine.add_detector(SpanishDetector())

    return engine


def create_result(source, path):
    """
    Construye el AnalysisResult con los metadatos básicos.
    """

    result = AnalysisResult()

    result.source = source
    result.local_path = str(path)
    result.file_name = path.name
    result.file_path = str(path)
    result.file_size = path.stat().st_size
    result.sha256 = sha256(path)

    return result


def analyze(source, read_first_bytes=False):
    """
    Ejecuta todo el análisis y devuelve un AnalysisResult.

    source:
        Ruta local o URL.

    read_first_bytes:
        Si es True guarda los primeros 32 bytes para el reporte.
    """

    #
    # Resolver archivo local o descargar si es URL
    #
    download = get_local_path(source)
    path = download.local_path

    #
    # Guardar información del origen
    #
    result = create_result(
        source,
        path
    )

    result.download_info = download.metadata or {}

    #
    # Crear motor
    #
    engine = create_engine()

    #
    # Ejecutar análisis
    #
    engine.analyze(path, result)

    #
    # Leer primeros bytes (opcional)
    #

    if read_first_bytes:
        with open(path, "rb") as f:
            result.first_bytes = f.read(32)

    return result