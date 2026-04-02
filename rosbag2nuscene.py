from tqdm import tqdm
import pickle
import os
import glob
from messages.colector import Colector
from messages.reader import Reader
from utils.config import Config
from utils.config_generator import conf_generator_without_kinematics, conf_reseter
from utils.convert_pcd import bin2pcd
from utils.extract_aligned_audio_from_rosbag import extract_aligned_audio

def rosbag2nuscene() -> None:
    bag_name = "rosbag2_2025_08_21-14_13_15"
    # extract the audio data from the rosbag and save into a pickle file 
    extract_aligned_audio(bag_name)

    # read the config file and initialize the bag name in the config
    conf_reseter()

    # check the sensor message in the rosbag and rewrite into the config file 
    conf_generator_without_kinematics(bag_name)

    # save the information in the config file into a class and change the bag path 
    conf = Config("config/config.yaml")

    # initialize a sequence reader
    reader = Reader()

    # put all the related message into a set
    topics = conf.get_msg_topics()
    colector = Colector(conf=conf)

    # read the pickle file to load the audio data 
    pickle_path = "/workspaces/Prius2audioscene/lidar_mic_windows.pkl"
    if os.path.exists(pickle_path):
        print("📥 Loading aligned audio windows from pickle:", pickle_path)
        with open(pickle_path, "rb") as f:
            audio_data = pickle.load(f)
    
    # dump all the audio data into the colector buffer
    for i in range(len(audio_data)):
        audio = audio_data[i]
        timestamp = audio["timestamp"]
        data = audio["data"]
        colector.colect_audio(data, timestamp)
        
    # read the all the rosbag in the selected folder 
    for bag in conf.bag["BAGS"]:
        print("📦 Reading bag:", bag)
        # read all the message in sequence 
        for topic, msg, timestamp in tqdm(
            
            reader.read_messages(input_bag=bag, topics=topics),
            desc="Processing Messages",
            
        ):  
            colector.colect(msg,timestamp)


    del reader

    colector.generate_samples()
    colector.calibrate_sensors()
    colector.copy_nuscenes_files()
    colector.write_tables()
    open("output/wiesn_map.png", mode='a').close()
    
    


if __name__ == "__main__":
    rosbag2nuscene()
    # bin2pcd()