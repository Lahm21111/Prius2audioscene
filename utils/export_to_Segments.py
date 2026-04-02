#!/usr/bin/env python3
# viz_and_upload_nuscenes_axes_consistent.py
#
# Visualize (and optionally upload) nuScenes LiDAR keyframes placed in WORLD using:
#   T_gs_raw = (global <- ego) @ (ego <- sensor_can) @ M_raw_to_can
#
# IMPORTANT: We DO NOT remap the point arrays; we fold the axis-fix into the POSE.
# This keeps the vehicle icon/upright orientation consistent with the data.
#
# Usage (visualize only):
#   python viz_and_upload_nuscenes_axes_consistent.py \
#     --dataroot /path --version v1.0-test --channel LIDAR_TOP \
#     --max_frames 50 --voxel 0.07 --raw_axes yzx --raw_signs "++-"
#
# Upload (optional):
#   export SEGMENTS_API_KEY=your_key
#   python viz_and_upload_nuscenes_axes_consistent.py ... \
#     --upload --dataset pmignot/test_track_dataset --sample_name first50_world_axes_fixed \
#     --bin_type nuscenes

from __future__ import annotations
import os, sys, time, math, argparse
from pathlib import Path
from typing import List, Tuple
import numpy as np
from pyquaternion import Quaternion
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from segments import SegmentsClient
import open3d as o3d


# ---------------- nuScenes transforms ----------------


def iter_keyframes_sorted(nusc: NuScenes, channel: str) -> List[str]:
    sds = []
    for s in nusc.sample:
        sd_tok = s["data"].get(channel)
        if not sd_tok: continue
        sd = nusc.get("sample_data", sd_tok)
        if not sd.get("is_key_frame", False): continue
        ep = nusc.get("ego_pose", sd["ego_pose_token"])
        sds.append((ep["timestamp"], sd_tok))
    sds.sort(key=lambda x: x[0])
    return [t for _, t in sds]

# ---------------- Open3D helpers ----------------

def color_wheel(n: int):
    hsv = np.stack([np.linspace(0,1,n,endpoint=False),
                    np.full(n,0.85), np.full(n,0.95)],1)
    out=[]
    for h,s,v in hsv:
        i=int(h*6); f=h*6-i; p=v*(1-s); q=v*(1-s*f); t=v*(1-s*(1-f)); i%=6
        if i==0: r,g,b=v,t,p
        elif i==1: r,g,b=q,v,p
        elif i==2: r,g,b=p,v,t
        elif i==3: r,g,b=p,q,v
        elif i==4: r,g,b=t,p,v
        else:      r,g,b=v,p,q
        out.append((r,g,b))
    return np.asarray(out,float)

def axes_at(T: np.ndarray, size=1.2):
    R,t = T[:3,:3], T[:3,3]
    pts = np.vstack([t, t+R@np.array([size,0,0]), t, t+R@np.array([0,size,0]), t, t+R@np.array([0,0,size])])
    lines = np.array([[0,1],[2,3],[4,5]], np.int32)
    ls = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(pts.astype(float)),
                              lines=o3d.utility.Vector2iVector(lines))
    ls.colors = o3d.utility.Vector3dVector(np.array([[1,0,0],[0,1,0],[0,0,1]], float))
    return ls

# ---------------- Transform points ----------------
def transform_points(mat, points):
    """Apply 4x4 homogenous coordinate transform to Nx3 points."""
    return mat[:3, :3].dot(points.T).T + mat[:3, 3][None]
# ---------------- Segments upload (optional) ----------------

def require_api_key() -> str:
    api = os.environ.get("SEGMENTS_API_KEY")
    if not api:
        sys.exit("Set SEGMENTS_API_KEY to your Segments.ai API key.")
    return api

