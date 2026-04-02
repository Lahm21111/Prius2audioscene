from typing import List, Optional
from cae_microphone_array.msg import AudioStream
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import PointCloud2  # ✅ 加这个
import numpy as np
import rosbag2_py
import pickle

# =========================
# User config (edit here)
# =========================
BAG_PATH = "/workspaces/Prius2audioscene/rosbag/"
TOPIC_MIC  = "/cae_micarray/audio/array"
TOPIC_LIDAR = "/sensing/lidar/top/points"
STORAGE_ID = "sqlite3"

WIN_BACK = 4800
OUT_PKL = "lidar_mic_windows.pkl"
# =========================


def stamp_to_ns(stamp) -> int:
    """ROS2 builtin_interfaces/Time -> int nanoseconds"""
    return int(stamp.sec) * 10**9 + int(stamp.nanosec)


def read_bag_collect(
    bag_path: str,
    topic_mic: str,
    topic_lidar: str,
    storage_id: str = "sqlite3",
):
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id=storage_id)
    converter_options = rosbag2_py.ConverterOptions("cdr", "cdr")

    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)

    # Try metadata for duration
    start_ns: Optional[int] = None
    end_ns: Optional[int] = None
    try:
        metadata = reader.get_metadata()
        start_ns = int(metadata.starting_time.nanoseconds)
        duration_ns = int(metadata.duration.nanoseconds)
        end_ns = start_ns + duration_ns
    except Exception:
        pass

    mic_ts: List[int] = []
    lidar_ts: List[int] = []          # ✅ 这里将存 header stamp(ns)
    lidar_bag_ts: List[int] = []      # （可选）同时存 bag ts 方便 debug
    mic_blocks = []

    first_ts: Optional[int] = None
    last_ts: Optional[int] = None

    while reader.has_next():
        topic_name, data, timestamp_ns = reader.read_next()
        ts_bag = int(timestamp_ns)

        if first_ts is None:
            first_ts = ts_bag
        last_ts = ts_bag

        if topic_name == topic_mic:
            mic_ts.append(ts_bag)  # mic 仍用 bag ts（你没要求改）
            msg = deserialize_message(data, AudioStream)
            audio_data = np.frombuffer(bytes(msg.data), dtype=np.float64)
            audio_data = audio_data.reshape(-1, 56)
            mic_blocks.append(audio_data)

        elif topic_name == topic_lidar:
            # ✅ 反序列化 LiDAR，取 header.stamp
            pc = deserialize_message(data, PointCloud2)
            ts_hdr = stamp_to_ns(pc.header.stamp)
            lidar_ts.append(ts_hdr)
            lidar_bag_ts.append(ts_bag)

    if not mic_blocks:
        raise RuntimeError(f"No MIC messages found on {topic_mic}")
    if not lidar_ts:
        raise RuntimeError(f"No LiDAR messages found on {topic_lidar}")

    micarray_record = np.vstack(mic_blocks)  # (N,56)

    # Fallback duration from scan (bag time)
    if start_ns is None or end_ns is None:
        start_ns = first_ts
        end_ns = last_ts

    duration_s = 0.0 if (start_ns is None or end_ns is None) else (end_ns - start_ns) / 1e9

    return duration_s, start_ns, end_ns, mic_ts, lidar_ts, micarray_record



def build_lidar_aligned_mic_windows(
    start_ns: int,
    end_ns: int,
    lidar_ts: List[int],
    micarray_record: np.ndarray,
    win_back: int = 4800,
):
    N = micarray_record.shape[0]
    C = micarray_record.shape[1]
    total_ns = max(1, end_ns - start_ns)  # avoid divide by zero

    out = []
    for ts in lidar_ts:
        ratio = (ts - start_ns) / total_ns
        ratio = float(np.clip(ratio, 0.0, 1.0))

        mic_idx = int(round(ratio * (N - 1)))
        mic_idx = int(np.clip(mic_idx, 0, N - 1))

        left = mic_idx - win_back
        right = mic_idx  # inclusive current => python slice end is exclusive
        if left < 0:
            # left pad zeros to keep fixed window length
            pad = -left
            window = micarray_record[0:right, :]
            if pad > 0:
                window = np.vstack([np.zeros((pad, C), dtype=micarray_record.dtype), window])
        else:
            window = micarray_record[left:right, :]
        print(ts, window.shape)
        out.append(
            {
                "timestamp": ts,
                "data": window,  # (4800,56)
            }
        )
    return out


def extract_aligned_audio(bag_name):
    duration_s, start_ns, end_ns, mic_ts, lidar_ts, micarray_record = read_bag_collect(
        bag_path=BAG_PATH+bag_name,
        topic_mic=TOPIC_MIC,
        topic_lidar=TOPIC_LIDAR,
        storage_id=STORAGE_ID,
    )
    print(lidar_ts)
    print("=== Bag summary ===")
    print(f"Bag path: {BAG_PATH}")
    print(f"Start (ns): {start_ns}")
    print(f"End   (ns): {end_ns}")
    print(f"Duration (s): {duration_s:.6f}")
    print(f"MIC msgs: {len(mic_ts)} | LIDAR msgs: {len(lidar_ts)}")
    print(f"micarray_record shape: {micarray_record.shape}, dtype={micarray_record.dtype}")

    aligned = build_lidar_aligned_mic_windows(
        start_ns=start_ns,
        end_ns=end_ns,
        lidar_ts=lidar_ts,
        micarray_record=micarray_record,
        win_back=WIN_BACK,
    )

    with open(OUT_PKL, "wb") as f:
        pickle.dump(aligned, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"\nSaved pickle: {OUT_PKL}")
    print(f"Example entry keys: {list(aligned[0].keys())}")
    print(f"Example mic_window shape: {aligned[0]['data'].shape}")


if __name__ == "__main__":
    bag_name = "rosbag2_2025_08_21-14_29_47"
    extract_aligned_audio(bag_name)