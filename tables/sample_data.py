import os
from typing import Any, Dict

import cv2
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from tqdm import tqdm

from messages.transforms import TFBuffer
from utils.combine_lidars import combine_lidars_to_top
from utils.config import Config
from utils.utils import create_dir, generate_token

from .ego_pose import EgoPose
from .sample import Sample
from .scene import Scene
from .sensor import Sensor
from .table import Table

schema = {
    "type": "object",
    "properties": {
        "calibrated_sensor_token": {"type": "string"},  # done
        "ego_pose_token": {"type": "string"},
        "fileformat": {"type": "string"},  # done
        "filename": {"type": "string"},  # done
        "height": {"type": "number"},  # done
        "is_key_frame": {"type": "boolean"},
        "next": {"type": "string"},  # done
        "prev": {"type": "string"},  # done
        "sample_token": {"type": "string"},  # done
        "timestamp": {"type": "number"},  # done
        "token": {"type": "string"},  # done
        "width": {"type": "number"},  # done
    },
}


class SampleData(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "sample_data.json")

    def create_record(cls, data: Dict) -> None:
        data["token"] = generate_token()
        super().create_record(
            data
        )  # Assuming this calls the parent class's method to actually save the record

    def group_into_samples(
        self,
        master_sensor_token: str,
        sample_window_ms: int,
        scene: Scene,
        sensors: Sensor,
        sample: Sample,
        egopose: EgoPose,
        tfbuffer: TFBuffer,
        conf: Config,
    ) -> None:
        
        # transfer the data format into dataframe and sort with timestamp
        df = pd.DataFrame(self.records)
        df.sort_values("timestamp", inplace=True)

        # Convert timestamp to DateTimeIndex
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df[~df.duplicated(subset=['timestamp', 'calibrated_sensor_token'])]
        # add ego_pose_token
        for index, row in df.iterrows():
            ego_pose_token = egopose.find_closest_ego_pose_token(row["timestamp"])
            df.at[index, "ego_pose_token"] = ego_pose_token

        # Set timestamp as index
        df.set_index("timestamp", drop=True, inplace=True)
        samples_df = self._create_samples(
            scene=scene,
            sample=sample,
            df=df,
            master_sensor_token=master_sensor_token,
            sample_window_ms=sample_window_ms,
        )

        df = self._assign_samples(df, samples_df)
        df = self._set_prev_and_next(df)

        # run a check to see if the sampling window is ok
        self._check_sampling(df, sensors, scene.data["name"])

        # add is_key_frame flag
        df = self._set_is_key_frame(df, master_sensor_token)
        # df = combine_lidars_to_top(
        #     df,
        #     tf_buffer=tfbuffer,
        #     conf=conf,
        # )
        self.records = df.to_dict(orient="records")
    
    def group_into_samples_without_odm(
        self,
        master_sensor_token: str,
        sample_window_ms: int,
        scene: Scene,
        sensors: Sensor,
        sample: Sample,
        egopose: EgoPose,
        tfbuffer: TFBuffer,
        conf: Config,
    ) -> None:
        df = pd.DataFrame(self.records)
        print(df)
        df.sort_values("timestamp", inplace=True)

        # Convert timestamp to DateTimeIndex
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df[~df.duplicated(subset=['timestamp', 'calibrated_sensor_token'])]

        # add ego_pose_token
        if len(egopose.records) == 0:
            print("⚠️ No odometry found, using a static ego pose (car stationary).")

            import uuid, time
            # create a static ego pose at origin
            static_ego_pose = {
                "timestamp": int(time.time() * 1e9),   
                "translation": [0.0, 0.0, 0.0],        
                "rotation": [0.0, 0.0, 0.0, 1.0],      
                "token": str(uuid.uuid4())             
            }
            egopose.records.append(static_ego_pose)

        # give the static ego pose token to all frames first
        static_token = egopose.records[0]["token"]
        df["ego_pose_token"] = static_token
        print(f"✅ All frames assigned to static ego pose token: {static_token}")
        # for index, row in df.iterrows():
        #     ego_pose_token = egopose.find_closest_ego_pose_token(row["timestamp"])
        #     df.at[index, "ego_pose_token"] = ego_pose_token

        # Set timestamp as index
        df.set_index("timestamp", drop=True, inplace=True)
        
        samples_df = self._create_samples(
            scene=scene,
            sample=sample,
            df=df,
            master_sensor_token=master_sensor_token,
            sample_window_ms=sample_window_ms,
        )

        df = self._assign_samples(df, samples_df)
        df = self._set_prev_and_next(df)

        # run a check to see if the sampling window is ok
        self._check_sampling(df, sensors, scene.data["name"])

        # add is_key_frame flag
        df = self._set_is_key_frame(df, master_sensor_token)
        # df = combine_lidars_to_top(
        #     df,
        #     tf_buffer=tfbuffer,
        #     conf=conf,
        # )
        self.records = df.to_dict(orient="records")

    def _create_samples(
        self,
        scene: Scene,
        sample: Sample,
        df: pd.DataFrame,
        master_sensor_token: str,
        sample_window_ms: int,
    ) -> pd.DataFrame:
        # All the code below is designed for master sensor only
        # Filter master sensor entries

        master_sensor_df = df[df.calibrated_sensor_token == master_sensor_token].copy()

        if master_sensor_df.empty:
            raise Exception(
                f"No sample data for master sensor {master_sensor_token} found"
            )

        master_sensor_start_time = master_sensor_df.index[0]
        master_sensor_df.loc[:,"timestamp"] = master_sensor_df.index
        
        # Resample with time window (binning) and choose nearest master sensor measurement.
        samples_df = master_sensor_df.resample(
            pd.Timedelta(milliseconds=sample_window_ms),
            origin=master_sensor_start_time,
        ).nearest(limit=1)
        samples_df = samples_df.set_index("timestamp")
        # Drop bins without master sensor measurement
        samples_df.dropna(inplace=True)

        # Rename index to avoid overlap with columns
        # Index contains uniform time stamps, column "timestamp" actual measuring time.
        samples_df.index.name = "bin"
        ## Drop first row to ensure completeness of the data:
        samples_df = samples_df.iloc[1:]
        # Create the actual Sample-object as a new column
        sample_tokens = []  # Store sample tokens here
        for index, row in samples_df.iterrows():
            sec = index.value // 10**9
            nsec = index.value % 10**9
            timestamp_sec = sec + nsec / 10**9
            sample.create_record(timestamp_sec, scene)
            sample_tokens.append(sample.get_last_token())
        # Delete next from last sample
        sample.delete_next_last()
        # Assign the sample tokens to the DataFrame
        samples_df["sample_token"] = sample_tokens
        samples_df["is_key_frame"]=True
        return samples_df

    def _assign_samples(
        self, df: pd.DataFrame, samples_df: pd.DataFrame
    ) -> pd.DataFrame:
        df = pd.concat([samples_df, df])

        # Reset the index (optional)
        df.reset_index(inplace=True, names="timestamp")
        samples_df.reset_index(inplace=True, names="timestamp")

        # Drop duplicate rows based on all columns
        df.drop_duplicates(
            subset=["token", "calibrated_sensor_token"], inplace=True
        )
        df.sort_values("timestamp", inplace=True)

        # add missing sample tokens
        # Initialize an empty list to store the sample tokens
        sample_tokens = []

        # Iterate over each row in df1
        # align the sample with the closest timestamp in samples_df
        for index, row in df.iterrows():
            if pd.isna(row["sample_token"]):
                # Find the closest timestamp in df2
                closest_timestamp_idx = np.argmin(
                    np.abs(samples_df["timestamp"] - row["timestamp"])
                )

                # Get the corresponding sample token from df2
                sample_token = samples_df.loc[closest_timestamp_idx, "sample_token"]
            else:
                sample_token = row["sample_token"]
            # Append the sample token to the list
            sample_tokens.append(sample_token)

        # Add the list of sample tokens as a new column to df1
        df["sample_token"] = sample_tokens

        # Convert timestamp to unix time (seconds and nanoseconds)
        sec = df["timestamp"].astype(np.int64) // 10**9
        nsec = df["timestamp"].astype(np.int64) % 10**9
        df["timestamp"] = sec + nsec / 10**9
        df.loc[:,"is_key_frame"] = df["is_key_frame"].convert_dtypes().fillna(False)
        return df

    def _set_prev_and_next(self, df: pd.DataFrame) -> pd.DataFrame:
        # Sort the DataFrame by calibrated_sensor_token and timestamp
        df_return = df.sort_values(by=["calibrated_sensor_token", "timestamp"])

        # Shift the 'token' column to get the next event token within the same calibrated_sensor_token
        df_return["next"] = df_return.groupby("calibrated_sensor_token")["token"].shift(-1)

        # Shift the 'token' column to get the previous event token within the same calibrated_sensor_token
        df_return["prev"] = df_return.groupby("calibrated_sensor_token")["token"].shift(1)

        # Fill NaN values with an empty string
        df_return["next"] = df_return["next"].fillna("")
        df_return["prev"] = df_return["prev"].fillna("")
        df_return = df_return.sort_values(by="timestamp")
        return df_return

    def _check_sampling(self, df: pd.DataFrame, sensors: Sensor, scene_name: str) -> None:
        df["count"] = df.groupby("sample_token").calibrated_sensor_token.transform(
            "nunique"
        )
        missing_sensors = df[df["count"] < sensors.get_nbr_sensors()][
            "sample_token"
        ].unique()

        if len(missing_sensors) > 0 and "labeling" in scene_name:
            print("MISSING SENSORS")
            raise Exception(f"Missing sensor for samples: {missing_sensors}")
        

        # if missing_sensors.any():
        #     raise Exception(f"Missing sensor for samples: {missing_sensors}")
        #     ## exception to warning, drop data with missing sensors

    def _set_is_key_frame(self, df: pd.DataFrame, master_sensor_token: str) -> pd.DataFrame:
        # Sort the DataFrame by sample_token and timestamp to ensure correct ordering
        # row wit mastr sensor data 
        master_sensor_keyframe = df["is_key_frame"]==True

        # row with the other sensor data
        no_master_sensor = df["calibrated_sensor_token"]!=master_sensor_token
        keyframe_timestamps = df.loc[df['is_key_frame'] == True, 'timestamp']
        df['distance_to_closest_keyframe'] = df['timestamp'].apply(lambda x: min(abs(x - kf) for kf in keyframe_timestamps))
        df_return = df.sort_values(
            by=["sample_token", "calibrated_sensor_token", "distance_to_closest_keyframe"]
        )
        # df.to_csv(
        #     "sorted_df_return.csv",
        #     index=False
        # )

        # for idx, row in df_return.iterrows():
        #     print(f"idx={idx}, sample_token={row['sample_token']}, calibrated_sensor_token={row['calibrated_sensor_token']}, timestamp={row['timestamp']}, dist={row['distance_to_closest_keyframe']}")



        # Create a mask indicating the first occurrence of each calibrated_sensor_token within each sample_token
        is_closest_key_frame = (
            df_return.groupby(["sample_token", "calibrated_sensor_token"]).cumcount()
            == 0
        )
        no_master_sensor_keyframe = no_master_sensor & is_closest_key_frame
        is_keyframe = master_sensor_keyframe | no_master_sensor_keyframe
        # Assign the mask to a new column is_key_frame
        df_return["is_key_frame"] = is_keyframe

        # Convert the first occurrence of each sample_token to True and the rest to False
        df_return["is_key_frame"] = df_return["is_key_frame"].astype(bool)
        for idx, row in df_return.iterrows():
            if bool(row["is_key_frame"]):
                print(
                    f"idx={idx}, "
                    f"sample_token={row['sample_token']}, "
                    f"calibrated_sensor_token={row['calibrated_sensor_token']}, "
                    f"timestamp={row['timestamp']}, "
                    f"dist={row['distance_to_closest_keyframe']}"
                )


        # Replace "samples" with "sweeps" in the filename column where is_key_frame is False
        df_return.loc[~df_return["is_key_frame"], "filename"] = df_return.loc[
            ~df_return["is_key_frame"], "filename"
        ].str.replace("samples", "sweeps")

        return df_return

    def _save_image(self, filename: os.PathLike, im: NDArray) -> None:
        filename = os.path.join("output", filename)

        create_dir(filename)

        cv2.imwrite(filename, im)

    def _save_pointcloud(self, filename: os.PathLike, points: np.ndarray) -> None:
        filename = os.path.join("output", filename)

        create_dir(filename)
        # Save the points to a binary file
        points.tofile(filename)

    def write_table(self) -> None:
        new_records = []
        for record in tqdm(
            self.records, desc="Saving samples/sweeps", total=len(self.records)
        ):
            if record["fileformat"] in ["jpg", "png"]:
                self._save_image(filename=record["filename"], im=record["filedata"])
            elif record["fileformat"] in ["pcd", "pcd.bin"]:
                self._save_pointcloud(
                    filename=record["filename"], points=record["filedata"]
                )
            elif record["fileformat"] == "npy":
                # use the function for pointcloud to save numpy array
                self._save_pointcloud(
                    filename=record["filename"], points=record["filedata"]
                )

            record.pop("filedata", None)
            record.pop("count", None)

            new_records.append(record)
        self.records = new_records

        super().write_table()
    
    def _fill_missing_sensors_by_global_nearest(
        self,
        df: pd.DataFrame,
        master_sensor_token: str,
        sensor_tokens_to_fill,
        make_filled_as_keyframe: bool = True,
        force_samples_path_for_filled: bool = False,
    ) -> pd.DataFrame:


        df_out = df.copy()

        # master rows & master timestamp per sample
        master_rows = df_out[df_out["calibrated_sensor_token"] == master_sensor_token]
        if master_rows.empty:
            # no master -> nothing to fill
            return df_out

        master_time_by_sample = master_rows.groupby("sample_token")["timestamp"].first()

        # decide which sensors we want to fill
        all_sensors = df_out["calibrated_sensor_token"].unique().tolist()
        if sensor_tokens_to_fill is None:
            sensor_tokens_to_fill = [s for s in all_sensors if s != master_sensor_token]
        else:
            # remove master if user accidentally included
            sensor_tokens_to_fill = [s for s in sensor_tokens_to_fill if s != master_sensor_token]

        # present (sample, sensor) pairs
        present_pairs = set(zip(df_out["sample_token"], df_out["calibrated_sensor_token"]))

        rows_to_add = []

        # Pre-split df by sensor for speed (avoid filtering repeatedly)
        df_by_sensor = {s: sdf for s, sdf in df_out.groupby("calibrated_sensor_token")}

        for sample_tok, t_master in master_time_by_sample.items():
            for sensor_tok in sensor_tokens_to_fill:
                if (sample_tok, sensor_tok) in present_pairs:
                    continue  # already has this sensor in this sample

                candidates = df_by_sensor.get(sensor_tok, None)
                if candidates is None or candidates.empty:
                    continue  # no such sensor globally

                # nearest row in this sensor stream to master timestamp
                idx_nearest = (candidates["timestamp"] - t_master).abs().idxmin()
                nearest_row = candidates.loc[idx_nearest].copy()

                # "move" it into the missing sample
                nearest_row["sample_token"] = sample_tok

                if make_filled_as_keyframe:
                    nearest_row["is_key_frame"] = True

                # if distance column exists, update or create it
                nearest_row["distance_to_closest_keyframe"] = abs(nearest_row["timestamp"] - t_master)

                # optional filename tweak
                if force_samples_path_for_filled and "filename" in nearest_row.index:
                    nearest_row["filename"] = str(nearest_row["filename"]).replace("sweeps", "samples")

                rows_to_add.append(nearest_row)

        if rows_to_add:
            df_out = pd.concat([df_out, pd.DataFrame(rows_to_add)], ignore_index=True)

        return df_out