def write_temp(points_xyz: np.ndarray, intens: np.ndarray, bin_type: str) -> Tuple[Path, str]:
    """Return (path, segments_type). points_xyz is (3,N) already in sensor RAW frame."""
    import tempfile
    N = points_xyz.shape[1]
    if bin_type == "nuscenes":
        ring = np.zeros((1,N), np.float32)
        arr  = np.vstack([points_xyz.astype(np.float32), intens.reshape(1,-1), ring]).T  # (N,5)
        p = Path(tempfile.mkstemp(suffix=".pcd.bin")[1]); arr.tofile(str(p)); return p, "nuscenes"
    elif bin_type == "binary-xyzi":
        arr = np.vstack([points_xyz.astype(np.float32), intens.reshape(1,-1)]).T       # (N,4)
        p = Path(tempfile.mkstemp(suffix=".bin")[1]); arr.tofile(str(p)); return p, "binary-xyzi"
    elif bin_type == "pcd":
        p = Path(tempfile.mkstemp(suffix=".pcd")[1])
        header = (
            "VERSION .7\nFIELDS x y z intensity\nSIZE 4 4 4 4\nTYPE F F F F\nCOUNT 1 1 1 1\n"
            f"WIDTH {N}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {N}\nDATA binary\n"
        )
        with open(p,"wb") as f:
            f.write(header.encode("ascii"))
            payload = np.hstack([points_xyz.T.astype(np.float32),
                                 intens.reshape(-1,1).astype(np.float32)]).tobytes()
            f.write(payload)
        return p, "pcd"
    else:
        raise ValueError("bin_type must be nuscenes | binary-xyzi | pcd")

def transform_gnss_to_base(ego_translation, ego_quat):
    # First, set the TF from GNSS link to base link

    # tf_gnss_to_base_4x4 = np.array([-1.000, 0.000, 0.000,  1.289,
    #                                  0.000, 0.000, -1.000,  0.435,
    #                                  0.000, -1.000,  0.000, 0.013,
    #                                 0.000,  0.000,  0.000,  1.000]).reshape(4,4)

    # qx = 0.0
    # qy = -math.sqrt(0.5)
    # qz = -math.sqrt(0.5)
    # qw = 0.0
    # gnss_to_base_quat = Quaternion(qw, qx, qy, qz)

    tf_base_to_gnss_4x4 = np.array([-1.000, 0.000, -0.000,  1.289,
                                    -0.000 ,-0.000, -1.000,  0.013,
                                    -0.000, -1.000,  0.000,  0.435,
                                    0.000,  0.000,  0.000,  1.000]).reshape(4,4)


    qx = 0.0
    qy = -math.sqrt(0.5)
    qz = -math.sqrt(0.5)
    qw = 0.0
    base_to_gnss_quat = Quaternion(qw, qx, qy, qz)

    # Now translate to ego vehicle coordinate system
    gnss_to_base_translation = tf_base_to_gnss_4x4[:3, 3]
    print("gnss_to_base_translation:", gnss_to_base_translation)
    # gnss_to_base_quat = Quaternion(matrix=tf_gnss_to_base_4x4[:3, :3])
    print("gnss_to_base_quat:", base_to_gnss_quat)
    center_in_base = ego_translation - gnss_to_base_translation
    print("center_in_base before rotation:", center_in_base)
    center_in_base = np.dot(base_to_gnss_quat.rotation_matrix.T, center_in_base)
    print("center_in_base after rotation:", center_in_base)
    quat_in_base = Quaternion(base_to_gnss_quat.inverse*ego_quat)
    print("quat_in_ego:", quat_in_base)
    return center_in_base, quat_in_base


def process_point_cloud_gnss(pc, ego_translation, ego_quat, offset):

    ego_translation -= offset

    # convert Open3D.o3d.geometry.PointCloud to numpy array
    points = pc.points.T

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    xyz_pcd = np.asarray(pcd.points)

    # First, set the TF from GNSS link to base link

    tf_gnss_to_base_4x4 = np.array([1.000, 0.000, -0.000,  1.289,
                                    -0.000 ,-0.000, -1.000,  0.013,
                                    -0.000, -1.000,  0.000,  0.435,
                                    0.000,  0.000,  0.000,  1.000]).reshape(4,4)

    tf_base_to_gnss_4x4 = np.array([-1.000, 0.000, -0.000,  1.289,
                                    -0.000 ,-0.000, -1.000,  0.435,
                                    -0.000, -1.000,  0.000,  0.013,
                                    0.000,  0.000,  0.000,  1.000]).reshape(4,4)

    # Now translate to ego vehicle coordinate system
    ego_pose_4x4 = np.eye(4)

    ego_pose_4x4[:3, :3] = ego_quat.rotation_matrix

    ego_pose_4x4[:3, 3] = ego_translation

    ego_pose_base_4x4 = ego_pose_4x4 @ tf_gnss_to_base_4x4

    tf_lidar_to_ego_4x4 = ego_pose_base_4x4 @ tf_base_to_gnss_4x4

    xyz_temp = xyz_pcd.copy()

    xyz_new = transform_points(tf_lidar_to_ego_4x4, xyz_temp)
    pcd_ego = o3d.geometry.PointCloud()
    pcd_ego.points = o3d.utility.Vector3dVector(xyz_new)
    return pcd_ego, ego_pose_base_4x4

