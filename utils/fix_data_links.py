import argparse
import json
import pandas as pd
from nuscenes.nuscenes import NuScenes
from pathlib import Path

def main(version: str, dataroot: str, output_path: str):
    print(f"Loading NuScenes dataset (version: {version}, root: {dataroot})...")
    nusc = NuScenes(version=version, dataroot=dataroot, verbose=False)

    print("Building DataFrame...")
    df = pd.DataFrame(nusc.sample_data)
    sample_df = pd.DataFrame(nusc.sample)
    sample_map = sample_df.set_index('token')['scene_token'].to_dict()
    df['scene_token'] = df['sample_token'].map(sample_map)

    print("Sorting by scene_token, channel, timestamp...")
    df.sort_values(by=['scene_token', 'channel', 'timestamp'], inplace=True)

    print("Assigning prev/next links...")
    grouped = df.groupby(['scene_token', 'channel'])
    df['prev'] = grouped['token'].shift(1).fillna('').astype(str)
    df['next'] = grouped['token'].shift(-1).fillna('').astype(str)

    result = df.to_dict(orient='records')

    print(f"Saving to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

    print(f"Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fixes the prev/next tokens in the sample_data.json of a NuScenes style dataset.")
    parser.add_argument("version", help="NuScenes dataset version, e.g., v1.0-mini or v1.0-trainval")
    parser.add_argument("dataroot", help="Path to the root of the NuScenes dataset")
    parser.add_argument("-o", "--output", help="Path to output JSON file. Defaults to '<dataroot>/<version>/sample_data.json' if not set")

    args = parser.parse_args()

    if args.output is None:
        output_file = Path(args.dataroot) / Path(args.version) / "sample_data.json"
    else:
        output_file = Path(args.output)
        if output_file.suffix.lower() != ".json":
            raise TypeError(f"Unsupported file type. Expected '.json' but got '{output_file.suffix.lower()}'")
        output_file.parent.mkdir(parents=True, exist_ok=True)

    main(args.version, args.dataroot, str(output_file))
