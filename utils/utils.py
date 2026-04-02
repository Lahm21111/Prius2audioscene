import json
import os
import secrets
from typing import Dict, List

import rclpy.time
from builtin_interfaces.msg import Time


def generate_token() -> str:
    return secrets.token_hex(16)


def create_dir(path: str | os.PathLike) -> None:
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)



def get_unix_time(stamp) -> float:
    sec = stamp.sec
    nsec = stamp.nanosec
    unix_timestamp = sec + (nsec / 1_000_000_000)
    return round(unix_timestamp, 6)




def read_json(path: os.PathLike) -> List | Dict:
    with open(path, "r+") as file:
        return json.load(file)


def get_file_timestamp(filename: str) -> rclpy.time.Time:
    timestamp = int(filename.split("__")[-1].split(".")[0])
    seconds = timestamp // 1e9
    nanoseconds = timestamp % 1e9
    ros_time = rclpy.time.Time(
        seconds=int(seconds),
        nanoseconds=int((nanoseconds % 1) * 1e9),
    )

    return ros_time
def get_token_if_column_contains_string(dataframe, column, string):
        """
        Get the token of the entry whose filename corresponds to an input.

        Args:
            filename (str): The filename to search for.

        Returns:
            str: The token of the entry if found, otherwise None.
        """
        token = dataframe.loc[dataframe[column].str.contains(string), 'token']
        return token.values[0] if not token.empty else None

def get_token_if_column_is_string(dataframe,column,string):
    """
    Get the token of the row whose name is equal to the input category name.

    Args:
        category_name (str): The category name to search for.

    Returns:
        str: The token of the row if found, otherwise None.
    """
    token = dataframe.loc[dataframe[column] == string, 'token']
    return token.values[0] if not token.empty else None

def get_column_if_token(dataframe,column,token):
    """
    Get the sample_token of the row whose token is equal to the input token.

    Args:
        token (str): The token to search for.

    Returns:
        str: The sample_token of the row if found, otherwise None.
    """
    column_value = dataframe.loc[dataframe['token'] == token, column]
    return column_value.values[0] if column_value.values else None

def write_json(filepath,data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
