import os.path as osp
from typing import Tuple

from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from PIL import Image
from pyquaternion import Quaternion
import numpy as np
from nuscenes.utils.geometry_utils import view_points


def map_pointcloud_to_image(
    nusc: NuScenes,
    pointsensor_token: str,
    camera_token: str,
) -> Tuple:
    """
    Given a point sensor (lidar/radar) token and camera sample_data token, load pointcloud and map it to the image
    plane.
    :param pointsensor_token: Lidar/radar sample_data token.
    :param camera_token: Camera sample_data token.
    :return (pointcloud <np.float: 2, n)>, coloring <np.float: n>, image <Image>).
    """

    cam = nusc.get("sample_data", camera_token)
    pointsensor = nusc.get("sample_data", pointsensor_token)
    pcl_path = osp.join(nusc.dataroot, pointsensor["filename"])
    modality = pointsensor["sensor_modality"]
    if modality == "lidar":
        pc = LidarPointCloud.from_file(pcl_path)
    else:
        raise Exception(f"Sensor with modality {modality} is not implemented")
    im = Image.open(osp.join(nusc.dataroot, cam["filename"]))

    # Points live in the point sensor frame. So they need to be transformed via global to the image plane.
    # First step: transform the pointcloud to the ego vehicle frame for the timestamp of the sweep.
    cs_record = nusc.get("calibrated_sensor", pointsensor["calibrated_sensor_token"])
    pc.rotate(Quaternion(cs_record["rotation"]).rotation_matrix)
    pc.translate(np.array(cs_record["translation"]))

    # Second step: transform from ego to the global frame.
    poserecord = nusc.get("ego_pose", pointsensor["ego_pose_token"])
    pc.rotate(Quaternion(poserecord["rotation"]).rotation_matrix)
    pc.translate(np.array(poserecord["translation"]))

    # Third step: transform from global into the ego vehicle frame for the timestamp of the image.
    poserecord = nusc.get("ego_pose", cam["ego_pose_token"])
    pc.translate(-np.array(poserecord["translation"]))
    pc.rotate(Quaternion(poserecord["rotation"]).rotation_matrix.T)

    # Fourth step: transform from ego into the camera.
    cs_record = nusc.get("calibrated_sensor", cam["calibrated_sensor_token"])
    pc.translate(-np.array(cs_record["translation"]))
    pc.rotate(Quaternion(cs_record["rotation"]).rotation_matrix.T)

    # Fifth step: actually take a "picture" of the point cloud.
    # Grab the depths (camera frame z axis points away from the camera).
    coloring = pc.points[2, :]

    # Take the actual picture (matrix multiplication with camera-matrix + renormalization).
    points = view_points(
        pc.points[:3, :], np.array(cs_record["camera_intrinsic"]), normalize=True
    )

    return points, coloring, im
