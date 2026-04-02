import os
import rosbag2_py
from datetime import timedelta

def split_rosbag(input_bag_path, output_dir, split_duration_sec):
    """
    Splits a ROS 2 bag file into smaller bags of a specified duration.

    Args:
        input_bag_path (str): Path to the input ROS 2 bag file.
        output_dir (str): Directory to save the split bags.
        split_duration_sec (int): Duration of each split bag in seconds.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the input bag
    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=input_bag_path, storage_id='mcap')
    converter_options = rosbag2_py.ConverterOptions('', '')
    reader.open(storage_options, converter_options)

    # Get metadata and topics
    metadata = reader.get_metadata()
    topics = [topic_info.topic_metadata.name for topic_info in metadata.topics_with_message_count]

    # Initialize writer for split bags
    writer = rosbag2_py.SequentialWriter()
    split_index = 0
    split_start_time = None
    split_end_time = None
    tf_static_msgs_data = []
    tf_static_timestamps_delta = []


    # Iterate through messages
    while reader.has_next():
        (topic, data, timestamp) = reader.read_next()
        # Store the `tf_static` topic value
        



        # Initialize split start and end times
        if split_start_time is None:
            split_start_time = timestamp
            split_end_time = split_start_time + int(split_duration_sec * 1e9)  # Convert seconds to nanoseconds

            # Open a new split bag
            split_bag_path = os.path.join(output_dir, f"moving_ego_vehicle_{split_index+7}")
            writer.open(
                rosbag2_py.StorageOptions(uri=split_bag_path, storage_id='mcap'),
                rosbag2_py.ConverterOptions('', '')
            )
            
            print("Creating topics for split bag...")
            for topic_info in metadata.topics_with_message_count:
                writer.create_topic(topic_info.topic_metadata)
        
        if topic == '/tf_static':
            print("found tf static")
            print(topic)
            # Save tf_static messages to replay in every split bag
            tf_static_msgs_data.append(data)
            tf_static_timestamps_delta.append(timestamp - split_start_time)
            print(tf_static_timestamps_delta)

        if split_index > 0:
            delta_timestamp = timestamp - split_start_time
            # Check if delta_timestamp is close to any stored tf_static_timestamps_delta (within 1ms)
            for idx, ts in enumerate(tf_static_timestamps_delta):  # 1e6 ns = 1 ms
                delta_diff = abs(delta_timestamp - ts)
                if delta_diff < 1e6:
                    print(delta_diff)
                    print("add tf static")
                    # Write the corresponding tf_static message to the current split bag
                    tf_static_data = tf_static_msgs_data[idx]
                    writer.write("/tf_static", tf_static_data, timestamp)


        # Write message to the current split bag
        writer.write(topic, data, timestamp)

        # Check if the split duration is exceeded
        if timestamp >= split_end_time:
            writer.close()
            split_index += 1
            split_start_time = None  # Reset for the next split

    # Close the last writer
    writer.close()
    print(f"Splitting completed. Bags saved in {output_dir}")

# Example usage
if __name__ == "__main__":
    input_bag = "rosbag/rosbag2_2025_07_31-16_24_13"
    output_directory = "rosbag/short_rosbags"
    split_duration = 40  # seconds
    split_rosbag(input_bag, output_directory, split_duration)
