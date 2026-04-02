import os
from typing import Dict

from utils.utils import generate_token

from .scene import Scene
from .table import Table

schema = {
    "type": "object",
    "properties": {
        "next": {"type": "string"},  # done
        "prev": {"type": "string"},  # done
        "scene_token": {"type": "string"},  # done
        "timestamp": {"type": "number"},  # done
        "token": {"type": "string"},  # done
    },
    "required": ["next", "prev", "scene_token", "timestamp", "token"],
}


class Sample(Table):
    prev_sample = ""
    curr_sample = generate_token()
    next_sample = generate_token()

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "sample.json")

    def create_record(self, timestamp: float, scene: Scene) -> None:
        data = {
            "prev": Sample.prev_sample,
            "token": Sample.curr_sample,
            "next": Sample.next_sample,
            "timestamp": timestamp,
            "scene_token": scene.get_scene_token(),
        }

        Sample.prev_sample = Sample.curr_sample
        Sample.curr_sample = Sample.next_sample
        Sample.next_sample = generate_token()

        super().create_record(data)

    def get_last_token(self) -> str:
        return self.records[-1]["token"]
    
    def delete_next_last(self):
        self.records[-1]["next"]=""        
