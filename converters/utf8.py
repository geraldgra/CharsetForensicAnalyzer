from pathlib import Path


def convert(result, error_mode="strict", verbose=True):
    #
    # Validación de bytes incompatibles
    #

    undefined_count = 0

    for info in result.undefined_details.values():

        undefined_count += info["count"]

    if undefined_count and error_mode == "strict":

        if verbose:
            print()
            print("=" * 60)
            print("CONVERSIÓN CANCELADA")
            print("=" * 60)

            print()
            print(
                f"Se encontraron {undefined_count:,} byte(s) incompatibles "
                "con el encoding detectado."
            )

            print()
            print(
                "Use '--errors replace' o '--errors ignore' "
                "si desea continuar."
            )

        raise ValueError(
            "El archivo contiene bytes incompatibles. "
            "Utilice error_mode='replace' o 'ignore'."
        )
    
    """
    Convierte el archivo detectado a UTF-8.

    Nunca modifica el archivo original.
    """

    #
    # Determinar el encoding de origen
    #

    if result.likely_encoding == "Windows-1252":

        source_encoding = "cp1252"

    elif result.likely_encoding.startswith("ISO-8859-1"):

        source_encoding = "latin1"

    elif result.likely_encoding.startswith("UTF-8"):

        if verbose:
            print("El archivo ya está en UTF-8.")
        raise ValueError(
            "El archivo ya se encuentra codificado en UTF-8."
        )

    else:

        if verbose:
            print("No fue posible determinar el encoding.")
        raise ValueError(
            "No fue posible determinar el encoding del archivo."
        )

    source = Path(result.file_path)

    suffix = "_utf8"

    if error_mode != "strict":
        suffix += "_" + error_mode

    destination = source.with_name(
        source.stem + suffix + source.suffix
    )

    #
    # Conversión
    #

    with open(
        source,
        "r",
        encoding=source_encoding,
        errors=error_mode
    ) as src:

        text = src.read()

    with open(destination, "w", encoding="utf-8", newline="") as dst:

        dst.write(text)

    print()
    print("=" * 60)
    print("CONVERSIÓN FINALIZADA")
    print("=" * 60)

    print(f"Origen            : {source}")
    print(f"Destino           : {destination}")
    print(f"Encoding origen   : {source_encoding}")
    print(f"Modo de errores   : {error_mode}")
    print(f"Bytes conflictivos: {undefined_count:,}")

    #
    # Verificación rápida
    #

    try:

        with open(destination, "r", encoding="utf-8") as f:
            f.read()
        print("Verificación      : OK (UTF-8 válido)")

    except UnicodeDecodeError:
        print("Verificación      : ERROR")

    return destination