import os
import json
import argparse
import random
random.seed(41)
# Mapping of old channel names to new channel names
channel_mapping = {
    "CAM_frontcenter": "CAM_FRONT",
    "CAM_frontleft": "CAM_FRONT_LEFT",
    "CAM_frontright": "CAM_FRONT_RIGHT",
    "CAM_rearcenter": "CAM_BACK",
    "CAM_rearleft": "CAM_BACK_LEFT",
    "CAM_rearright": "CAM_BACK_RIGHT",
    "LIDAR_TOP": "LIDAR_TOP"  # No change for this
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update nuscenes formatted dataset to be compatible with nuscenes-devkit")
    parser.add_argument("dataset_root", type=str, help="Root directory of the NuScenes formatted dataset.")
    parser.add_argument("--version", type=str, default="v1.0-test", help="Dataset version (default: v1.0-test).")
    parser.add_argument("--update-intrinsics", action="store_true", help="Update camera intrinsics if enabled.")
    parser.add_argument("--train_proportion", type=float, help="Proportion of training scenes", default=0.7)
    parser.add_argument("--val_proportion", type=float, help="Proportion of val scenes", default=0.2)
    return parser.parse_args()

def update_sensor_json(dataset_root, version):
    sensor_file_path = os.path.join(dataset_root, version, "sensor.json")
    if not os.path.exists(sensor_file_path):
        raise FileNotFoundError(f"sensor.json not found in {sensor_file_path}.")
    
    with open(sensor_file_path, "r") as file:
        data = json.load(file)
    
    # Update the channel names
    for entry in data:
        if entry["channel"] in channel_mapping:
            entry["channel"] = channel_mapping[entry["channel"]]
    
    # Write back the updated sensor.json file
    with open(sensor_file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Updated sensor.json in {version}")

def get_sensor_tokens(dataset_root, version, sensor_names: list):
    sensor_file_path = os.path.join(dataset_root, version, "sensor.json")
    sensor_tokens = []
    with open(sensor_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        if item.get("channel") in sensor_names:
            sensor_tokens.append(item.get("token"))
    return sensor_tokens 

def update_camera_intrinsics(dataset_root, version):
    default_calibrated_sensor_file_path = os.path.join(dataset_root, version, "calibrated_sensor_default.json")
    calibrated_sensor_file_path = os.path.join(dataset_root, version, "calibrated_sensor.json")
    
    if not os.path.exists(default_calibrated_sensor_file_path):
        print(f"Error: {default_calibrated_sensor_file_path} not found. Please copy it to the same directory as calibrated_sensor_default.json.")
        return
    
    skip_tokens = get_sensor_tokens(dataset_root, version, ["CAM_FRONT","LIDAR_TOP"])
    
    
    with open(calibrated_sensor_file_path, "r") as file:
        data = json.load(file)
    
    with open(default_calibrated_sensor_file_path, "r") as file:
        data_default = json.load(file)
    
    for record, default_record in zip(data, data_default):
        if record["sensor_token"] not in skip_tokens and record["camera_intrinsic"] == default_record["camera_intrinsic"]:
            record["camera_intrinsic"][0][0] /= 5.0  # f_x
            record["camera_intrinsic"][1][1] /= 5.0  # f_y
            record["camera_intrinsic"][0][2] /= 5.0  # c_x
            record["camera_intrinsic"][1][2] /= 5.0  # c_y
    
    with open(calibrated_sensor_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Updated calibrated_sensor.json in {version}")

def create_splits_json(dataset_root, version, train_proportion=0.7, val_proportion=0.2):
    scene_file_path = os.path.join(dataset_root, version, "scene.json")
    splits_file_path = os.path.join(dataset_root, version, "splits.json")
    
    if not os.path.exists(scene_file_path):
        raise FileNotFoundError(f"scene.json not found in {scene_file_path}.")
    
    with open(scene_file_path, "r") as file:
        scene_data = json.load(file)
    
    # Extract scene names
    scene_names = [scene["name"] for scene in scene_data]
    
    random.shuffle(scene_names)
    train_len = int(len(scene_names)*train_proportion)
    val_len = int(len(scene_names)*val_proportion)
    test_len = len(scene_names)-train_len-val_len
    train_scenes = scene_names[0:train_len]
    val_scenes = scene_names[train_len:train_len+val_len]
    test_scenes = scene_names[train_len+val_len:]
    print(scene_names)
    # Create splits.json
    splits_data = {"train": train_scenes,
                   "val": val_scenes,
                   "test": test_scenes}
    with open(splits_file_path, "w") as file:
        json.dump(splits_data, file, indent=4)
    print(f"Created splits.json in {version}")

def main():
    args = parse_arguments()
    dataset_root = args.dataset_root
    version = args.version
    update_intrinsics = args.update_intrinsics
    train_proportion = args.train_proportion
    val_proportion = args.val_proportion

    if os.path.exists(dataset_root):
        try:
            #update_sensor_json(dataset_root, version)
            create_splits_json(dataset_root, version, train_proportion, val_proportion)
            #if update_intrinsics:
            #    update_camera_intrinsics(dataset_root, version)
        except FileNotFoundError as e:
            print(e)
    else:
        print(f"Invalid dataset root path: {dataset_root}")

if __name__ == "__main__":
    main()
