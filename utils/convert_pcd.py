import numpy as np
import struct
import open3d as o3d
import os
import tqdm

def bin2pcd():
    # Specify the input folder containing pcd.bin files
    input_folder = "output/samples/LIDAR_TOP"

    # Specify the output folder for converted PCD files
    output_folder = input_folder + "_pcd"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in tqdm.tqdm(os.listdir(input_folder)):
        # Check if the file is a pcd.bin file
        if filename.endswith(".pcd.bin"):
            # Read the pcd.bin file
            with open(os.path.join(input_folder, filename), "rb") as f:
                data = f.read()

            # Unpack the binary data into a NumPy array
            pcd_bin = np.frombuffer(data, dtype=np.float32)

            # Reshape the data into a 3D pointcloud
            pcd_bin = pcd_bin.reshape(-1, 5)[:, 0:3]

            # Create an Open3D pointcloud from the NumPy array
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(pcd_bin)

            # Save the pointcloud as a PCD file
            output_filename = filename.replace(".pcd.bin", ".pcd")
            o3d.io.write_point_cloud(os.path.join(output_folder, output_filename), pcd)

if __name__ == "__main__":
    bin2pcd()