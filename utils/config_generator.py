from flask import config
import rosbag2_py
from messages.reader import Reader

import yaml
import glob
import os

CAMERA_DICT = {
    "CAM_camera0":"CAM_FRONTCENTER",
    "CAM_camera1":"CAM_FRONTRIGHT",
    "CAM_camera2":"CAM_RIGHT",
    "CAM_camera3":"CAM_REARRIGHT",
    "CAM_camera4":"CAM_REARCENTER",
    "CAM_camera5":"CAM_REARLEFT",
    "CAM_camera6":"CAM_LEFT",
    "CAM_camera7":"CAM_FRONTLEFT",
}
def get_frame_id(bag_path, topic_name):
    n_reader = Reader()
    first_topic, first_msg, first_timestamp = next(
        n_reader.read_messages(bag_path[0], topic_name)
    )
    frame_id = first_msg.header.frame_id
    return frame_id

def get_topic_message_count(bag_path, topic_name):
    # Create an Info object to retrieve metadata
    info = rosbag2_py.Info()
    
    # Read metadata from the bag file
    metadata = info.read_metadata(bag_path, 'mcap')
    
    # Search for the specified topic
    for topic in metadata.topics_with_message_count:
        if topic.topic_metadata.name == topic_name:
            print(f"Message count for topic '{topic_name}': {topic.message_count}")
            return topic.message_count  # Return the message count
    
    print(f"Topic '{topic_name}' not found in the bag file.")
    return None  # Return None if the topic is not found

def get_topic_message_count_dictionary(bag_path):
    # Create an Info object to retrieve metadata
    info = rosbag2_py.Info()
    
    # Read metadata from the bag file
    metadata = info.read_metadata(bag_path, 'sqlite3')
    
    # Create a dictionary to store message counts for each topic
    message_counts = {}
    
    # Iterate through the topics and their message counts
    for topic in metadata.topics_with_message_count:
        message_counts[topic.topic_metadata.name] = topic.message_count
    
    return message_counts  # Return the dictionary of message counts


def conf_generator():

    config_path = os.environ.get("CONFIG_PATH", "config/config.yaml")
    print(f"Reading config from {config_path}")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    SCENE_NAME = os.environ.get('SCENE_NAME', "ros2_output")
    CAM_FRONTCENTER_TYPE = os.environ.get('CAM_FRONTCENTER_TYPE', "image_raw")
    CAM_SECONDARY_TYPE = os.environ.get('CAM_SECONDARY_TYPE', "image_raw")


    config["BAG_INFO"]["NAME"] = SCENE_NAME
    print(f"Scene name: {SCENE_NAME}")
    bag_folder_path = config["BAG_INFO"]["BAGS"]

    # Find all .db3 files in the rosbag folder
    bag_path = glob.glob(os.path.join(bag_folder_path,SCENE_NAME, "*.db3"))
    print(f"List of processing bags: {bag_path}")

    # read all topics from the rosbag
    storage_options = rosbag2_py.StorageOptions(uri=bag_path[0], storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions("", "")
    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)
    all_topics = reader.get_all_topics_and_types()
    print(f"All topics in the bag: {[topic.name for topic in all_topics]}")


    available_odometry_topics = []
    config["SENSOR_INFO"] = {}
    config["LIDARS"] = {}
    message_count_dict = get_topic_message_count_dictionary(bag_path[0])
    for topic in all_topics:

        # Find the camera topics
        if (topic.name.find(CAM_FRONTCENTER_TYPE) != -1) and (topic.name.find("camera0") != -1):
            frame_id = get_frame_id(bag_path, topic.name)
            if topic.name.find("sensing") == -1:
                sensor_name = f"CAM_{topic.name.split('/')[5]}"
                sensor_name = CAMERA_DICT[sensor_name]
            else:
                sensor_name = f"CAM_{topic.name.split('/')[3]}"
                sensor_name = CAMERA_DICT[sensor_name]
            
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["CALIB"] = f"{topic.name.rsplit('/', 1)[0]}/camera_info"
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["SENSOR_INFO"][sensor_name][
                    "TOPIC"
                ] = topic.name
            continue
        elif (topic.name.find(CAM_SECONDARY_TYPE) != -1 and (topic.name.find("frontcenter") == -1)):
            frame_id = get_frame_id(bag_path, topic.name)
            if topic.name.find("sensing") == -1:
                sensor_name = f"CAM_{topic.name.split('/')[5]}"
                sensor_name = CAMERA_DICT[sensor_name]
            else:
                sensor_name = f"CAM_{topic.name.split('/')[3]}"
                sensor_name = CAMERA_DICT[sensor_name]
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["CALIB"] = f"{topic.name.rsplit('/', 1)[0]}/camera_info"
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["SENSOR_INFO"][sensor_name][
                    "TOPIC"
                ] = topic.name
            continue

        # Evaluate LIDAR_TOP. In case Lidars are not concatenated innovusion_frontcenter is the LIDAR_TOP
        if (
            topic.name.find("concatenated") != -1
            or topic.name.find("top/pointcloud") != -1
        ):
            print(topic.name)
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            frame_id = get_frame_id(bag_path, topic.name)
            sensor_name = "LIDAR_TOP"
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["TOPIC"] = topic.name
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["LIDARS"][sensor_name] = frame_id
            continue

        # Add all Lidars to the config in case they are not concatenated
        # if topic.name.find("pointcloud") != -1:
        #     if message_count_dict[topic.name] == 0:
        #         print(f"Topic {topic.name} has no messages and cannot be processed.")
        #         continue
        #     frame_id = get_frame_id(bag_path, topic.name)
        #     sensor_name = f"LIDAR_{topic.name.split('/')[3]}"
        #     config["SENSOR_INFO"][sensor_name] = {}
        #     config["SENSOR_INFO"][sensor_name]["TOPIC"] = topic.name
        #     config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
        #     config["LIDARS"][sensor_name] = frame_id

        if topic.type.find("Odometry") != -1:
            print(topic.name)
            #config["BAG_INFO"]["ODOM_TOPIC"] = topic.name
            available_odometry_topics.append(topic.name)
    
    # Check if Kinematic state is empty
    # If it is not empty, set it as the odometry topic
    # If it is empty, set the first available odometry topic
    if '/localization/kinematic_state' in available_odometry_topics:
        number_messages_kinematic_state = message_count_dict["/localization/kinematic_state"]
    else:
        number_messages_kinematic_state = 0
    if "/localization/kinematic_state" in available_odometry_topics and number_messages_kinematic_state > 0:
        config["BAG_INFO"]["ODOM_TOPIC"] = "/localization/kinematic_state"
    else:
        if "/localization/kinematic_state" in available_odometry_topics:
            available_odometry_topics.remove("/localization/kinematic_state")
        if message_count_dict[available_odometry_topics[0]] == 0:
            raise ValueError(
                f"Topic {available_odometry_topics[0]} has no messages and cannot be processed."
            )
        config["BAG_INFO"]["ODOM_TOPIC"] = available_odometry_topics[0]
        print(
            f"Using the first available odometry topic: {available_odometry_topics[0]}"
        )
    
    # Save the modified dictionary back to a YAML file
    print(f" Config: {config}")
    print(f"Writing config to {config_path}")
    with open(config_path, "w") as file:
        yaml.dump(config, file)

