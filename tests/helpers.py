import pathlib


def folder_path(file: str):
    return pathlib.Path(file).parent
