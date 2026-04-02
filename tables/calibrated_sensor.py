import os
from typing import Dict

import numpy as np
from scipy.spatial.transform import Rotation as R

from messages.info import Info
from messages.transforms import TFBuffer
from utils.utils import generate_token

from .sensor import Sensor
from .table import Table

schema = {
    "type": "object",
    "properties": {
        "camera_intrinsic": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 3,
                "maxItems": 3,
            },
            "minItems": 0,
            "maxItems": 3,
        },
        "rotation": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 4,
            "maxItems": 4,
        },
        "sensor_token": {"type": "string"},  # done
        "token": {"type": "string"},
        "translation": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 3,
            "maxItems": 3,
        },
    },
    "required": [
        "camera_intrinsic",
        "rotation",
        "sensor_token",
        "token",
        "translation",
    ],
}


class CalibratedSensor(Table):

    def __init__(self, sensors: Sensor) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "calibrated_sensor.json")

        self.sensors = sensors
        self._create_sensor_token_map(sensors)
        print(self._sensor_token_map)

        self.cam_info = {}

    def create_record(self, frame_id: str, tfbuffer: TFBuffer) -> None:
        sensor = self.sensors.get_sensor_by_frame_id(frame_id)
        cal_sensor_token = self.get_calibrated_sensor_token(sensor["token"])
        tf = tfbuffer.get_transform(
            # "axle_edgar_rearcenterground",
            "base_link",
            frame_id,
        )
        t = tf.transform.translation
        r = tf.transform.rotation
        data = {
            "sensor_token": sensor["token"],
            "token": cal_sensor_token,
            "translation": [t.x, t.y, t.z],
            "rotation": [r.w, r.x, r.y, r.z],
            "camera_intrinsic": self.cam_info.get(cal_sensor_token, []),
        }
        super().create_record(data)

    def _create_sensor_token_map(self, sensors: Sensor) -> None:
        self._sensor_token_map = {
            sensor["token"]: generate_token() for sensor in sensors.records
        }

    def get_calibrated_sensor_token(self, sensor_token: str) -> str:
        return self._sensor_token_map[sensor_token]

    def create_cam_info(self, info: Info) -> None:
        sensor_token = self.sensors.get_sensor_by_frame_id(info.frame_id)["token"]
        print(sensor_token)
        cal_sensor_token = self.get_calibrated_sensor_token(sensor_token)

        self.cam_info[cal_sensor_token] = info.camera_intrinsic
