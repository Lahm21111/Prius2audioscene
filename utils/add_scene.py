import os
import json
import shutil
import sys
import tqdm

"""
This script merges new scene data into an existing EDGAR dataset.
Functions:
    merge_folders(src_folder: str, dst_folder: str) -> None:
        Recursively merges the contents of the source folder into the destination folder.
    update_json_file(edgar_scenes_path: str, new_scene_path: str, file_name: str) -> None:
        Updates a JSON file by appending data from a new scene to the existing EDGAR dataset.
    main():
        Main function that processes command-line arguments, updates JSON files, and merges folders.
Usage:
    python add_scene.py <edgar_scenes_path> <new_scene_path>
Arguments:
    edgar_scenes_path: str - Path to the existing EDGAR dataset.
    new_scene_path: str - Path to the new scene data to be merged.
"""

def merge_folders(src_folder: str, dst_folder: str) -> None:
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)
        
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path)
            else:
                merge_folders(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

def update_json_file(edgar_scenes_path: str, new_scene_path: str, file_name: str, dataset_version="v1.0-trainval") -> None:
    with open(os.path.join(edgar_scenes_path, dataset_version, file_name), 'r') as f:
        calibrated_sensors = json.load(f)

    with open(os.path.join(new_scene_path, dataset_version, file_name), 'r') as f:
        new_data = json.load(f)

    calibrated_sensors.extend(new_data)

    # Save the merged data back to the file
    with open(os.path.join(edgar_scenes_path, dataset_version, file_name), 'w') as f:
        json.dump(calibrated_sensors, f, indent=4)

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_scene.py <edgar_scenes_path> <new_scene_path>")
        sys.exit(1)

    edgar_scenes_path = sys.argv[1]
    new_scene_path = sys.argv[2]

    if not os.path.exists(edgar_scenes_path):
        print(f"Error: The path {edgar_scenes_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(new_scene_path):
        print(f"Error: The path {new_scene_path} does not exist.")
        sys.exit(1)
    
    # #backup_path = os.path.join(edgar_scenes_path, 'backup')
    # backup_path = os.path.join(os.path.dirname(edgar_scenes_path), 'backup')
    # if not os.path.exists(backup_path):
    #     os.makedirs(backup_path)

    # print(f"Creating backup at {backup_path}...")
    # shutil.copytree(edgar_scenes_path, backup_path, dirs_exist_ok=True)
    print("Updating JSON files...")
  
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
    print(files_to_update)
    for file_name in files_to_update:
        update_json_file(edgar_scenes_path, new_scene_path, file_name)
    print("Merging folders...")
   
    folders_to_merge = ["samples", "sweeps"]
    print(folders_to_merge)
    for folder in tqdm.tqdm(folders_to_merge):
        merge_folders(os.path.join(new_scene_path, folder), 
                      os.path.join(edgar_scenes_path, folder))


if __name__ == '__main__':
    main()