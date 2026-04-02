#!/usr/bin/env python3
"""
简单版：双击 / 点运行就能把 ROS2 rosbag 里的麦克风阵列数据导出成一个 pickle 字典文件。

功能：
- 读取 ROS2 rosbag2 (sqlite3)
- 订阅指定 topic（默认：/cae_micarray/audio/array）
- 解析消息中的 data / channels / sample_rate
- 把每一条消息的数据整理成一个字典：
    {
        timestamp(int): numpy.ndarray, 形状为 (本条消息采样点数, 通道数)
        ...
    }
- 保存成 .pickle 文件，包含：
    {
        "audio_dict": {timestamp: ndarray},
        "sample_rate": int,
        "channels": int,
    }
"""

import os
import sys
import pickle
import numpy as np

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


# ===================== 用户配置区 =====================

# 1. 你的 rosbag 目录路径（就是 ros2 bag record -o 后面的名字）
#    例如：ros2 bag record -o /cae-data/bags/mic_bag ...
BAG_PATH = "/workspaces/Prius2audioscene/rosbag/rosbag2_2025_08_21-14_22_25"   # <<< 这里只要改成自己的路径

# 2. 麦克风数组的 topic 名
TOPIC_NAME = "/cae_micarray/audio/array"

# 3. 导出文件名（保存在当前脚本所在目录）
OUTPUT_FILE = "/workspaces/Prius2audioscene/micarray_data.pickle"

# 4. 数据类型（根据你的 AudioStream.data 实际类型来选）
#    常见情况：
#       - "float64"  (np.float64)
#       - "float32"  (np.float32)
#       - "int16"    (np.int16)
DATA_DTYPE = "float64"

# =================== 用户配置结束 =====================


def create_reader(bag_path: str):
    """创建 rosbag2 顺序读取器，并返回 (reader, topic_type_map)。"""
    if not os.path.exists(bag_path):
        raise FileNotFoundError(f"Bag 路径不存在：{bag_path}")

    storage_options = rosbag2_py.StorageOptions(
        uri=bag_path,
        storage_id="sqlite3",
    )
    converter_options = rosbag2_py.ConverterOptions(
        input_serialization_format="cdr",
        output_serialization_format="cdr",
    )

    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()
    type_map = {t.name: t.type for t in topic_types}

    return reader, type_map


def collect_micarray_data(bag_path: str, topic_name: str, dtype=np.float64):
    """
    从 rosbag 里读取指定 topic 的所有消息，整理成一个字典。

    返回：
        audio_dict: dict，形如：
            {
                timestamp(int): np.ndarray, shape = (N_i, channels),
                ...
            }
        sample_rate: int
        channels: int
    """
    reader, type_map = create_reader(bag_path)

    if topic_name not in type_map:
        raise RuntimeError(
            f"在 bag {bag_path!r} 中找不到 topic {topic_name!r}\n"
            f"可用的 topic 有：{list(type_map.keys())}"
        )

    msg_type_str = type_map[topic_name]
    msg_type = get_message(msg_type_str)

    audio_dict = {}   # key: timestamp, value: ndarray

    sample_rate = None
    channels = None
    msg_count = 0

    print("===============================================")
    print(f"[INFO] 正在读取 rosbag: {bag_path}")
    print(f"[INFO] 目标 topic: {topic_name}")
    print(f"[INFO] 消息类型: {msg_type_str}")
    print("===============================================")

    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        if topic != topic_name:
            continue

        msg = deserialize_message(data, msg_type)
        msg_count += 1

        # 第一次读到消息时，记录采样率和通道数
        if sample_rate is None:
            # 假设消息格式里有 sample_rate 和 channels 字段
            sample_rate = int(msg.sample_rate)
            channels = int(msg.channels)
            print(f"[INFO] 第一条消息：sample_rate = {sample_rate}, channels = {channels}")

        # buffer → numpy
        arr = np.frombuffer(msg.data, dtype=dtype)

        if len(arr) % channels != 0:
            raise ValueError(
                f"第 {msg_count} 条消息的数据长度 {len(arr)} "
                f"不能被通道数 {channels} 整除，检查 DATA_DTYPE 是否设置正确。"
            )

        # (本条消息的采样点数, 通道数)
        arr = arr.reshape(-1, channels)

        # 保存到字典： key=timestamp, value=array
        # timestamp 是 rosbag2_py 读出来的整型时间戳（通常是 ns）
        audio_dict[timestamp] = arr

        if msg_count == 1:
            print(f"[INFO] 第 1 条消息矩阵形状: {arr.shape}")

    if msg_count == 0:
        raise RuntimeError(
            f"在 bag {bag_path!r} 中没有找到任何 {topic_name!r} 的消息。"
        )

    print("===============================================")
    print(f"[INFO] 共读取消息条数: {msg_count}")
    print(f"[INFO] 字典中的 key 数量: {len(audio_dict)}")
    print("===============================================")

    return audio_dict, sample_rate, channels


def main():
    # 将字符串 dtype 映射为 numpy dtype
    dtype_map = {
        "float64": np.float64,
        "float32": np.float32,
        "int16": np.int16,
    }
    if DATA_DTYPE not in dtype_map:
        raise ValueError(
            f"DATA_DTYPE 设置错误：{DATA_DTYPE}，"
            f"可选值为 {list(dtype_map.keys())}"
        )
    dtype = dtype_map[DATA_DTYPE]

    try:
        audio_dict, sample_rate, channels = collect_micarray_data(
            bag_path=BAG_PATH,
            topic_name=TOPIC_NAME,
            dtype=dtype,
        )
    except Exception as e:
        print("===============================================")
        print("[ERROR] 导出过程中出错：")
        print(e)
        print("===============================================")
        print("请检查：")
        print("1) BAG_PATH 路径是否正确")
        print("2) TOPIC_NAME 是否写对")
        print("3) DATA_DTYPE 是否和实际消息里的 data 类型一致")
        input("按回车键退出...")
        sys.exit(1)

    # ====== 使用 pickle 保存成一个字典 ======
    data_to_save = {
        "audio_dict": audio_dict,   # {timestamp: ndarray}
        "sample_rate": sample_rate,
        "channels": channels,
    }

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(data_to_save, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"[INFO] 数据已保存到: {OUTPUT_FILE}")
    print("    内容包括：")
    print("    - audio_dict: {timestamp → ndarray(shape = (N_i, channels))}")
    print("    - sample_rate: int")
    print("    - channels: int")
    print("===============================================")
    input("导出完成，按回车键退出...")


if __name__ == "__main__":
    main()
