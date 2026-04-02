import os

import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

from tables.calibrated_sensor import CalibratedSensor
from tables.sensor import Sensor
from utils.utils import get_unix_time


class LiDAR:
    def __init__(
        self,
        msg: PointCloud2,
        sensors: Sensor,
        calibrated_sensors: CalibratedSensor,
    ) -> None:
        sensor = sensors.get_sensor_by_frame_id(msg.header.frame_id)

        filename = self._get_filename(msg, sensor["channel"])

        # a sensor token at the last 
        self.data = {
            "fileformat": "pcd.bin",  # Assuming you want to save as PCD files
            "filename": filename,
            "height": 0,
            "width": 0,
            "filedata": self._get_points(msg),  # This will be a list of XYZ points
            "timestamp": get_unix_time(msg.header.stamp),
            "calibrated_sensor_token": calibrated_sensors.get_calibrated_sensor_token(
                sensor["token"]
            ),
        }

    def _get_filename(self, msg: PointCloud2, sensor_channel: str) -> str:
        if not sensor_channel:
            raise Exception(f"Sensor with frame {msg.header.frame_id} not found")

        # timestamp = str(int(get_unix_time(msg.header.stamp) * 1e9))
        timestamp = str(int(get_unix_time(msg.header.stamp) * 1e6))  # microseconds
        filename = os.path.join(
            "samples",
            sensor_channel,
            "rosbag__" + sensor_channel + "__" + timestamp + ".pcd.bin",
        )

        return filename

    def _get_points(self, msg: PointCloud2) -> np.ndarray:
        # Define the fields you expect in your PointCloud2 data
        field_names = ["x", "y", "z", "intensity"]

    
        points_np_1 = pc2.read_points(
             msg, skip_nans=True, field_names=field_names
        )

        # Convert the list of points into a numpy array
        points_np_1 = np.column_stack((points_np_1['x'], points_np_1['y'], points_np_1['z'], points_np_1['intensity'].astype(float)))
        # Ensure the array is of type np.float32 and has shape (N, 5)
        # points_np = np.array(points, dtype=np.float32)

        # Check the shape of your points array
        if points_np_1.shape[1] != 5:
            zeros = np.zeros((points_np_1.shape[0], 1))
            points_np_1 = np.hstack((points_np_1, zeros))
        return points_np_1.astype("float32")
