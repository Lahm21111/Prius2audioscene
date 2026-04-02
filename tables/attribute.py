import os

from .table import Table

schema = {
    "type": "object",
    "properties": {},
    "required": [],
}


class Attribute(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "attribute.json")
