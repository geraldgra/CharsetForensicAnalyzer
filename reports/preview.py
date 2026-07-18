from pathlib import Path


ENCODINGS = [

    ("Windows-1252", "cp1252"),
    ("ISO-8859-1", "latin1"),
    ("UTF-8", "utf-8"),
    ("UTF-8 (replace)", "utf-8"),
]


def show_preview(path, lines=10):

    print()
    print("=" * 60)
    print("VISTA PREVIA DEL CONTENIDO")
    print("=" * 60)

    for title, encoding in ENCODINGS:

        print()
        print("-" * 60)
        print(title)
        print("-" * 60)

        try:

            errors = "replace" if "replace" in title else "strict"

            with open(path, "r", encoding=encoding, errors=errors) as f:

                for _ in range(lines):

                    line = f.readline()

                    if not line:
                        break

                    print(line.rstrip())

        except UnicodeDecodeError as ex:

            print(f"[ERROR] {ex}")

        except Exception as ex:

            print(f"[ERROR] {ex}")