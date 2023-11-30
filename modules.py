import os
from pathlib import Path
from typing import List


def init():
    os.chdir(Path(__file__).parent)


def get_data_string(name: str) -> List[str]:
    return open(f"data/{name}.txt", "r", encoding="utf8").read().splitlines()


def get_data(name: str, type: type) -> List:
    return list(map(type, get_data_string(name)))
