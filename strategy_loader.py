# strategy_loader.py
import os
import json

def load_strategy_info(pattern_name):
    filename = os.path.join('strategy', f'{pattern_name}.json')
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
