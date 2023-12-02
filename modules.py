import os
from pathlib import Path
from typing import List


class DataManager:
    def __init__(self, file):
        os.chdir(Path(file).parent)
        filename = os.path.basename(file)
        self.challenge = filename[:2]

    def get_data_string(self) -> List[str]:
        return (
            open(f"data/{self.challenge}.txt", "r", encoding="utf8").read().splitlines()
        )

    def get_data(self, type: type) -> List:
        return list(map(type, self.get_data_string()))
