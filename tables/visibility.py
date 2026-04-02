import os
from typing import Dict

from .table import Table

schema = {
    "type": "object",
    "properties": {},
    "required": [],
}


class Visibilty(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "visibility.json")
