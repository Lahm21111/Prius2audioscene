# Dataset Preparation Guide

This document describes the full workflow for converting a rosbag into the dataset format, aligning annotations from Segments.ai, and optionally uploading the dataset back to Segments.

---

<!-- ## Prerequisites

Before starting, make sure that:

- the project has been reopened in the development container
- the rosbag file is available
- the annotation file can be downloaded from Segments.ai

--- -->

## Directory Overview

```text
.
├── rosbag/
├── dataset/
│   └── labels/
├── rosbag2nuscene.py
└── utils/
    ├── export_to_Segments.py
    └── create_annotations_fromSegments.py
```

## Step-by-Step Instructions

### 1. Reopen the project in the container

First, reopen the project in the container environment.

### 2. Add the rosbag file

Place the rosbag file into the `rosbag/` directory.

Example:

```text
rosbag/your_bag_name.bag
```

### 3. Convert the rosbag to dataset format

Open `rosbag2nuscene.py`, copy the rosbag filename, and set the `bag_name` variable.

Example:

```python
bag_name = "your_rosbag_folder"
```

Please copy the name of the rosbag to line 13 in `rosbag2nuscene.py` and run:

```python
python rosbag2nuscene.py
```

This step converts the rosbag into the dataset format.

### 4. Download the annotation file from Segments.ai

Download the annotation file from Segments.ai and place it into:

`dataset/labels/`

### 5. Move the generated output to the dataset directory

After the conversion is complete, move the generated output (`output/`) into the `dataset/` directory if it is not already there.

### 6. Align the annotations

Open `utils/create_annotations_fromSegments.py`, change the bag name to match the current rosbag, and run the script.

Example:

```python
python utils/create_annotations_fromSegments.py
```

This step aligns the downloaded annotations with the generated dataset.

### 7. Optional: Upload the dataset to Segments.ai

If you want to upload the dataset to Segments.ai, open `utils/export_to_Segments.py`, change args.dataset (line 348) to the target dataset name and the name of the sample (scene) in line 323, and run the script.

Example:

```python
python utils/export_to_Segments.py
```
