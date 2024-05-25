from pathlib import Path
from dotenv import dotenv_values
from os import listdir

def parent_dir() -> str:
    """Return the parent directory, so the folder can be added as needed"""
    return str(Path("./").parent.absolute()).replace("\\transform","")

MAIN_DIR = parent_dir()

def get_config(path: str) -> dict:
    """Given the path of the .env file, file return the values as a dictionary"""
    return dotenv_values("../extract/dhelos_files.env")


def get_excels(path: str) -> list[str]:
    """From a path, returns only the files that ends with .xlsx"""
    return [file for file in listdir(path) if file.endswith(".xlsx")]