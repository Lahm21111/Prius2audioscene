import os
from typing import Dict

from utils.utils import generate_token

from .table import Table
from .log import Log

schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},  # done
        "first_sample_token": {"type": "string"},  # done
        "last_sample_token": {"type": "string"},  # done
        "log_token": {"type": "string"},  # done
        "name": {"type": "string"},  # done
        "nbr_samples": {"type": "number"},  # done
        "token": {"type": "string"},  # done
    },
    "required": [
        "description",
        "first_sample_token",
        "last_sample_token",
        "log_token",
        "name",
        "nbr_samples",
        "token",
    ],
}


class Scene(Table):

    def __init__(self, bag: Dict) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "scene.json")

        self.token = generate_token()
        self.data = {
            "description": bag["DESCRIPTION"],
            "log_token": "",
            "name": bag["NAME"],
            "token": self.token,
        }

    def get_scene_token(self) -> str:
        return self.token

    def complete(
        self,
        first_sample_token: str,
        last_sample_token: str,
        nbr_samples: int,
        log_token: str,
    ):
        self.data["first_sample_token"] = first_sample_token
        self.data["last_sample_token"] = last_sample_token
        self.data["nbr_samples"] = nbr_samples
        self.data["log_token"] = log_token

        self.create_record(self.data)
