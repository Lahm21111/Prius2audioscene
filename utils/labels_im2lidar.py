import os

import matplotlib.pyplot as plt
import numpy as np
from nuscenes.nuscenes import NuScenes
from shapely.geometry import Point, Polygon
from tqdm import tqdm

from tables.lidarseg import LidarSeg
from utils.map_lidar_image import map_pointcloud_to_image
from utils.utils import read_json

DRIVEABLE_SPACE = 24
OTHER = 29


def label_lidar(
    nusc: NuScenes,
    sample: dict,
    lidarseg: LidarSeg,
    camera: str = "CAMERA_FRONT_CENTER",
    lidar: str = "LIDAR_TOP",
    plot: bool = False,
):
    lidar_token = sample["data"][lidar]
    filename = os.path.join(lidarseg.output_path, lidar_token + "_lidarseg.bin")

    # Project pointcloud to image
    points, coloring, im = map_pointcloud_to_image(
        nusc=nusc,
        pointsensor_token=lidar_token,
        camera_token=sample["data"][camera],
    )

    # Get labels
    path_labels = (
        nusc.get_sample_data_path(sample["data"][camera])
        .replace(f"samples/{camera}", f"samples/{camera}/label")
        .replace(".jpeg", ".json")
    )
    labels = read_json(path_labels)

    # Create a polygon for the label "drivable space"
    polygon = Polygon(labels["shapes"][0]["points"])

    # Check if each point is inside the polygon
    is_inside = [polygon.contains(Point(p[0], p[1])) for p in points.T]

    # Set the color of the points based on whether they are inside the polygon
    colors = np.array(
        [DRIVEABLE_SPACE if inside else OTHER for inside in is_inside], dtype=np.int8
    )

    # Save lidarseg info
    data = {
        "token": lidar_token,
        "sample_data_token": lidar_token,
        "filename": filename,
    }
    lidarseg.create_record(data)
    colors.tofile(
        os.path.join("output", filename),
    )

    # Plot the points
    if plot:
        fig, ax = plt.subplots(1, 1, figsize=(9, 16))
        ax.imshow(im)
        ax.scatter(points[0, :], points[1, :], c=coloring, s=1)
        ax.plot(*polygon.exterior.xy)
        ax.scatter(points[0, :], points[1, :], c=colors, s=1)
        ax.axis("off")
        plt.show()


def main(
    camera: str = "CAMERA_FRONT_CENTER", lidar: str = "LIDAR_TOP", plot: bool = False
):
    # Load dataset
    nusc = NuScenes(version="v1.0-test", dataroot="./output", verbose=True)
    lidarseg = LidarSeg()
    for sample in tqdm(nusc.sample, total=len(nusc.sample), desc="Generating lidarseg"):
        label_lidar(nusc=nusc, sample=sample, lidarseg=lidarseg, plot=plot)
    lidarseg.write_table()


if __name__ == "__main__":
    main(plot=False)
