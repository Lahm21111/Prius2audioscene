import os
import numpy as np

from utils.utils import get_unix_time
from tables.calibrated_sensor import CalibratedSensor
from tables.sensor import Sensor


class AudioArray:
    """
    Wrapper class for converting an audio array ROS message into
    a NuScenes-style sample_data record containing a numpy array.
    """

    def __init__(
        self,
        msg,
        sensors: Sensor,
        calibrated_sensors: CalibratedSensor,
        timestamp,
    ) -> None:

        # Get the logical sensor entry based on its frame_id
        sensor = sensors.get_sensor_by_frame_id("cae_micarray")

        # Construct filename based on channel & timestamp
        filename = self._get_filename(msg, sensor["channel"],timestamp)
        print(msg.shape)
        # Build data structure similar to LiDAR
        self.data = {
            "fileformat": "npy",  # audio saved as numpy array
            "filename": filename,
            "height": 0,
            "width": 0,
            "timestamp": round(timestamp*1e-9, 6),
            "filedata": msg,  # numpy array
            "calibrated_sensor_token": calibrated_sensors.get_calibrated_sensor_token(
                sensor["token"]
            ),
        }

    def _get_filename(self, msg, sensor_channel: str,timestamp) -> str:
        """
        Construct the filename for saving the audio numpy array.
        """
        if not sensor_channel:
            raise Exception(f"Sensor with frame {msg.header.frame_id} not found")

        timestamp = str(int(timestamp * 1e-3))  # microseconds

        filename = os.path.join(
            "samples",
            sensor_channel,
            "rosbag__" + sensor_channel + "__" + timestamp + ".npy",
        )
        return filename

