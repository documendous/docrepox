import os
import pathlib


def str_to_bool(val: str) -> bool:
    return val.lower() == "true" if val else False


def get_extension(file_name: str) -> str:  # pragma: no coverage
    "Returns a file extension"
    return pathlib.Path(file_name).suffix.lower()


def get_name_and_ext(
    file_name: os.PathLike[str],
) -> tuple[str, str]:  # pragma: no coverage
    "Returns a file name and a file extension as a tuple"
    return os.path.splitext(file_name)
