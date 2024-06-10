import json
from pathlib import Path
from json import load
def readjson(filename):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        url = BASE_DIR / 'tests' / filename
        with open(url) as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("ERROR: ", e)