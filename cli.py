import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        prog="Charset Forensic Analyzer",
        description="Analiza archivos para determinar su codificación y detectar problemas de encoding."
    )

    parser.add_argument(
        "file",
        help="Ruta del archivo a analizar."
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Muestra información adicional durante el análisis."
    )

    parser.add_argument(
        "--hex",
        action="store_true",
        help="Muestra los primeros bytes del archivo en hexadecimal."
    )

    parser.add_argument(
    "--preview",
    action="store_true",
    help="Muestra una vista previa del archivo usando varios encodings."
    )

    parser.add_argument(
    "--convert",
    choices=["utf8"],
    help="Convierte el archivo al encoding indicado."
    )
 
    parser.add_argument(
    "--errors",
    choices=["strict", "ignore", "replace"],
    default="strict",
    help="Cómo tratar caracteres no representables durante la conversión."
    )

    parser.add_argument(
    "--json",
    action="store_true",
    help="Genera un archivo JSON con el resultado del análisis."
    )

    parser.add_argument(
    "--output",
    choices=["text","json"],
    default="text",
    help="Formato de salida por consola."
    )
    
    return parser.parse_args()