def conf_generator_without_kinematics(scene_name):

    # read the config file
    config_path = os.environ.get("CONFIG_PATH", "config/config.yaml")
    print(f"Reading config from {config_path}")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # rewrite the scene name 
    SCENE_NAME = scene_name
    # SCENE_NAME = os.environ.get('SCENE_NAME', "ros2_output")

    # get the type of the message from the camera 
    CAM_FRONTCENTER_TYPE = os.environ.get('CAM_FRONTCENTER_TYPE', "image_raw")
    CAM_SECONDARY_TYPE = os.environ.get('CAM_SECONDARY_TYPE', "image_raw")

    # rewrite the scene name in the config file
    config["BAG_INFO"]["NAME"] = SCENE_NAME
    print(f"Scene name: {SCENE_NAME}")
    bag_folder_path = config["BAG_INFO"]["BAGS"]

    # Find all .db3 files in the rosbag folder
    bag_path = glob.glob(os.path.join(bag_folder_path,SCENE_NAME, "*.db3"))
    print(bag_path)
    print(f"List of processing bags: {bag_path}")

    # read all topics from the rosbag
    storage_options = rosbag2_py.StorageOptions(uri=bag_path[0], storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions("", "")
    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)
    all_topics = reader.get_all_topics_and_types()
    print(f"All topics in the bag: {[topic.name for topic in all_topics]}")

    available_odometry_topics = []
    config["SENSOR_INFO"] = {}
    config["LIDARS"] = {}
    # Uncomment to add microphone modality
    config["MICARRAY"] = {}

    # count the number of the messages per topic 
    message_count_dict = get_topic_message_count_dictionary(bag_path[0])
    for topic in all_topics:


        # Find the camera topics
        if (topic.name.find(CAM_FRONTCENTER_TYPE) != -1) and (topic.name.find("camera0") != -1):
            frame_id = get_frame_id(bag_path, topic.name)

            # give a name to the topic 
            if topic.name.find("sensing") == -1:
                sensor_name = f"CAM_{topic.name.split('/')[5]}"
                sensor_name = CAMERA_DICT[sensor_name]
            else:
                sensor_name = f"CAM_{topic.name.split('/')[3]}"
                sensor_name = CAMERA_DICT[sensor_name]
            
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")

            # initialize the message in the config file 
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["CALIB"] = f"{topic.name.rsplit('/', 1)[0]}/camera_info"
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["SENSOR_INFO"][sensor_name][
                    "TOPIC"
                ] = topic.name
            continue
        elif (topic.name.find(CAM_SECONDARY_TYPE) != -1 and (topic.name.find("frontcenter") == -1)):
            frame_id = get_frame_id(bag_path, topic.name)
            if topic.name.find("sensing") == -1:
                sensor_name = f"CAM_{topic.name.split('/')[5]}"
                sensor_name = CAMERA_DICT[sensor_name]
            else:
                sensor_name = f"CAM_{topic.name.split('/')[3]}"
                sensor_name = CAMERA_DICT[sensor_name]
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["CALIB"] = f"{topic.name.rsplit('/', 1)[0]}/camera_info"
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["SENSOR_INFO"][sensor_name][
                    "TOPIC"
                ] = topic.name
            continue

        # Evaluate LIDAR_TOP. In case Lidars are not concatenated innovusion_frontcenter is the LIDAR_TOP
        if (
            topic.name.find("concatenated") != -1
            or topic.name.find("top/pointcloud") != -1
        ):
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            frame_id = get_frame_id(bag_path, topic.name)
            print("lidar",frame_id)
            sensor_name = "LIDAR_TOP"
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["TOPIC"] = topic.name
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["LIDARS"][sensor_name] = frame_id
            continue

        # Uncomment to add the microphone array top into the config file
        if topic.name.find("/cae_micarray/audio/array") != -1:
            if message_count_dict[topic.name] == 0:
                raise ValueError(f"Topic {topic.name} has no messages and cannot be processed.")
            
            # set the frame directly as base_link
            frame_id = "cae_micarray"
            sensor_name = "MICARRAY"
            config["SENSOR_INFO"][sensor_name] = {}
            config["SENSOR_INFO"][sensor_name]["TOPIC"] = topic.name
            config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
            config["SENSOR_INFO"][sensor_name]["FREQUENCY"] = 48000
            config["SENSOR_INFO"][sensor_name]["MIC_NUM"] = 56
            config["MICARRAY"][sensor_name] = frame_id
            continue

        # Add all Lidars to the config in case they are not concatenated
        # if topic.name.find("pointcloud") != -1:
        #     if message_count_dict[topic.name] == 0:
        #         print(f"Topic {topic.name} has no messages and cannot be processed.")
        #         continue
        #     frame_id = get_frame_id(bag_path, topic.name)
        #     sensor_name = f"LIDAR_{topic.name.split('/')[3]}"
        #     config["SENSOR_INFO"][sensor_name] = {}
        #     config["SENSOR_INFO"][sensor_name]["TOPIC"] = topic.name
        #     config["SENSOR_INFO"][sensor_name]["FRAME"] = frame_id
        #     config["LIDARS"][sensor_name] = frame_id

        if topic.type.find("Odometry") != -1:
            #config["BAG_INFO"]["ODOM_TOPIC"] = topic.name
            available_odometry_topics.append(topic.name)
    
    # Check if Kinematic state is empty
    # If it is not empty, set it as the odometry topic
    # If it is empty, set the first available odometry topic
    # if '/localization/kinematic_state' in available_odometry_topics:
    #     number_messages_kinematic_state = message_count_dict["/localization/kinematic_state"]
    # else:
    #     number_messages_kinematic_state = 0
    # if "/localization/kinematic_state" in available_odometry_topics and number_messages_kinematic_state > 0:
    #     config["BAG_INFO"]["ODOM_TOPIC"] = "/localization/kinematic_state"
    # else:
    #     if "/localization/kinematic_state" in available_odometry_topics:
    #         available_odometry_topics.remove("/localization/kinematic_state")
    #     if message_count_dict[available_odometry_topics[0]] == 0:
    #         raise ValueError(
    #             f"Topic {available_odometry_topics[0]} has no messages and cannot be processed."
    #         )
    #     config["BAG_INFO"]["ODOM_TOPIC"] = available_odometry_topics[0]
    #     print(
    #         f"Using the first available odometry topic: {available_odometry_topics[0]}"
    #     )
    # Save the modified dictionary back to a YAML file

    # config["BAG_INFO"]["ODOM_TOPIC"] = "None"
    print(f"Writing config to {config_path}")
    with open(config_path, "w") as file:
        yaml.dump(config, file)

def conf_reseter():
    config_path = os.environ.get("CONFIG_PATH", "config/config.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    config["BAG_INFO"]["NAME"]="NONE"
    with open(config_path, "w") as file:
        yaml.dump(config, file)