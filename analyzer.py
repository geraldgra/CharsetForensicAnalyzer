from cli import get_arguments

from reports.console import show as show_console
from reports.preview import show_preview
from reports.json_report import (
    show as show_json,
    save as save_json
)

from converters.utf8 import convert

from services.analyzer_service import analyze


def main():

    args = get_arguments()

    try:
        #
        # Ejecutar análisis
        #
        result = analyze(
            args.file,
            read_first_bytes=args.hex
        )

        #
        # Mostrar resultado
        #
        if args.output == "json":
            show_json(result)
        else:
            show_console(result)

        #
        # Conversión opcional
        #
        if args.convert == "utf8":
            convert(
                result,
                error_mode=args.errors
            )

        #
        # Preview
        #
        if args.preview:
            show_preview(result.local_path)

        #
        # Reporte JSON
        #
        if args.json:
            save_json(result)

    except Exception as ex:

        print()
        print(f"ERROR: {ex}")


if __name__ == "__main__":

    main()