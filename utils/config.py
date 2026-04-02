import os
from typing import List

import yaml


class Config:
    def __init__(self, path: os.PathLike) -> None:
        with open(path, "r") as file:
            config = yaml.safe_load(file)
            self.bag = config["BAG_INFO"]
            self.sensors = config["SENSOR_INFO"]
            self.nuscenes_files = config["NUSCENES_FILES"]
            self.lidars = config["LIDARS"]

        if isinstance(self.bag["BAGS"], str):
            if os.path.isdir(self.bag["BAGS"]):
                # self.bag["BAGS"] = [
                #     os.path.join(self.bag["BAGS"], file)
                #     for file in os.listdir(self.bag["BAGS"])
                # ]
                self.bag["BAGS"] = [
                    os.path.join(self.bag["BAGS"], self.bag["NAME"], file)
                    for file in os.listdir(os.path.join(self.bag["BAGS"], self.bag["NAME"]))
                     if file.endswith(".db3")
                ]
            else:
                raise Exception(f"Bag path is not a directory: {self.bag['BAGS']}") 

    def get_msg_topics(self) -> List:
        topics = set()
        topics.update(self.bag["TF_TOPIC"])
        topics.add(self.bag["ODOM_TOPIC"])
        for sensor, info in self.sensors.items():
            topics.add(info["TOPIC"])
            calib = info.get("CALIB")
            if calib:
                topics.add(calib)

        return topics
