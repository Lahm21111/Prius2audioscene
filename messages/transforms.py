from typing import Dict

import numpy as np
import rclpy
import yaml
from scipy.spatial.transform import Rotation
from tf2_msgs.msg import TFMessage
from tf2_ros import Buffer, TransformStamped


class TFBuffer:
    def __init__(self) -> None:
        self.tf_buffer = Buffer(cache_time=rclpy.duration.Duration(seconds=0))

        lidar_top_tf = TransformStamped()

        # Populate the fields of the TransformStamped message
        lidar_top_tf.transform.translation.x = 0.985793
        lidar_top_tf.transform.translation.y = 0.0
        lidar_top_tf.transform.translation.z = 1.84019

        lidar_top_tf.transform.rotation.x = -0.006492242056004365
        lidar_top_tf.transform.rotation.y = 0.010646214713995808
        lidar_top_tf.transform.rotation.z = -0.7063073142877817
        lidar_top_tf.transform.rotation.w = 0.7077955119163518

        # Set the frame_id and child_frame_id
        # lidar_top_tf.header.frame_id = "axle_edgar_rearcenterground"
        lidar_top_tf.header.frame_id = "base_link"
        lidar_top_tf.child_frame_id = "lidar_top"

        # Add the transform to the buffer
        self.tf_buffer.set_transform_static(lidar_top_tf, "default_authority")

    def process_tf_message(self, msg: TFMessage) -> None:
        current_time = rclpy.time.Time().to_msg()
        for transform in msg.transforms:
            transform.header.stamp = current_time
            self.tf_buffer.set_transform_static(transform, "default_authority")

    def get_transform(
        self,
        target_frame: str,
        source_frame: str,
        ros_time: rclpy.time.Time = rclpy.time.Time(),
    ) -> TransformStamped:
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                ros_time,
            )
        except:
            try:
                transform = self.tf_buffer.lookup_transform(
                    target_frame, self._get_full_frame(source_frame), ros_time
                )
            except Exception as e:
                transform = TransformStamped()
                transform.header.stamp = ros_time.to_msg()
                transform.header.frame_id = target_frame     
                transform.child_frame_id = source_frame       
                transform.transform.translation.x = 0.0
                transform.transform.translation.y = 0.0
                transform.transform.translation.z = 0.0
                transform.transform.rotation.x = 0.0
                transform.transform.rotation.y = 0.0
                transform.transform.rotation.z = 0.0
                transform.transform.rotation.w = 1.0

        return transform

    def _get_frame_list(self) -> Dict:
        all_frames_yaml = self.tf_buffer.all_frames_as_yaml()
        return yaml.safe_load(all_frames_yaml)

    def _get_full_frame(self, frame: str) -> str:
        mapping = {
            "cam_fc": "camera_sr_front_center",
            "cam_fl": "camera_sr_front_left",
            "cam_fr": "camera_sr_front_right",
            "cam_rc": "camera_sr_rear_center",
            "cam_rl": "camera_sr_rear_left",
            "cam_rr": "camera_sr_rear_right",
        }
        return mapping.get(frame, frame)

    def get_transformation_matrix(
        self,
        target_frame: str,
        source_frame: str,
        ros_time: rclpy.time.Time = rclpy.time.Time(),
    ):
        ts = self.get_transform(target_frame, source_frame, ros_time)
        q = [
            ts.transform.rotation.x,
            ts.transform.rotation.y,
            ts.transform.rotation.z,
            ts.transform.rotation.w,
        ]
        t = [
            ts.transform.translation.x,
            ts.transform.translation.y,
            ts.transform.translation.z,
        ]
        # Combine to form the transformation matrix and apply the transformation
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = Rotation.from_quat(q).as_matrix()
        transform_matrix[:3, 3] = t

        return transform_matrix
