import sys


def info(message):
    """
    Mensajes informativos.

    Se envían a STDERR para no contaminar la salida
    principal (STDOUT), especialmente cuando el
    usuario solicita JSON.
    """

    print(
        message,
        file=sys.stderr
    )

def blank():
    """
    Inserta una línea en blanco en STDERR.
    """

    print(file=sys.stderr)