import os
from typing import Dict

from utils.utils import generate_token

from .table import Table

schema = {
    "type": "object",
    "properties": {
        "channel": {"type": "string"},  # done
        "modality": {"type": "string"},  # done
        "token": {"type": "string"},  # done
    },
    "required": ["channel", "modality", "token"],
}


class Sensor(Table):
    def __init__(self, sensors: Dict) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "sensor.json")

        self.frame_map = {}

        # save the name of the sensor and its modality, generate a token for each sensor
        for name, info in sensors.items():
            data = {
                "channel": name,
                "modality": self._get_modality(name),
                "token": generate_token(),
            }
            self.frame_map[info["FRAME"]] = data
            self.create_record(data)

    def _get_modality(self, name: str) -> str:
        if "CAM" in name:
            return "camera"
        elif "LIDAR" in name:
            return "lidar"
        elif "MICARRAY" in name:
            return "microphone_array"
        else:
            raise Exception(f"Could not find modality for sensor {name}")

    def get_nbr_sensors(self) -> int:
        return len(self.records)

    def get_sensor_by_frame_id(self, frame_id: str) -> Dict:
        try:
            sensor = self.frame_map[frame_id]
        except:
            raise Exception(f"Sensor with frame {frame_id} not found")

        return sensor
