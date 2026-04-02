import json
import os
from typing import Dict

from jsonschema import validate

from utils.utils import create_dir, read_json


class Table:
    def __init__(self) -> None:
        self.records = []
        self._path = "output/v1.0-test"
        self._schema = None

    def create_record(self, data: Dict) -> None:
        if self._schema is None:
            raise Warning(f"Missing schema for {type(self)}")
        validate(data, self._schema)

        self.records.append(data)

    def copy_nuscenes_records(self, nuscenes_path: os.PathLike) -> None:
        self.records = []

        for record in read_json(nuscenes_path):
            self.create_record(record)

    def write_table(self) -> None:
        create_dir(self._path)
        print("The table is written to:", self._path)

        with open(self._path, "w+") as file:
            json.dump(self.records, file, indent=4)
