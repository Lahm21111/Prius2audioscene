from sensor_msgs.msg import CameraInfo


class Info:

    def __init__(self, msg: CameraInfo) -> None:
        self.frame_id = msg.header.frame_id
        self.camera_intrinsic = msg.k.reshape((3, 3)).tolist()
