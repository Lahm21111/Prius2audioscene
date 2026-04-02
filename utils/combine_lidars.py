from typing import Dict

import numpy as np
import open3d as o3d
import pandas as pd
import rclpy

from messages.transforms import TFBuffer

from .utils import get_file_timestamp

from utils.config import Config




def combine_lidars_to_top(
    df: pd.DataFrame,
    tf_buffer: TFBuffer,
    conf: Config,
    #sensor_dict: Dict,
    # {
    #     "LIDAR_TOP": "base_link",
    #     # "LIDAR_REAR": "lidar_innovusion_rear",
    #     # "LIDAR_LEFT": "lidar_ouster_left",
    #     # "LIDAR_RIGHT": "lidar_ouster_right",
    # },
):
    sensor_dict = conf.lidars
    lidars=conf.lidars
    key_frame_df = df[(df["is_key_frame"] == True) & (df["fileformat"] == "pcd.bin")]

    grouped_df = key_frame_df.groupby(by="sample_token")
    for _, group in grouped_df:
        assert (
            # group.shape[0] == 1
            group.shape[0]
            == len(lidars)
        ), "There should be exactly 1(if concatenated) or 4 lidars for each sample token!"

        # find the lidar top row and use lidar_top as combination base
        lidar_top_index = group[
            group["filename"].str.contains("LIDAR_TOP")
        ].index.values.astype(int)[0]

        all_pc_list = []
        for sensor_name, frame_id in sensor_dict.items():
            point, filename = _extract_pointcloud(group, sensor_name)
            # use open3d for transformation
            o3d_pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(point[:, :3]))
            ros_time = rclpy.time.Time()

            transformed_o3d_pc = _transform_o3d_pc(
                o3d_pc,
                source_frame=frame_id,
                target_frame="base_link",
                tf_buffer=tf_buffer,
                ros_time=ros_time,
            )

            point[:, :3] = np.asarray(transformed_o3d_pc.points)
            all_pc_list.append(point)

        # combine all point clouds into one array
        all_points = np.vstack(all_pc_list)
        df.at[lidar_top_index, "filedata"] = all_points

    return df


def _extract_pointcloud(df: pd.DataFrame, sensor_type: str):
    pc_row = df[df["filename"].str.contains(sensor_type)]

    pc = pc_row["filedata"].values
    point = np.vstack(pc)
    filename = pc_row["filename"].values.astype(str)[0]

    return point, filename


def _transform_o3d_pc(
    o3d_pc: o3d.geometry.PointCloud,
    source_frame: str,
    target_frame: str,
    tf_buffer: TFBuffer,
    ros_time: rclpy.time.Time,
) -> o3d.geometry.PointCloud:

    transformation_matrix = tf_buffer.get_transformation_matrix(
        source_frame=source_frame, target_frame=target_frame, ros_time=ros_time
    )
    return o3d_pc.transform(transformation_matrix)
