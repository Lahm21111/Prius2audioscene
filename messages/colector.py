from typing import Any, Dict
import numpy as np


from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import CameraInfo, Image, CompressedImage, PointCloud2
from cae_microphone_array.msg import AudioStream
from tf2_msgs.msg import TFMessage
from tqdm import tqdm

from tables.attribute import Attribute
from tables.calibrated_sensor import CalibratedSensor
from tables.category import Category
from tables.ego_pose import EgoPose
from tables.instance import Instance
from tables.lidarseg import LidarSeg
from tables.log import Log
from tables.map import Map
from tables.sample import Sample
from tables.sample_annotation import SampleAnnotation
from tables.sample_data import SampleData
from tables.scene import Scene
from tables.sensor import Sensor
from tables.table import Table
from tables.visibility import Visibilty
from utils.config import Config
from utils.decorators import log_time
from utils.utils import read_json
import os
from collections import deque

from .image import Image as Img
from .image import ImageCompressed
from .info import Info
from .lidar import LiDAR as Lidar
from .audio import AudioArray
from .transforms import TFBuffer


class Colector:
    def __init__(self, conf: Config) -> None:

        # initializ the tools for image transfer
        self.conf = conf
        self.brigde = CvBridge()
        self.tfbuffer = TFBuffer()


        self.sensor = Sensor(conf.sensors)
        self.calibrated_sensor = CalibratedSensor(self.sensor)
        
        # record all the other important tables
        
        self.scene = Scene(self.conf.bag)
        self.sample = Sample()
        self.sample_data = SampleData()
        self.sample_anotation = SampleAnnotation()

        self.category = Category()
        self.instance = Instance()
        self.attributes = Attribute()

        self.ego_pose = EgoPose()
        self.log = Log()
        self.map = Map()
        self.visibility = Visibilty()

        # initialize the audio buffer
        self.audio_sr = int(self.conf.sensors["MICARRAY"].get("FREQUENCY", 48000))
        self.audio_ch = int(self.conf.sensors["MICARRAY"].get("MIC_NUM", 56))
        self._win_samples = int(0.100 * self.audio_sr)  # 4800
        self._audio_buf = np.zeros((0, self.audio_ch), dtype=np.float32) 

        # # NUSCENE OUTPUT
        # self.audio_out_dir = os.path.join(self.conf.bag["OUTPUT"], "samples", "AUDIO_ARRAY")
        # os.makedirs(self.audio_out_dir, exist_ok=True)



        if self.conf.bag.get("LIDARSEG", False):
            self.lidarseg = LidarSeg()

    def colect(self, msg: Any,timestamp) -> None:
        # create the sample data based on the message type
        if isinstance(msg, Image):
            img = Img(msg, self.brigde, self.sensor, self.calibrated_sensor)
            self.sample_data.create_record(img.data)
        elif isinstance(msg, CompressedImage):
            img = ImageCompressed(msg, self.brigde, self.sensor, self.calibrated_sensor)
            # add to the sample data 
            self.sample_data.create_record(img.data)
        elif isinstance(msg, CameraInfo):
            info = Info(msg)
            self.calibrated_sensor.create_cam_info(info)
        elif isinstance(msg, PointCloud2):
            lidar = Lidar(msg, self.sensor, self.calibrated_sensor)
            self.sample_data.create_record(lidar.data)
        elif isinstance(msg, TFMessage):
            self.tfbuffer.process_tf_message(msg)
        # elif isinstance(msg, PoseStamped):
        #     self.ego_pose.create_record(msg)
        # elif isinstance(msg, Odometry):
        #     self.ego_pose.create_record(msg)
        elif isinstance(msg, AudioStream):
            return
        else:
            raise Exception(f"Message type {type(msg)} is not supported")
        
    def colect_audio(self, data: np.ndarray,timestamp) -> None:
        # add the information to the tail of the buffer
        audio_array = AudioArray(data, self.sensor, self.calibrated_sensor,timestamp)
        self.sample_data.create_record(audio_array.data)

    @log_time
    def generate_samples(self) -> None:
        # creates samples based on resampling of sample_data
        master_cal_sensor_token = self.calibrated_sensor.get_calibrated_sensor_token(
            self.sensor.frame_map["base_link"]["token"]
        )

        #align the timestamp 
        self.sample_data.group_into_samples_without_odm(
            master_sensor_token=master_cal_sensor_token,
            sample_window_ms=self.conf.bag["SAMPLE_WINDOW"],
            scene=self.scene,
            sensors=self.sensor,
            sample=self.sample,
            egopose=self.ego_pose,
            tfbuffer=self.tfbuffer,
            conf=self.conf,
        )

        # fill in missing values for scene (scene information)
        self.scene.complete(
            first_sample_token=self.sample.records[0]["token"],
            last_sample_token=self.sample.records[-1]["token"],
            nbr_samples=len(self.sample.records),
            log_token=self.log.create_record(self.map),
        )

    @log_time
    def calibrate_sensors(self) -> None:
        for frame_id in self.sensor.frame_map.keys():
            self.calibrated_sensor.create_record(frame_id, self.tfbuffer)

    def write_tables(self) -> None:
        # Iterate over attributes of the class
        # write all the tables to files
        variables = vars(self).items()
        for _, attr_value in tqdm(
            variables,
            desc="Writing Tables",
            total=len(variables),
        ):

            # Check if the attribute is an instance of Table or its subclasses
            if isinstance(attr_value, Table):
                attr_value.write_table()

    @log_time
    def copy_nuscenes_files(self):
        for name, file in self.conf.nuscenes_files.items():
            try:
                attribute = getattr(self, name)
            except:
                if name == "lidarseg":
                    raise Exception(
                        "Liderseg is not true in config BAG_INFO, but file is specified"
                    )
                else:
                    pass

            attribute.records = read_json(file)
