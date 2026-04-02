import os
import tqdm
import json
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from utils import read_json, create_dir, generate_token, get_token_if_column_contains_string, get_token_if_column_is_string, write_json, get_column_if_token

class Annotator:
    def __init__(self, data_path="dataset/output/",lidar_sensor="LIDAR_TOP", pcd_prefix="rosbag__", version="v1.0-test", threshold=0.4):
        """
        Constructor for Annotator class.

        Args:
        data_path (str): Path to the folder containing the annotations.
        lidar_sensor (str): Name of the lidar sensor.
        pcd_prefix (str): Prefix for the point cloud files.

        Attributes:
        data_path (str): Path to the folder containing the annotations.
        lidar_sensor (str): Name of the lidar sensor.
        pcd_prefix (str): Prefix for the point cloud files.
        sample_data_df (pd.DataFrame): DataFrame containing the sample data.
        """
        self.data_path = data_path
        self.dataset_version = version
        self.lidar_sensor = lidar_sensor
        self.pcd_prefix = f"{pcd_prefix}{self.lidar_sensor}__"
        self.sample_data_df = pd.read_json(os.path.join(self.data_path, self.dataset_version, "sample_data.json"))
        self.sample_annotation_path = os.path.join(self.data_path, self.dataset_version, "sample_annotation.json")
        self.pseudo_sample_result_path = os.path.join(self.data_path, self.dataset_version, "pseudo_sample_result.json")
        self.sample_df = pd.read_json(os.path.join(self.data_path, self.dataset_version, "sample.json"))
        self.category_df = pd.read_json(os.path.join(self.data_path, self.dataset_version, "category.json"))
        self.visibility_df = pd.read_json(os.path.join(self.data_path, self.dataset_version, "visibility.json"))
        self.ego_pose_df = pd.read_json(os.path.join(self.data_path, self.dataset_version, "ego_pose.json"))
        self.threshold = threshold
        self.class_mapping = {0:"vehicle.car", 1:"human.pedestrian.adult", 2:"vehicle.bicycle", 3:"ignore"} # TODO: Know what happens with the classes in MS3D
    def read_multiple_annotations(self):
        # Check if the PCD file exists
        """
        Reads multiple annotation pickles from a directory and merges them into a single dictionary.
        
        Args:
            pickles_path (str): Path to the directory containing the annotation pickles.
        
        Returns:
            dict: A dictionary containing the merged annotations.
        """
        pickles_path = os.path.join(self.data_path,"labels")
        print(pickles_path)
        if not os.path.exists(pickles_path):
            print(f"Folder not found: {pickles_path}")
            return
        annotations = {}     
        for filename in os.listdir(pickles_path):
            pickle_filepath = os.path.join(pickles_path,filename)
            annotation = self.read_annotation(pickle_filepath)
            annotations.update(annotation)
        return annotations

    def read_annotation(self,pickle_path):
        # Check if the PCD file exists
        """
        Reads a single annotation pickle from a file path.

        Args:
            pickle_path (str): Path to the annotation pickle file.

        Returns:
            dict: A dictionary containing the annotation.
        """
        print(pickle_path)
        if not os.path.exists(pickle_path):
            print(f"Folder not found: {pickle_path}")
            return     
        result = pd.read_pickle(pickle_path)
        return result


    def process_annotations(self,annotation_dictionary):
        """
        Process multiple annotations and writes the annotation and instance data to the JSON files.

        Args:
            annotation_dictionary (dict): A dictionary containing the annotations, where the key is the timestamp and the value is a dictionary containing the annotations.

        Returns:
            None
        """
        annotation_to_json = []
        instance_to_json = []
        result_to_json = []
        for timestamp, annotations in tqdm.tqdm(annotation_dictionary.items(),):
            sample_annotation_data, instance_data, result_annotation_data = self.process_sample_annotation(timestamp, annotations)
            if sample_annotation_data is None and instance_data is None and result_annotation_data is None:
                continue
            annotation_to_json.extend(sample_annotation_data)
            instance_to_json.extend(instance_data)
            result_to_json.extend(result_annotation_data)
        write_json(os.path.join(self.data_path,self.dataset_version,"pseudo_sample_annotation.json"),annotation_to_json)
        write_json(os.path.join(self.data_path,self.dataset_version,"pseudo_instance.json"),instance_to_json)
        
        results_json = self.create_final_results_format(result_to_json)
        write_json(self.pseudo_sample_result_path, results_json)
    
    def create_final_results_format(self, results_list):
        meta_data = {"use_camera": False, "use_lidar": True, "use_radar": False, "use_map": False, "use_external": False}
        results_dict = {}
        anno = {
            "meta": meta_data,
            "results": results_dict
        }
        # Iterate over results list
        for result in results_list:
            if result["sample_token"] not in results_dict:
                results_dict[result["sample_token"]] = [result]
            else:
                results_dict[result["sample_token"]].append(result)

        # Fill up empty sample_tokens
        sample_annotation_sample_tokens = [item["sample_token"] for item in read_json(os.path.join(self.data_path, self.dataset_version, "sample_annotation.json"))]
        for sample_token in sample_annotation_sample_tokens:
            if sample_token not in results_dict.keys():
                print("Added empty token", sample_token)
                results_dict[sample_token] = []
        return anno

    def process_sample_annotation(self, timestamp,annotations):
        """
        Process a single sample annotation.

        Args:
            timestamp (int): The timestamp for the sample annotation.
            annotations (dict): A dictionary containing the annotations for the sample.

        Returns:
            tuple: A tuple containing two lists. The first list contains the sample annotation data in the format of the nuScenes dataset. The second list contains the instance data in the format of the nuScenes dataset.
        """
        sample_annotation_data = []
        instance_data = []
        result_data = []
        pcd_filename = f"{self.pcd_prefix}{timestamp}.pcd.bin"
        pcd_filepath = os.path.join(self.data_path,"samples",self.lidar_sensor,pcd_filename)
        if not os.path.exists(pcd_filepath):
            # In annotated edgar data, the "timestamp" is actually the .pcd file name
            pcd_filename = f"{timestamp}.bin"
            pcd_filepath = os.path.join(self.data_path,"samples",self.lidar_sensor,pcd_filename)
            if not os.path.exists(pcd_filepath):
                print(f"File not found: {pcd_filepath}")
                return None, None, None
        sample_data_token = get_token_if_column_contains_string(self.sample_data_df,"filename",pcd_filename)
        sample_token = get_column_if_token(self.sample_data_df,"sample_token",sample_data_token)
        if sample_token is None:
            return None, None, None
        for box_annotation in annotations["gt_boxes"]:
            box_entry, instance_entry, result_entry = self.process_box_annotation(box_annotation, sample_token, sample_data_token)
            if box_entry is None and instance_entry is None and result_entry is None:
                continue
            sample_annotation_data.append(box_entry)
            instance_data.append(instance_entry)
            result_data.append(result_entry)
        return sample_annotation_data, instance_data, result_data
    
    def process_box_annotation(self,box_annotation, sample_token, sample_data_token):
        """
        Process a single box annotation.

        Args:
        box_annotation (dict): Dictionary containing the annotation information.
        sample_token (str): Token for the sample containing the annotation.
        sample_data_token (str): Token for the sample data containing the annotation.

        Returns:
        tuple: A tuple containing the sample annotation data and instance annotation data.
        The sample annotation data is a dictionary with the following keys:
        - token (str): Unique token for the sample annotation.
        - sample_token (str): Token for the sample containing the annotation.
        - instance_token (str): Token for the instance annotation.
        - visibility_token (str): Token for the visibility information.
        - attribute_tokens (list): List of tokens for the attributes.
        - translation (list): List containing the x, y, z coordinates of the box center.
        - size (list): List containing the length, width, height of the box.
        - rotation (list): List containing the quaternion representation of the box rotation.
        - num_lidar_pts (int): Number of lidar points in the box.
        - num_radar_pts (int): Number of radar points in the box.
        - prev (str): Token for the previous annotation in the sequence.
        - next (str): Token for the next annotation in the sequence.

        The instance annotation data is a dictionary with the following keys:
        - token (str): Unique token for the instance annotation.
        - category_token (str): Token for the category of the instance.
        - nbr_annotations (int): Number of annotations in the instance.
        - first_annotation_token (str): Token for the first annotation in the instance.
        - last_annotation_token (str): Token for the last annotation in the instance.
        """
        ego_pose = self.get_ego_pose(sample_data_token)
        center,lwh,rot,label,score = self.extract_box_information(box_annotation, ego_pose)
        category_token = get_token_if_column_is_string(self.category_df,"name",self.class_mapping[label])
        if score < self.threshold:
             return None, None, None
        box_token = generate_token()
        instance_token = generate_token()
        box_annotation = {
            "token": box_token,
            "sample_token": sample_token,
            "instance_token": instance_token,  # Generate a new instance token for each annotation
            "visibility_token": "",  # Assuming visibility info is available
            "attribute_tokens": [],  # Assuming attributes are available
            "translation": center,
            "size": lwh,
            "rotation": rot,
            "num_lidar_pts": 10,
            "num_radar_pts": 10,
            "prev":"",
            "next": ""  # Update if there is a link to the next annotation
        }
        instance_annotation = {
            "token": instance_token,
            "category_token": category_token,
            "nbr_annotations": 1,
            "first_annotation_token": box_token,
            "last_annotation_token": box_token

        }
        result_annotation = {
            "sample_token": sample_token,
            "translation": center,
            "size": lwh,
            "rotation": rot,
            "velocity": [0,0],
            "detection_name": self.class_mapping[label],
            "detection_score": score,
            "attribute_name": ""
        }
        return box_annotation, instance_annotation, result_annotation
    
    def extract_box_information(self,annotation, ego_pose):
        """
        Extract the information from the box annotation into a standardized format.
        The input annotation is a list of floats where
        [0, 1, 2] are the center of the box in the lidar coordinate system (x, y, z)
        [3, 4, 5] are the length, width, and height of the box
        [6] is the yaw angle of the box in radians
        [7] is the score of the box
        [8] is the label of the box
        The output is a tuple of (center, size, rotation, label, score)
        where center is a list of floats [x, y, z] of the center of the box
        size is a list of floats [width,length, height] (Nuscenes Format)
        rotation is a list of floats [scalar-first quaternion]
        label is an integer of the label of the box
        score is a float of the score of the box
        """
        label = np.float64(annotation[-2])
        score = np.float64(annotation[8])
        center = [np.float64(annotation[0]),np.float64(annotation[1]),np.float64(annotation[2])]
        lwh = np.float64(annotation[3:6] * 1)
        wlh = lwh[[1, 0, 2]].tolist()
        # add a small value to avoid division by zero and assumes no pitch and roll
        axis_angles = np.array([0, 0, annotation[6] + 1e-10]) 
        ## TODO: CHECK
        rot = Rotation.from_euler('xyz', axis_angles, degrees=False)
        center, rot = transform_to_global(ego_pose, center, rot)
        rot_list = rot.as_quat(scalar_first=True).tolist()
        return center.tolist(), wlh, rot_list, label, score

    def get_ego_pose(self,sample_data_token):
        """
        Get the ego pose from the sample data token.

        Parameters
        ----------
        sample_data_token : str
            The token of the sample data.

        Returns
        -------
        ego_pose : pd.DataFrame
            The ego pose of the sample data.
        """
        sample_data = self.sample_data_df[self.sample_data_df["token"] == sample_data_token]
        ego_pose_token = sample_data["ego_pose_token"].values[0]
        ego_pose = self.ego_pose_df[self.ego_pose_df["token"] == ego_pose_token]
        return ego_pose

    def eval(self, version="v1.0-test", output_path="./"):
        from nuscenes.nuscenes import NuScenes
        from nuscenes.eval.detection.config import config_factory
        from custom_evaluate import CustomDetectionEval

        nusc = NuScenes(version=version, dataroot=self.data_path, verbose=True)
        nusc_eval = CustomDetectionEval(
            nusc,
            config=config_factory("detection_cvpr_2019"),
            result_path=self.pseudo_sample_result_path,
            eval_set="edgar", # trigger reading scene names from splits.json
            output_dir=output_path,
            verbose=True,
        )
        metrics_summary = nusc_eval.main(plot_examples=0, render_curves=False)
        metrics_summary_agnostic = nusc_eval.main_agnostic(plot_examples=0, render_curves=False)

