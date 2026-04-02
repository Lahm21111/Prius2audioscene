from ast import List
from typing import Any, Generator

from rclpy.serialization import deserialize_message
import numpy as np
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions
from rosidl_runtime_py.utilities import get_message


class Reader:
    def __init__(self) -> None:
        self.reader = SequentialReader()

    def read_messages(
        self, input_bag: str, topics: List
    ) -> Generator[tuple[Any, Any, Any], Any, None]:
        self.reader.open(
            StorageOptions(uri=input_bag, storage_id="sqlite3"),
            ConverterOptions(
                input_serialization_format="cdr", output_serialization_format="cdr"
            ),
        )

        # get the type and the name of the topic from the bag 
        topic_types = self.reader.get_all_topics_and_types()
        topic_type_map = {t.name: t.type for t in self.reader.get_all_topics_and_types()}

        # a function to get the type of the topic
        def typename(topic_name):  # -> Any:
            for topic_type in topic_types:
                if topic_type.name == topic_name:
                    return topic_type.type
            raise ValueError(f"topic {topic_name} not in bag")

        
        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()
            # if a audio message has been read, convert the data into numpy array
            # if "/cae_micarray/audio/array" in topics and topic == "/cae_micarray/audio/array":
            #     mic_array_data = np.frombuffer(data.data, dtype=np.float64)
            #     yield topic, mic_array_data, timestamp
            # else:
            msg_type_str = topic_type_map.get(topic)
            if topic in topics:
                try:
                    msg_type = get_message(typename(topic))
                    msg = deserialize_message(data, msg_type)
                    yield topic, msg, timestamp
                except Exception as e:
                    continue
                                
