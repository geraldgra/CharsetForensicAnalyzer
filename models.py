from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, UTC
from app import (
    APP_NAME,
    APP_VERSION,
    REPORT_SCHEMA
)


@dataclass
class Evidence:

    offset: int
    severity: str
    description: str
    hex_bytes: str = ""


@dataclass
class AnalysisResult:

    file_name: str = ""
    file_path: str = ""
    file_size: int = 0
    sha256: str = ""
    bom: str = ""

    first_bytes: bytes = b""
    utf8_valid: bool | None = None
    utf8_errors: int = 0
    extended_chars: int = 0
    
    total_bytes_analyzed: int = 0
    first_utf8_error_offset: int | None = None
    last_utf8_error_offset: int | None = None
    

    statistics: dict = field(default_factory=dict)
    byte_frequency: list = field(default_factory=lambda: [0] * 256)
    evidences: list = field(default_factory=list)


    windows1252_bytes: int = 0
    iso_control_bytes: int = 0
    likely_encoding: str = ""
    confidence: float = 0.0
    mojibake_patterns: dict = field(default_factory=dict)
    mojibake_count: int = 0
    null_bytes: int = 0
    control_bytes: int = 0
    undefined_bytes: dict = field(default_factory=dict)
    download_info: dict = field(default_factory=dict)

    #
    # Información del origen
    #

    source: str = ""
    local_path: str = ""

    def to_dict(self):

        report_file = Path(self.file_path).with_suffix(".json").name

        generated_at = (
            datetime
            .now(UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        return {

            "metadata": {
                "tool": APP_NAME,
                "tool_version": APP_VERSION,
                "schema": REPORT_SCHEMA,
                "report_encoding": "UTF-8",
                "json_report": report_file
            },
            "download": self.download_info,
            "source": self.source,
            "local_path": self.local_path,
            "file": self.file_name,
            "path": self.file_path,
            "size": self.file_size,
            "sha256": self.sha256,
            "bom": self.bom,
            "utf8": {
                "valid": self.utf8_valid,
                "errors": self.utf8_errors,
                "first_error": self.first_utf8_error_offset,
                "last_error": self.last_utf8_error_offset
            },
            "diagnostic": {
                "likely_encoding": self.likely_encoding,
                "confidence": self.confidence,
                "windows1252_bytes": self.windows1252_bytes,
                "undefined_bytes": self.iso_control_bytes
            },
            "mojibake": {
                "count": self.mojibake_count,
                "patterns": self.mojibake_patterns
            },
            "content": {
                "null_bytes": self.null_bytes,
                "control_bytes": self.control_bytes
            },
            "statistics": self.statistics,
            "undefined_details": {
                f"0x{k:02X}": {
                    "count": v["count"],
                    "offset": v["offset"],
                    "context_hex": v["context"].hex(" ")
                }
                for k, v in self.undefined_details.items()
            }
        }

    def to_json(self, indent=4):
        """
        Devuelve el análisis serializado en formato JSON.
        """

        import json

        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False
        )

@dataclass
class DownloadResult:
    """
    Resultado de obtener un archivo.

    Puede provenir del disco local
    o haber sido descargado desde Internet.
    """

    local_path: Path
    original_source: str = ""
    metadata: dict = field(default_factory=dict)