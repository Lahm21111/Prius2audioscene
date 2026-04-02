import numpy as np

# 你的文件路径
file_path = "/workspaces/Prius2audioscene/output/sweeps/MICARRAY/rosbag__MICARRAY__1755777405400236.pcd.bin"

# 读取为 float32 数组
points = np.fromfile(file_path, dtype=np.float32)

print(points.reshape(4410,-1).shape)