#!/bin/bash

# Set the base directory containing all the folders you want to process.
BASE_DIR="/media/esteban/8a1ab513-6f51-4d75-bc94-da244f38ae65/toolsad-04/EDGAR_processed/to_label/processed/"

# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
  echo "Error: Directory not found: $BASE_DIR"
  exit 1
fi

echo "🚀 Starting to process folders in $BASE_DIR..."

# Loop through each item in the base directory
# The "*/" at the end ensures we only match directories
for folder in "$BASE_DIR"/*/
do
  # Check if it is a directory before processing
  if [ -d "$folder" ]; then
    echo "-----------------------------------------"
    echo "Processing: $folder"
    python utils/swap_left_right.py "$folder"
  fi
done

echo "-----------------------------------------"
echo "✅ All folders processed."