import os
import argparse
import json
def get_tokens(target_folder):
    tokenL = None
    tokenR = None
    for dirpath, _, filenames in os.walk(target_folder):
        for filename in filenames:
            if filename.endswith('.json') and filename == "sensor.json":
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = json.load(file)

                    for sensor in content:
                        if sensor['channel'] == "CAM_BACK_LEFT":
                            tokenL = sensor['token']
                        if sensor['channel'] == "CAM_BACK_RIGHT":
                            tokenR = sensor['token']

                    return tokenL, tokenR
                    
                except Exception as e:
                    print(f"  -> ❌ Error processing {file_path}: {e}")


def fix_json(target_folder, tokenL, tokenR):
    for dirpath, _, filenames in os.walk(target_folder):
        for filename in filenames:
            if filename.endswith('.json') and filename == "calibrated_sensor.json":
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = json.load(file)

                    cal_l, cal_r = None, None
                    indl, indr = -1, -1
                    for idx, calibration in enumerate(content):
                        if calibration['sensor_token'] == tokenL:
                            cal_l = calibration
                            indl = idx
                        if calibration['sensor_token'] == tokenR:
                            cal_r = calibration
                            indr = idx

                    cal_back = {
                        'sensor_token': cal_l['sensor_token'],
                        'token': cal_l['token']
                    }
                    cal_l['sensor_token'] = cal_r['sensor_token']
                    cal_l['token'] = cal_r['token']
                    cal_r['sensor_token'] = cal_back['sensor_token']
                    cal_r['token'] = cal_back['token']

                    content[indl] = cal_l
                    content[indr] = cal_r

                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(content, file, indent=4)


                    return
                    
                except Exception as e:
                    print(f"  -> ❌ Error processing {file_path}: {e}")

def swap_back_left_right(text):
    """
    Swaps 'BACK_LEFT' with 'BACK_RIGHT' and vice-versa in a string.

    This is a direct string replacement. It uses a temporary placeholder
    to ensure a correct swap in a single pass.

    Args:
        text (str): The input string (e.g., a filename).

    Returns:
        str: The processed string with names swapped.
    """
    # Using a unique placeholder is crucial to avoid incorrect swaps,
    # e.g., BACK_LEFT -> BACK_RIGHT, then BACK_RIGHT (the new one) -> BACK_LEFT.
    placeholder = "___TEMP_SWAP_PLACEHOLDER___"
    text = text.replace("BACK_LEFT", placeholder)
    text = text.replace("BACK_RIGHT", "BACK_LEFT")
    text = text.replace(placeholder, "BACK_RIGHT")
    return text

def swap_text(text,old,new):
    """
    Swaps 'BACK_LEFT' with 'BACK_RIGHT' and vice-versa in a string.

    This is a direct string replacement. It uses a temporary placeholder
    to ensure a correct swap in a single pass.

    Args:
        text (str): The input string (e.g., a filename).

    Returns:
        str: The processed string with names swapped.
    """
    # Using a unique placeholder is crucial to avoid incorrect swaps,
    # e.g., BACK_LEFT -> BACK_RIGHT, then BACK_RIGHT (the new one) -> BACK_LEFT.
    text = text.replace(old, new)
    return text

def process_directory(root_path):
    """
    Walks through a directory to swap 'BACK_LEFT' and 'BACK_RIGHT' in
    file and directory names.

    The renaming process is done bottom-up to avoid path issues where a parent
    directory is renamed before its children are processed.

    Args:
        root_path (str): The absolute or relative path to the target directory.
    """
    if not os.path.isdir(root_path):
        print(f"Error: The provided path '{root_path}' is not a valid directory.")
        return

    # --- Rename files and directories (bottom-up) ---
    print("--- Starting: Renaming files and directories ---")
    # A bottom-up walk is crucial. It renames items in subdirectories before
    # renaming the parent directories themselves, preventing path conflicts.
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Rename files first
        for filename in filenames:
            new_filename = swap_back_left_right(filename)
            if new_filename != filename:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f"🔄 Renamed file:      {old_path} -> {new_path}")
                except OSError as e:
                    print(f"❌ Could not rename file {old_path}: {e}")

        # Then rename directories
        for dirname in dirnames:
            new_dirname = swap_text(dirname,"BACK_LEFT","___TEMP_SWAP_PLACEHOLDER___LEFT")
            if new_dirname != dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f"🔄 Renamed directory: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"❌ Could not rename directory {old_path}: {e}")
            new_dirname = swap_text(dirname,"BACK_RIGHT","___TEMP_SWAP_PLACEHOLDER___RIGHT")
            if new_dirname != dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f"🔄 Renamed directory: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"❌ Could not rename directory {old_path}: {e}")
    
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        for dirname in dirnames:
            new_dirname = swap_text(dirname,"___TEMP_SWAP_PLACEHOLDER___LEFT","BACK_RIGHT")
            if new_dirname != dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f"🔄 Renamed directory: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"❌ Could not rename directory {old_path}: {e}")
            new_dirname = swap_text(dirname,"___TEMP_SWAP_PLACEHOLDER___RIGHT","BACK_LEFT")
            if new_dirname != dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f"🔄 Renamed directory: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"❌ Could not rename directory {old_path}: {e}")
    print("--- Finished Renaming ---")

    print("Swaping BACK_LEFT and BACK_RIGHT completed in json files content")
    target_folder = root_path 

    # The strings to swap
    string1 = 'BACK_RIGHT'
    string2 = 'BACK_LEFT'

    # A temporary placeholder that is unlikely to exist in your files
    placeholder = '%%PLACEHOLDER_SWAP%%'

    # --- Script Logic ---
    print(f"🚀 Starting swap in folder: {os.path.abspath(target_folder)}")

    # os.walk will go through the target_folder and all its subfolders
    for dirpath, _, filenames in os.walk(target_folder):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    # Read the original file content
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                    # Check if a swap is even needed
                    if string1 in content or string2 in content:
                        print(f"  -> Processing: {file_path}")
                        
                        # Perform the swap using the placeholder
                        content_swapped = content.replace(string1, placeholder)
                        content_swapped = content_swapped.replace(string2, string1)
                        content_swapped = content_swapped.replace(placeholder, string2)
                        
                        # Write the modified content back to the file
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(content_swapped)
                    
                except Exception as e:
                    print(f"  -> ❌ Error processing {file_path}: {e}")

    print("✅ Swap complete!")
    print("--- Starting: Reverting tokens ---")
    tokenL, tokenR = get_tokens(target_folder)
    fix_json(target_folder, tokenL, tokenR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively swap 'BACK_LEFT' and 'BACK_RIGHT' in filenames and directory names.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "folder_path",
        help="The path to the folder you want to process."
    )
    args = parser.parse_args()

    target_folder = args.folder_path
    
    print(f"\nTarget folder: {os.path.abspath(target_folder)}\n")
    process_directory(target_folder)
    print("\nScript finished successfully.")