def process_point_cloud(pc, ego_translation, ego_quat, offset):

    ego_translation -= offset

    # convert Open3D.o3d.geometry.PointCloud to numpy array
    points = pc.points.T

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    xyz_pcd = np.asarray(pcd.points)

    # Now translate to ego vehicle coordinate system
    ego_pose_base_4x4 = np.eye(4)

    ego_pose_base_4x4[:3, :3] = ego_quat.rotation_matrix

    ego_pose_base_4x4[:3, 3] = ego_translation

    xyz_temp = xyz_pcd.copy()

    xyz_new = transform_points(ego_pose_base_4x4, xyz_temp)
    pcd_ego = o3d.geometry.PointCloud()
    pcd_ego.points = o3d.utility.Vector3dVector(xyz_new)
    return pcd_ego, ego_pose_base_4x4

def upload_frames(nusc: NuScenes, sd_tokens: List[str], dataset: str,
                   sample_name: str, bin_type: str):

    print("require api key and create client")
    client = SegmentsClient(require_api_key())
    print("upload frames")
    frames=[]
    for i, sd_tok in enumerate(sd_tokens, start=1):
        pcl_path = nusc.get_sample_data_path(sd_tok)
        pc = LidarPointCloud.from_file(pcl_path)
        ref_sd_record = nusc.get('sample_data', sd_tok)
        ego_pose_token = ref_sd_record['ego_pose_token']
        ego_pose_record = nusc.get('ego_pose', ego_pose_token)
        ego_quat = Quaternion(ego_pose_record['rotation'])
        ego_translation = np.array(ego_pose_record['translation']) 

        # ego_translation, ego_quat = transform_gnss_to_base(ego_translation, ego_quat)

        P = pc.points[:3,:].astype(np.float32)
        I = (pc.points[3,:] if pc.points.shape[0] >= 4 else np.zeros(P.shape[1], np.float32)).astype(np.float32)

        tmp, stype = write_temp(P, I, bin_type)
        for attempt in range(1,5):
            try:
                with open(tmp,"rb") as f: url = client.upload_asset(f, filename=tmp.name).url
                break
            except Exception:
                if attempt==4: raise
                time.sleep(1.5**attempt)
        try: tmp.unlink(missing_ok=True)
        except Exception: pass

        sd = nusc.get("sample_data", sd_tok)
        print(f"Frame {i}/{len(sd_tokens)} ts in ns {sd['timestamp']}...")
        ts_ns = sd["timestamp"]
        print(f"Uploading frame {i}/{len(sd_tokens)} ts in ns {ts_ns}...")
        qw, qx, qy, qz = ego_quat.elements
        frames.append({
            "pcd": {"url": url, "type": stype},
            "name": Path(nusc.get_sample_data_path(sd_tok)).name,
            "timestamp": ts_ns,
            "ego_pose": {
                "position": {"x": float(ego_translation[0]), "y": float(ego_translation[1]), "z": float(ego_translation[2])},
                "heading":  {"qx": float(qx), "qy": float(qy), "qz": float(qz), "qw": float(qw)},
            },
        })
        if i==1 or i%10==0 or i==len(sd_tokens):
            print(f"  → uploaded {i}/{len(sd_tokens)}")
    s = client.add_sample(dataset, sample_name, {"frames": frames})
    print(f"✅ Created sample '{s.name}' with {len(frames)} frames.")

# ---------------- Build O3D scene ----------------



