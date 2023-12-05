import os
from pathlib import Path
from typing import List


class DataManager:
    def __init__(self, file):
        os.chdir(Path(file).parent)
        filename = os.path.basename(file)
        self.challenge = filename[:2]

    def get_data_string(self, day=None) -> List[str]:
        if day:
            self.challenge = day
        with open(f"data/{self.challenge}.txt") as f:
            return [line.strip() for line in f.readlines()]

    def get_data(self, type: type) -> List:
        return list(map(type, self.get_data_string()))