def transform_to_global(ego_pose, center, rot):
    """
    Transform a box from the ego pose coordinate system to the map coordinate system.

    Parameters
    ----------
    ego_pose : pd.DataFrame
        The ego pose of the sample data.
    center : list
        The center of the box in the ego pose coordinate system.
    rot : Rotation
        The rotation of the box in the ego pose coordinate system.

    Returns
    -------
    center_in_map : list
        The center of the box in the map coordinate system.
    rot_in_map : Rotation
        The rotation of the box in the map coordinate system.
    """
    center_in_ego = np.dot(Rotation.from_quat(ego_pose["rotation"].values[0], scalar_first=True).as_matrix(), center)
    center_in_map = np.array(center_in_ego) + np.array(ego_pose["translation"].values[0])
    rot_in_map = Rotation.from_quat(ego_pose["rotation"].values[0], scalar_first=True)*rot
    return center_in_map, rot_in_map 



def main():
    print("###########")
    print("Processing Annotations")
    annotator = Annotator(lidar_sensor="LIDAR_TOP")
    annotations_dictionary = annotator.read_multiple_annotations()
    annotator.process_annotations(annotations_dictionary)
    print("###########")
    print("Done processing annotations")
    # if os.path.exists(annotator.sample_annotation_path):
    #     print("###########")
    #     print("Evaluating pseudo sample annotations")
    #     annotator.eval()
    #     print("Done evaluation")
    #     print("###########")

        
if __name__ == "__main__":
    main()
