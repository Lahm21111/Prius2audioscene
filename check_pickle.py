#!/usr/bin/env python3

from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

# =========================
# USER INPUT (只改这里)
# =========================
BAG_PATH = "/workspaces/Prius2audioscene/rosbag/rosbag2_2025_08_21-14_22_25"
TOPIC    = "/sensing/lidar/concatenated/pointcloud"


def main():
    reader = SequentialReader()

    storage_options = StorageOptions(
        uri=BAG_PATH,
        storage_id="sqlite3"
    )

    converter_options = ConverterOptions(
        input_serialization_format="cdr",
        output_serialization_format="cdr"
    )

    reader.open(storage_options, converter_options)

    # topic -> type 映射
    topics = reader.get_all_topics_and_types()
    type_map = {t.name: t.type for t in topics}

    if TOPIC not in type_map:
        print(f"[ERROR] Topic '{TOPIC}' not found.")
        print("Available topics:")
        for t in type_map:
            print(" ", t)
        return

    msg_type = get_message(type_map[TOPIC])

    print(f"Bag   : {BAG_PATH}")
    print(f"Topic : {TOPIC}")
    print("=" * 60)

    idx = 0
    while reader.has_next():
        topic, data, t = reader.read_next()

        if topic != TOPIC:
            continue

        # rosbag 记录时间（ns）
        sec  = t // 1_000_000_000
        nsec = t %  1_000_000_000

        # 反序列化（为了拿 header.stamp）
        msg = deserialize_message(data, msg_type)

        if hasattr(msg, "header"):
            stamp = msg.header.stamp
            print(
                f"{idx:04d} | "
                f"bag_time={sec}.{nsec:09d} | "
                f"msg_time={stamp.sec}.{stamp.nanosec:09d}"
            )
        else:
            print(
                f"{idx:04d} | "
                f"bag_time={sec}.{nsec:09d}"
            )

        idx += 1

    print("=" * 60)
    print(f"Total messages: {idx}")


if __name__ == "__main__":
    main()
