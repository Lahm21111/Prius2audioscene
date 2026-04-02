import os

from cv_bridge import CvBridge
from numpy.typing import NDArray
from sensor_msgs.msg import Image, CompressedImage

from tables.calibrated_sensor import CalibratedSensor
from tables.sensor import Sensor
from utils.utils import get_unix_time


class Image:
    def __init__(
        self,
        msg: Image,
        bridge: CvBridge,
        sensors: Sensor,
        calibrated_sensors: CalibratedSensor,
    ) -> None:
        sensor = sensors.get_sensor_by_frame_id(msg.header.frame_id)

        filename = self._get_filename(msg, sensor["channel"])

        self.data = {
            "fileformat": "jpg",
            "filename": filename,
            "filedata": self._get_image(bridge, msg),
            "height": msg.height,
            "width": msg.width,
            "timestamp": get_unix_time(msg.header.stamp),
            "calibrated_sensor_token": calibrated_sensors.get_calibrated_sensor_token(
                sensor["token"]
            ),
            # "modality": "camera"
        }

    def _get_filename(self, msg: Image, sensor_channel: str) -> str:
        if not sensor_channel:
            raise Exception(f"Sensor with frame {msg.header.frame_id} not found")

        # timestamp = str(int(get_unix_time(msg.header.stamp) * 1e9))
        timestamp = str(int(get_unix_time(msg.header.stamp) * 1e6))  # microseconds

        filename = os.path.join(
            "samples",
            sensor_channel,
            "rosbag__" + sensor_channel + "__" + timestamp + ".jpeg",
        )

        return filename

    def _get_image(self, bridge: CvBridge, msg: Image) -> NDArray:
        return bridge.imgmsg_to_cv2(msg, "bgr8")

class ImageCompressed(Image):
    def __init__(
        self,
        msg: CompressedImage,
        bridge: CvBridge,
        sensors: Sensor,
        calibrated_sensors: CalibratedSensor,
    ) -> None:
        sensor = sensors.get_sensor_by_frame_id(msg.header.frame_id)

        filename = self._get_filename(msg, sensor["channel"])

        self.data = {
            "fileformat": "jpg",
            "filename": filename,
            "filedata": self._get_image(bridge, msg),
            "height": 1200,
            "width": 1920,
            "timestamp": get_unix_time(msg.header.stamp),
            "calibrated_sensor_token": calibrated_sensors.get_calibrated_sensor_token(
                sensor["token"]
            ),
            # "modality": "camera"
        }
        self.data["height"] = self.data["filedata"].shape[0]
        self.data["width"] = self.data["filedata"].shape[1]
    def _get_image(self, bridge, msg):
        cv2_image =bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        return cv2_image
    