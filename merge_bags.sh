#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

folder="$1"

# Check if the provided folder exists
if [ ! -d "$folder" ]; then
  echo "Error: Folder '$folder' not found."
  exit 1
fi

# Find all .mcap files recursively and store paths in an array
mapfile -t mcap_files < <(find "$folder" -type f -name '*.mcap')

# Display the paths of .mcap files found
echo "Found ${#mcap_files[@]} .mcap files:"
for file in "${mcap_files[@]}"; do
  echo "$file"
done

# Prepare the ros2 bag convert command with all .mcap files
cmd="ros2 bag convert"
for file in "${mcap_files[@]}"; do
  cmd+=" --input $file mcap"
done

cmd+=" -o merge_bags_config.yaml"
# Print the final command
echo "Executing command:"
echo "$cmd"

# Uncomment the line below to execute the command
eval "$cmd"
