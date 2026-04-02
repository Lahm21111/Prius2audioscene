# visualize_nusc_like.py
# Quick BEV visualizer for NuScenes-like datasets exported by Prius2audioscene.
# Author: Ziang’s helper :)

import os
import json
import math
import argparse
from collections import defaultdict, OrderedDict

import numpy as np
import matplotlib.pyplot as plt

# ============ Utils ============

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def quat_to_yaw(qw, qx, qy, qz):
    """Return yaw (rotation around Z) in radians from [qw, qx, qy, qz]."""
    # yaw = atan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    return math.atan2(siny_cosp, cosy_cosp)

def box_corners_xy(translation, size, yaw):
    """
    NuScenes size = [w, l, h] where:
      w: width (y axis extent), l: length (x axis extent)
    Return 4x2 XY corners in counter-clockwise order.
    """
    w, l, _ = size
    x, y, _ = translation
    dx = l / 2.0
    dy = w / 2.0
    # local corners (x forward, y left)
    corners = np.array([
        [ dx,  dy],
        [ dx, -dy],
        [-dx, -dy],
        [-dx,  dy],
    ])  # shape (4,2)

    c = math.cos(yaw)
    s = math.sin(yaw)
    R = np.array([[c, -s],
                  [s,  c]], dtype=np.float32)
    world = corners @ R.T
    world[:, 0] += x
    world[:, 1] += y
    return world

def try_load_lidar_xy(filepath):
    """
    Try to load lidar points as Nx(>=3) float32 (NuScenes .bin).
    Returns Nx2 XY or None.
    """
    if not os.path.isfile(filepath):
        return None
    try:
        if filepath.endswith(".bin"):
            pts = np.fromfile(filepath, dtype=np.float32)
            if pts.size % 5 == 0:
                pts = pts.reshape(-1, 5)  # x,y,z,intensity,ring
            elif pts.size % 4 == 0:
                pts = pts.reshape(-1, 4)  # x,y,z,intensity
            elif pts.size % 3 == 0:
                pts = pts.reshape(-1, 3)  # x,y,z
            else:
                # Unknown layout
                return None
            xy = pts[:, :2]
            return xy
        elif filepath.endswith(".pcd"):
            # Optional: need open3d
            try:
                import open3d as o3d
                pcd = o3d.io.read_point_cloud(filepath)
                pts = np.asarray(pcd.points)
                if pts.shape[1] >= 2:
                    return pts[:, :2]
                return None
            except Exception:
                return None
        else:
            return None
    except Exception:
        return None

# ============ Indexing ============

def build_indices(root, version):
    """Load tables and build useful indices."""
    vpath = os.path.join(root, version)
    req = ["scene.json", "sample.json", "sample_data.json", "sample_annotation.json", "category.json"]
    for f in req:
        if not os.path.isfile(os.path.join(vpath, f)):
            raise FileNotFoundError(f"Missing {f} in {vpath}")

    scenes = load_json(os.path.join(vpath, "scene.json"))
    samples = load_json(os.path.join(vpath, "sample.json"))
    sdata   = load_json(os.path.join(vpath, "sample_data.json"))
    annos   = load_json(os.path.join(vpath, "sample_annotation.json"))
    cats    = load_json(os.path.join(vpath, "category.json"))

    scene_by_token = {s["token"]: s for s in scenes}
    sample_by_token = {s["token"]: s for s in samples}
    cat_name_by_token = {c["token"]: c["name"] if "name" in c else c.get("category_name", "") for c in cats}

    # sample -> sample_data list
    sample_to_sdata = defaultdict(list)
    for sd in sdata:
        sample_to_sdata[sd["sample_token"]].append(sd)

    # sample -> annotations list
    sample_to_annos = defaultdict(list)
    for a in annos:
        sample_to_annos[a["sample_token"]].append(a)

    # scene -> ordered sample tokens (by timestamp)
    scene_to_samples = defaultdict(list)
    for s in samples:
        scene_to_samples[s["scene_token"]].append(s)
    for k in scene_to_samples:
        scene_to_samples[k] = list(sorted(scene_to_samples[k], key=lambda x: x["timestamp"]))

    # Also index SD by channel for quick lookup (e.g., LIDAR_TOP)
    def sdata_channel_map(sample_token):
        by_ch = {}
        for sd in sample_to_sdata.get(sample_token, []):
            ch = sd.get("channel") or sd.get("sensor_channel") or ""
            by_ch[ch] = sd
        return by_ch

    return dict(
        scenes=scenes,
        scene_by_token=scene_by_token,
        samples=samples,
        sample_by_token=sample_by_token,
        sample_to_sdata=sample_to_sdata,
        sample_to_annos=sample_to_annos,
        scene_to_samples=scene_to_samples,
        sdata_channel_map=sdata_channel_map,
        cat_name_by_token=cat_name_by_token,
        vpath=vpath
    )

# ============ Visualizer ============

