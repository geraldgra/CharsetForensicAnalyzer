from pathlib import Path
from app import (
    APP_NAME,
    APP_VERSION,
    DESCRIPTION
)

def separator(title=None):
    """
    Imprime un separador visual entre secciones.
    """
    print()

    if title:
        print("-" * 60)
        print(title)
        print("-" * 60)
    else:
        print("-" * 60)


def show(result):
     
    # ==========================================================
    # CABECERA
    # ==========================================================

    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)

    print(f"Archivo : {result.file_name}")
    print(f"Ruta    : {Path(result.file_path).resolve()}")
    print(f"Tamaño  : {result.file_size:,} bytes")
    print(f"BOM     : {result.bom}")
    print(f"SHA256  : {result.sha256}")

    # ==========================================================
    # PRIMEROS BYTES
    # ==========================================================

    if result.first_bytes:

        separator("Primeros 32 bytes")

        print(result.first_bytes.hex(" "))

    # ==========================================================
    # UTF8
    # ==========================================================

    separator("UTF8")

    print(f"  Válido          : {result.utf8_valid}")
    print(f"  Errores         : {result.utf8_errors:,}")
    print(f"  Bytes analizados: {result.total_bytes_analyzed:,}")
    print(f"  Primer error    : {result.first_utf8_error_offset}")
    print(f"  Último error    : {result.last_utf8_error_offset}")

    # ==========================================================
    # ESTADÍSTICAS
    # ==========================================================

    separator("Estadísticas")

    for k, v in result.statistics.items():

        # Solo imprimir estadísticas numéricas
        if isinstance(v, int):

            print(f"  {k:15} {v:,}")

    # ==========================================================
    # FRECUENCIA DE BYTES
    # ==========================================================

    separator("Frecuencia de bytes (>127)")

    encontrados = False

    for i in range(128, 256):

        if result.byte_frequency[i]:

            encontrados = True

            print(f"  {i:02X} : {result.byte_frequency[i]:,}")

    if not encontrados:

        print("  No se encontraron bytes superiores a 127.")

    # ==========================================================
    # DIAGNÓSTICO
    # ==========================================================

    separator("Diagnóstico")

    print(f"  Encoding probable : {result.likely_encoding}")
    print(f"  Confianza         : {result.confidence:.1f}%")
    print(f"  Bytes Windows1252 : {result.windows1252_bytes:,}")
    print(f"  Bytes indefinidos : {result.iso_control_bytes:,}")

    if result.undefined_details:

        print()
        print("  Detalle de bytes incompatibles")

        for byte, info in result.undefined_details.items():

            print()
            print(f"    Byte           : 0x{byte:02X}")
            print(f"    Cantidad       : {info['count']:,}")
            print(f"    Primer offset  : {info['offset']:,}")
            print(f"    Contexto HEX   : {info['context'].hex(' ')}")
            ascii_text = ""

            for c in info["context"]:

                if 32 <= c <= 126:
                    ascii_text += chr(c)
                else:
                    ascii_text += "."

            print(f"    Contexto ASCII : {ascii_text}")

    # ==========================================================
    # MOJIBAKE
    # ==========================================================

    separator("Mojibake")

    print(f"  Patrones encontrados : {result.mojibake_count:,}")

    if result.mojibake_patterns:

        for pattern, count in result.mojibake_patterns.items():

            print(f"    {pattern} : {count:,}")

    else:

        print("  No se detectaron patrones conocidos.")

    # ==========================================================
    # CONTENIDO
    # ==========================================================

    separator("Contenido")

    print(f"  Bytes NULL       : {result.null_bytes:,}")
    print(f"  Controles ASCII  : {result.control_bytes:,}")

    # ==========================================================
    # CARACTERES ESPAÑOLES
    # ==========================================================

    separator("Caracteres españoles")

    spanish = result.statistics.get("spanish", {})

    if spanish:

        encontrados = False

        for c, count in spanish.items():

            if count:

                encontrados = True

                print(f"  {c} : {count:,}")

        if not encontrados:

            print("  No se encontraron caracteres acentuados.")

    else:

        print("  Estadística no disponible.")

    # ==========================================================
    # CONCLUSIÓN
    # ==========================================================

    separator("Conclusión")

    if result.utf8_valid:

        print("✓ El archivo es un UTF-8 válido.")

    else:

        print("✓ El archivo NO es un UTF-8 válido.")

    print(f"✓ El encoding más probable es: {result.likely_encoding}")

    if result.mojibake_count == 0:

        print("✓ No se detectó evidencia de doble codificación (mojibake).")

    else:

        print("⚠ Se detectaron patrones compatibles con mojibake.")

    if result.likely_encoding == "Windows-1252":

        print("✓ Se recomienda convertir el archivo a UTF-8 antes de utilizarlo en aplicaciones web.")

    elif result.likely_encoding.startswith("UTF"):

        print("✓ No es necesario convertir el archivo.")

    else:

        print("✓ Se recomienda revisar manualmente la codificación.")