def build_geoms(nusc: NuScenes, sd_tokens: List[str],
                voxel: float, color_per_frame: bool):
    geoms=[o3d.geometry.TriangleMesh.create_coordinate_frame(size=2.0)]
    boxes = []
    cols = color_wheel(len(sd_tokens)) if color_per_frame else np.tile(np.array([[0.95,0.95,0.95]],float),(len(sd_tokens),1))
    for i, sd_tok in enumerate(sd_tokens):
        pcl_path = nusc.get_sample_data_path(sd_tok)
        pc = LidarPointCloud.from_file(pcl_path)
        ref_sd_record = nusc.get('sample_data', sd_tok)
        ego_pose_token = ref_sd_record['ego_pose_token']
        ego_pose_record = nusc.get('ego_pose', ego_pose_token)
        ego_quat = Quaternion(ego_pose_record['rotation'])
        ego_translation = np.array(ego_pose_record['translation']) 

        # Correct: first subtract translation (including0, 0] offset), then apply inverse rotation
        offset = np.array([94092, 61855, 0])
        #offset = np.array([0, 0, 0])

        pcd_ego, ego_pose_base_4x4 = process_point_cloud(pc, ego_translation, ego_quat, offset)
        box_unit = o3d.geometry.OrientedBoundingBox(ego_pose_base_4x4[:3, 3], ego_pose_base_4x4[:3, :3], np.array([3, 1, 1]))

        # ego_translation, ego_quat = transform_gnss_to_base(ego_translation, ego_quat)
        # box_unit = o3d.geometry.OrientedBoundingBox(ego_translation, ego_quat.rotation_matrix, np.array([3, 1, 1]))

        geoms.append(pcd_ego)
        boxes.append(box_unit)

        if voxel > 0: pcd_ego = pcd_ego.voxel_down_sample(float(voxel))
        col = np.asarray(cols[i], float)
        pcd_ego.colors = o3d.utility.Vector3dVector(np.tile(col,(np.asarray(pcd_ego.points).shape[0],1)))
        box_unit.color = cols[i]
        geoms.append(pcd_ego)

    return geoms, boxes

# ---------------- Main ----------------
def main():
    ap = argparse.ArgumentParser("Visualize/Upload nuScenes LiDAR in world with axis-consistent poses")
    ap.add_argument("--dataroot", default="/workspaces/Prius2audioscene/dataset/output")
    ap.add_argument("--version", default="v1.0-test")
    ap.add_argument("--channel", default="LIDAR_TOP")
    ap.add_argument("--max_frames", type=int, default=2000)
    ap.add_argument("--voxel", type=float, default=0.01)
    ap.add_argument("--single_color", action="store_true", default=False)
    ap.add_argument("--point_size", type=float, default=2.0)

    # optional upload
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--visualize", action="store_true")
    ap.add_argument("--dataset", default="marioney/test_with_cameras", help="<owner>/<dataset> on Segments.ai")
    ap.add_argument("--sample_name", default="rosbag2_2025_07_02-13_46_40")
    ap.add_argument("--bin_type", choices=["nuscenes","binary-xyzi","pcd"], default="nuscenes")

    args = ap.parse_args()

    nusc = NuScenes(version=args.version, dataroot=args.dataroot, verbose=True)
    sd_all = iter_keyframes_sorted(nusc, args.channel)
    if not sd_all: raise SystemExit(f"No keyframes for {args.channel}")
    sd_tokens = sd_all[:args.max_frames]

    # Visualize
    # Optional upload
    # if args.visualize:
    #     print(f"Visualizing {len(sd_tokens)} keyframes from {args.channel}...")
    #     geoms, boxes = build_geoms(nusc, sd_tokens, voxel=args.voxel,
    #                         color_per_frame=(not args.single_color))
    #     vis = o3d.visualization.Visualizer()
    #     vis.create_window(window_name=f"{args.channel} | world overlay (axes fixed in POSE) | N={len(sd_tokens)}", width=1400, height=900)
    #     for g in geoms: vis.add_geometry(g)
    #     for b in boxes: vis.add_geometry(b)
    #     opt = vis.get_render_option(); opt.point_size=float(args.point_size); opt.background_color=np.asarray([0,0,0])
    #     vis.run(); vis.destroy_window()

    # Optional Upload frames
    args.upload = True
    args.dataset = "shiming/AcousticScenes"
    if args.upload:
        upload_frames(nusc, sd_tokens, dataset=args.dataset, sample_name=args.sample_name, bin_type=args.bin_type)


if __name__ == "__main__":
    main()