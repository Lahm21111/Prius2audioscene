import pickle

# ======== 修改这里：你的 pickle 文件名 ========
PICKLE_FILE = "/workspaces/Prius2audioscene/micarray_data.pickle"
# ===========================================

# 读取 pickle
with open(PICKLE_FILE, "rb") as f:
    data = pickle.load(f)

audio_dict = data["audio_dict"]   # {timestamp: ndarray}
timestamps = sorted(audio_dict.keys())

print("Loaded", len(timestamps), "timestamps")

# ======== 输入一个 timestamp（你希望访问的那个） ========
target_ts = int(1755778954971836000)
# =====================================================

# 查找是否存在
if target_ts in audio_dict:
    audio = audio_dict[target_ts]
    print("找到 timestamp!")
    print("该条 audio 矩阵形状:", audio.shape)
    print("前 10 个数据:\n", audio[:10])
else:
    print("没有找到该 timestamp! 可用的最近 timestamp 如下：")
    # 找最接近的时间戳
    import bisect
    idx = bisect.bisect_left(timestamps, target_ts)

    if idx == 0:
        nearest = timestamps[0]
    elif idx == len(timestamps):
        nearest = timestamps[-1]
    else:
        before = timestamps[idx - 1]
        after = timestamps[idx]
        nearest = before if abs(before - target_ts) < abs(after - target_ts) else after

    print("最近的 timestamp:", nearest)
    audio = audio_dict[nearest]
    print("该条 audio 矩阵形状:", audio.shape)
    print("前 10 个数据:\n", audio[:10])
