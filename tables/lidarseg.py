import os
from typing import Dict

from utils.utils import create_dir

from .table import Table

schema = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
        "sample_data_token": {"type": "string"},
        "filename": {"type": "string"},
    },
    "required": [
        "token",
        "sample_data_token",
        "filename",
    ],
}


class LidarSeg(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "lidarseg.json")
        self.output_path = "lidarseg/v1.0-test/"

        create_dir(os.path.join("output", self.output_path))
