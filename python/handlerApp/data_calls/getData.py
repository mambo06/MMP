from collections import deque, defaultdict
from typing import Any, Dict, List, Set, Tuple, Optional
import json
import os
import sys

def find_node_by_name( name: str) -> Dict[str, Any]:
    """Return the first node whose 'name' matches."""

    # Construct the file path
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = '/'.join(file_path.split(os.sep)[:-2])

    file_path += '/data/diagram.json'
    # file_path = '../data/diagram.json'
    # print(os.getcwd())

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        real_path = os.path.abspath(file_path)
        raise FileNotFoundError(f"The file at {real_path} was not found. ")
    except IsADirectoryError:
        real_path = os.path.abspath(file_path)
        raise IsADirectoryError(f"The path {real_path} is a directory, not a file.")
    except Exception as e:
        real_path = os.path.abspath(file_path)
        raise Exception(f"An error occurred while trying to read the file at {real_path}: {e}")

    graph = json.loads(content)

    for n in graph.get("nodes", []):
        if n.get("name") == name:
            return n
    # raise KeyError(f"No node with name={name!r}")

if __name__ == "__main__":
    # with open(file_path if isinstance(file_path, str) else input_identifier, 'r', encoding='utf-8') as file:
    #             content = file.read()
    find_node_by_name('sample_data')