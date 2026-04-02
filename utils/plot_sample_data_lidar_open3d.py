import open3d as o3d
import numpy as np
import os
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from pyquaternion import Quaternion

def transform_to_ego(annotation, ego_pose_record):
    """
    Transform a box from the global coordinate system to the ego vehicle coordinate system.

    Parameters
    ----------
    annotation : dict
        The annotation of the box, containing the keys 'translation' and 'rotation'.
    ego_pose_record : dict
        The ego pose, containing the keys 'translation' and 'rotation'.

    Returns
    -------
    center_in_ego : numpy array
        The center of the box in the ego vehicle coordinate system.
    quat_in_ego : pyquaternion.Quaternion
        The rotation of the box in the ego vehicle coordinate system.
    """
    
    ego_quat = Quaternion(ego_pose_record['rotation'])
    center_in_ego = np.array(annotation['translation']) - np.array(ego_pose_record['translation'])
    center_in_ego = np.dot(ego_quat.rotation_matrix.T, center_in_ego)
    quat_in_ego = Quaternion(ego_pose_record['rotation']).inverse*Quaternion(annotation['rotation'])
    return center_in_ego, quat_in_ego

if __name__ == "__main__":
    # Load NuScenes dataset
    nusc = NuScenes(version='v1.0-test', dataroot='output', verbose=True)
    my_scene = nusc.scene[0]
    # Select a sample
    first_sample_token = my_scene['first_sample_token']
    my_sample = nusc.get('sample', first_sample_token)


    my_scene = nusc.scene[0]

    # Load pointcloud and annotations
    ref_sd_token = my_sample['data']['LIDAR_TOP']
    ref_sd_record = nusc.get('sample_data', ref_sd_token)
    pcl_path = os.path.join(nusc.dataroot, ref_sd_record['filename'])
    pc = LidarPointCloud.from_file(pcl_path)
    points = pc.points.T
    points.shape

    pcd = o3d.geometry.PointCloud()
    #points = points[points[:, 0] >= 0]
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    annotation_tokens = my_sample["anns"]
    annotations = [nusc.get('sample_annotation', annotation_tokens[i]) for i in range(len(annotation_tokens))]
    ego_pose_token = ref_sd_record['ego_pose_token']
    ego_pose_record = nusc.get('ego_pose', ego_pose_token)
    # Convert annotations to Open3D format
    boxes = []
    for annotation in annotations:
        center_in_ego, quat_ego = transform_to_ego(annotation, ego_pose_record)
        new_size = [annotation['size'][1],annotation['size'][0],annotation['size'][2]] # Data is originally in nuscenes format (wlh)
        box = o3d.geometry.OrientedBoundingBox(center_in_ego,quat_ego.rotation_matrix, new_size)
        boxes.append(box)
    # Visualize pointcloud and annotations
    o3d.visualization.draw_geometries([pcd]+boxes+[o3d.geometry.TriangleMesh.create_coordinate_frame()])