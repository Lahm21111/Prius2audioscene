import open3d as o3d
import numpy as np
import os
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from pyquaternion import Quaternion
from typing import List


def transform_points(mat, points):
    """Apply 4x4 homogenous coordinate transform to Nx3 points."""
    return mat[:3, :3].dot(points.T).T + mat[:3, 3][None]

def iter_keyframes_sorted(nusc: NuScenes, channel: str) -> List[str]:
    sds = []
    for s in nusc.sample:
        sd_tok = s["data"].get(channel)
        if not sd_tok: continue
        sd = nusc.get("sample_data", sd_tok)
        if not sd.get("is_key_frame", False): continue
        ep = nusc.get("ego_pose", sd["ego_pose_token"])
        sds.append((ep["timestamp"], sd_tok))
    sds.sort(key=lambda x: x[0])
    return [t for _, t in sds]

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
    nusc = NuScenes(version='v1.0-test', dataroot='/workspaces/Prius2audioscene/output2', verbose=True)
    my_scene = nusc.scene[0]
    sd_all = iter_keyframes_sorted(nusc, 'LIDAR_TOP')
    sd_tokens = sd_all[5:7] + sd_all[48:50]
    geoms=[o3d.geometry.TriangleMesh.create_coordinate_frame(size=2.0)]
    boxes = []

    for i, sd_tok in enumerate(sd_tokens):
        # my_sample = nusc.get("sample", sd_token)
        # # Do something with the sample data

        # # first_sample_token = my_scene['last_sample_token']
        # # my_sample = nusc.get('sample', first_sample_token)


        # my_scene = nusc.scene[0]

        # # Load pointcloud and annotations
        # ref_sd_token = my_sample['data']['LIDAR_TOP']
        # ref_sd_record = nusc.get('sample_data', ref_sd_token)
        pcl_path = nusc.get_sample_data_path(sd_tok)
        ref_sd_record = nusc.get('sample_data', sd_tok)
        pc = LidarPointCloud.from_file(pcl_path)
       
        ego_pose_token = ref_sd_record['ego_pose_token']
        ego_pose_record = nusc.get('ego_pose', ego_pose_token)

       
        # Translate the pointcloud to the ego vehicle coordinate system
        print(ego_pose_record['rotation'])        
        # ego_quat = Quaternion(ego_pose_record['rotation'][3], ego_pose_record['rotation'][0], ego_pose_record['rotation'][1], ego_pose_record['rotation'][2])
        ego_quat = Quaternion(ego_pose_record['rotation'])

        # Correct: first subtract translation (including0, 0] offset), then apply inverse rotation
        offset = np.array([94092, 61855, 0])
        
        translation = np.array(ego_pose_record['translation']) - offset

        # convert Open3D.o3d.geometry.PointCloud to numpy array
        points = pc.points.T
        points.shape

        pcd = o3d.geometry.PointCloud()
        #points = points[points[:, 0] >= 0]
        pcd.points = o3d.utility.Vector3dVector(points[:, :3])
        xyz_pcd = np.asarray(pcd.points)

        # First, set the TF from GNSS link to base link

        tf_gnss_to_base_4x4 = np.array([1.000, 0.000, -0.000,  1.289,
                                        -0.000 ,-0.000, -1.000,  0.013,
                                        -0.000, -1.000,  0.000,  0.435,
                                        0.000,  0.000,  0.000,  1.000]).reshape(4,4)
    
        tf_base_to_gnss_4x4 = np.array([-1.000, 0.000, -0.000,  1.289,
                                        -0.000 ,-0.000, -1.000,  0.435,
                                        -0.000, -1.000,  0.000,  0.013,
                                        0.000,  0.000,  0.000,  1.000]).reshape(4,4)
        
        # Now translate to ego vehicle coordinate system
        ego_pose_4x4 = np.eye(4)

        ego_pose_4x4[:3, :3] = ego_quat.rotation_matrix

        ego_pose_4x4[:3, 3] = translation

        ego_pose_base_4x4 = ego_pose_4x4 @ tf_gnss_to_base_4x4

        tf_lidar_to_ego_4x4 = ego_pose_4x4 @ tf_base_to_gnss_4x4

        xyz_temp = xyz_pcd.copy()

        xyz_new = transform_points(tf_lidar_to_ego_4x4, xyz_temp)
        
        pcd_ego = o3d.geometry.PointCloud()
        pcd_ego.points = o3d.utility.Vector3dVector(xyz_new)
        

        box_unit = o3d.geometry.OrientedBoundingBox(ego_pose_base_4x4[:3, 3], ego_pose_base_4x4[:3, :3], np.array([3, 1, 1]))
        box_unit.color = (1, 0, 0)

        # print(sd_tok)
        # print("Record")
        # print(ref_sd_record)
        # annotation_tokens =  ref_sd_record['anns']
        # print(f"Annotation tokens: {annotation_tokens}")
        # annotations = [nusc.get('sample_annotation', annotation_tokens[i]) for i in range(len(annotation_tokens))]

        # annotoation_boxes = []

        # for annotation in annotations:
        #     center_in_ego, quat_ego = transform_to_ego(annotation, ego_pose_record)
        #     new_size = [annotation['size'][1],annotation['size'][0],annotation['size'][2]] # Data is originally in nuscenes format (wlh)
        #     box = o3d.geometry.OrientedBoundingBox(center_in_ego,quat_ego.rotation_matrix, new_size)
        #     annotoation_boxes.append(box)
        # Visualize pointcloud and annotations
        o3d.visualization.draw_geometries([pcd]+[box_unit]+[o3d.geometry.TriangleMesh.create_coordinate_frame()])
        geoms.append(pcd_ego)
        boxes.append(box_unit)

        # o3d.visualization.draw_geometries([pcd_ego]+[o3d.geometry.TriangleMesh.create_coordinate_frame()])
        # visualize the frames so far
    o3d.visualization.draw_geometries(geoms+boxes)