class BevPlayer:
    def __init__(self, indices, scene_name=None, lidar_channel="LIDAR_TOP"):
        self.idc = indices
        self.lidar_channel = lidar_channel
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title("NuScenes-like BEV Visualizer")
        self.fig.tight_layout()
        self.ax.set_aspect("equal", adjustable="box")

        # pick scene
        if scene_name is None:
            # take first scene
            scene = self.idc["scenes"][0]
        else:
            # match by name (case sensitive)
            matched = [s for s in self.idc["scenes"] if s.get("name", "") == scene_name]
            if not matched:
                print(f"[Warn] Scene '{scene_name}' not found. Using the first scene.")
                scene = self.idc["scenes"][0]
            else:
                scene = matched[0]

        self.scene = scene
        self.sample_list = self.idc["scene_to_samples"][scene["token"]]
        self.frame = 0

        self.cid = self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.redraw()

    def on_key(self, e):
        if e.key == "right":
            self.frame = min(self.frame + 1, len(self.sample_list) - 1)
            self.redraw()
        elif e.key == "left":
            self.frame = max(self.frame - 1, 0)
            self.redraw()
        elif e.key in ("q", "escape"):
            plt.close(self.fig)

    def redraw(self):
        self.ax.clear()
        self.ax.set_title(f"Scene: {self.scene.get('name','(no name)')} | Frame {self.frame+1}/{len(self.sample_list)}")
        self.ax.set_xlabel("X (m, forward)")
        self.ax.set_ylabel("Y (m, left)")
        self.ax.grid(True, linestyle=":", linewidth=0.5)

        sample = self.sample_list[self.frame]
        sample_token = sample["token"]

        # 1) draw lidar XY (optional)
        ch_map = self.idc["sdata_channel_map"](sample_token)
        lidar_sd = ch_map.get(self.lidar_channel, None)
        if lidar_sd is not None:
            # NuScenes-style sample_data has "filename" relative to dataset root/version
            rel = lidar_sd.get("filename") or lidar_sd.get("file_name") or ""
            fp = os.path.join(self.idc["vpath"], rel)
            xy = try_load_lidar_xy(fp)
            if xy is not None and xy.size > 0:
                # downsample if too many points
                if xy.shape[0] > 200000:
                    idx = np.random.choice(xy.shape[0], size=200000, replace=False)
                    xy = xy[idx]
                self.ax.scatter(xy[:, 0], xy[:, 1], s=0.2, alpha=0.4)

        # 2) draw boxes from sample_annotation
        annos = self.idc["sample_to_annos"].get(sample_token, [])
        for a in annos:
            trans = a.get("translation", [0, 0, 0])
            size  = a.get("size", [1, 1, 1])
            rot   = a.get("rotation", [1, 0, 0, 0])  # qw,qx,qy,qz
            yaw = quat_to_yaw(rot[0], rot[1], rot[2], rot[3])
            corners = box_corners_xy(trans, size, yaw)
            poly = np.vstack([corners, corners[0:1]])  # close the loop
            self.ax.plot(poly[:, 0], poly[:, 1], linewidth=2)

            # heading arrow
            heading = np.array([ [0.6*size[1], 0.0] ])  # 60% length forward in local
            c = math.cos(yaw); s = math.sin(yaw)
            R = np.array([[c, -s],[s, c]], dtype=np.float32)
            arrow = (heading @ R.T) + np.array([[trans[0], trans[1]]])
            self.ax.arrow(trans[0], trans[1], arrow[0,0]-trans[0], arrow[0,1]-trans[1],
                          head_width=0.3, head_length=0.5, length_includes_head=True)

            # label text
            cname = a.get("category_name", "")
            self.ax.text(trans[0], trans[1], cname, fontsize=8, ha="center", va="bottom")

        # nice BEV limits (auto or fixed window)
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(-50, 50)
        self.ax.set_aspect("equal", adjustable="box")
        self.fig.canvas.draw_idle()

# ============ Main ============

def main():
    parser = argparse.ArgumentParser(description="Quick BEV visualizer for NuScenes-like dataset.")
    parser.add_argument("--root", default="/workspaces/Prius2audioscene/dataset/output",type=str, help="Path to dataset root that contains versions (e.g., v1.0-test)")
    parser.add_argument("--version", default="v1.0-test", type=str, help="Version folder name, e.g., v1.0-test")
    parser.add_argument("--scene_name", default="rosbag2_2025_08_21-13_56_45", type=str, help="Optional scene name to open directly")
    parser.add_argument("--lidar_channel", default="LIDAR_TOP", type=str, help="SampleData channel for lidar (default: LIDAR_TOP)")
    args = parser.parse_args()

    indices = build_indices(args.root, args.version)
    BevPlayer(indices, scene_name=args.scene_name, lidar_channel=args.lidar_channel)
    print("Controls: ← → to step frames, q to quit.")
    plt.savefig("output_bev.png", dpi=200)
    print("Saved visualization to output_bev.png")

if __name__ == "__main__":
    main()
