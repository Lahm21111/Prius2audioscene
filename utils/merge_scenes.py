from add_scene import merge_folders, update_json_file
import os
import sys
import shutil
import tqdm 
"""
    Main function to merge scenes from a specified directory into a single directory.

    This script takes two command-line arguments:
    1. edgar_scenes_name: The name of the directory where the merged scenes will be stored.
    2. separated_scenes_path: The path to the directory containing the separated scenes.

    The function performs the following steps:
    1. Checks if the correct number of command-line arguments are provided.
    2. Constructs the path for the edgar_scenes directory.
    3. Creates the edgar_scenes directory if it does not exist, otherwise exits with an error. Avoids undesired overwritting
    4. Checks if the separated_scenes_path exists, otherwise exits with an error.
    5. Lists and sorts the scenes in the separated_scenes_path.
    6. Iterates through each scene directory and merges it into the edgar_scenes directory.
       - The first scene is copied entirely.
       - Subsequent scenes are merged using the merge_scenes function.
    
    Prints progress and error messages during the merging process.

    Usage:
        python merge_scenes.py <edgar_scenes_name> <separated_scenes_path>
    """
def merge_scenes(edgar_scenes_path: str, scene_path: str, dataset_version="v1.0-test") -> None:
    files_to_update = [
                    'calibrated_sensor.json', 
                    'ego_pose.json', 
                    'instance.json', 
                    'log.json', 
                    'map.json', 
                    'sample_annotation.json', 
                    'sample_data.json',
                    'scene.json',
                    'sample.json', 
                    'sensor.json'
                    ]
    folders_to_merge = ["samples", "sweeps"]

    for file_name in files_to_update:
        update_json_file(edgar_scenes_path, scene_path, file_name, dataset_version)
    print("Merging folders...")
    for folder in tqdm.tqdm(folders_to_merge):
        merge_folders(os.path.join(scene_path, folder), 
                      os.path.join(edgar_scenes_path, folder))
    
def main():
    if len(sys.argv) != 3:
        print("Usage: python merge_scenes.py <edgar_scenes_name> <separated_scenes_path> <dataset_version>")
        sys.exit(1)

    edgar_scenes = sys.argv[1]
    scenes_path = sys.argv[2]
    dataset_version = sys.argv[3] if len(sys.argv) > 3 else "v1.0-test"
    edgar_scenes_path = os.path.join(os.path.dirname(scenes_path), edgar_scenes)
    if not os.path.exists(edgar_scenes_path):
        os.makedirs(edgar_scenes_path)
    else:
        print(f"Error: The path {edgar_scenes_path} already exists.")
        sys.exit(1)

    if not os.path.exists(scenes_path):
        print(f"Error: The path {scenes_path} does not exist.")
        sys.exit(1)

    print("Merging scenes...")

    list_scenes = os.listdir(scenes_path)
    list_scenes.sort()
    first_scene_bool = True

    print(list_scenes)
    for scene in tqdm.tqdm(list_scenes):
        scene_path = os.path.join(scenes_path, scene)
        if os.path.isdir(scene_path):
            print(f"Merging scene: {scene}")
            if first_scene_bool:
                shutil.copytree(scene_path, edgar_scenes_path, dirs_exist_ok=True)
                first_scene_bool = False
            else:
                try:
                    merge_scenes(edgar_scenes_path, scene_path, dataset_version)
                    print("############################################")
                    print(f"Scene {scene} merged successfully.")
                except Exception as e:
                    print("#############################################")
                    print(f"Error: The scene {scene} could not be merged.")
                    print(f"Exception: {e}")
if __name__ == "__main__":
    main()