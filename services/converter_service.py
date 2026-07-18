from converters.utf8 import convert
from storage.manager import StorageManager

storage = StorageManager()


def convert_to_utf8(
    result,
    error_mode="replace"
):

    converted_file = convert(
        result,
        error_mode=error_mode
    )

    if converted_file is None:
        return None

    return storage.save(
        converted_file
    )

    return storage.save(output_file)