# strategy_loader.py
import os
import json

def load_strategy_info(self, pattern_name):
    """Instance method to load strategy information from JSON files."""
    filename = os.path.join("strategy", f"{pattern_name}.json")
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
