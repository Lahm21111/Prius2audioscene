import os
from typing import Dict

import numpy as np
import pandas as pd
from nav_msgs.msg import Odometry

from utils.utils import generate_token, get_unix_time

from .table import Table

schema = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
        "translation": {"type": "array"},
        "rotation": {"type": "array"},
        "timestamp": {"type": "number"},
    },
    "required": [
        "token",
        "translation",
        "rotation",
        "timestamp",
    ],
}


class EgoPose(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "ego_pose.json")

    def create_record(self, msg: Odometry) -> None:
        t = msg.pose.pose.position
        r = msg.pose.pose.orientation
        data = {
            "token": generate_token(),
            "translation": [t.x, t.y, 0],  # z is always 0
            "rotation": [r.w, r.x, r.y, r.z],
            "timestamp": get_unix_time(msg.header.stamp),
        }

        super().create_record(data)

    def find_closest_ego_pose_token(self, sample_timestamp):
        ego_poses_df = pd.DataFrame(self.records)
        # Ensure 'timestamp' is in the correct format for comparison
        ego_poses_df["timestamp"] = pd.to_datetime(ego_poses_df["timestamp"], unit="s")

        # Calculate the absolute difference between the sample timestamp and each ego pose timestamp
        time_diffs = np.abs(
            ego_poses_df["timestamp"] - pd.to_datetime(sample_timestamp, unit="s")
        )

        # Find the index of the minimum difference
        closest_index = time_diffs.idxmin()

        # Return the token of the closest ego pose
        return ego_poses_df.iloc[closest_index]["token"]
