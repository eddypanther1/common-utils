#manually evaluate data returned from the API
#0. validate and clean up with jsonlint as needed
#1.  paste data from the API after da = 
#or afte json_string = """
#2. run the script interactively 
#$  cd llama && python -i data_eval.py
# will load this file
#3. if in json format, use json.loads(data) to convert to dict
# walk through the dict by d.da['x'] or d.j['x']
#4. or dget(j, '/messages/0/content/0/text')

import re
import json
import difflib
import dpath 

def dget(d, path):
    """Get value from dict using dpath."""
    try:
        text=dpath.get(d, path)
        print(f"'{path}': {text}")
        return dpath.get(d, path)
    except KeyError:
        return None

# not reliable; so use jsonlint or similar to validate JSON first
def clean_json_string(json_string):

    original = json_string

    # Remove comments (// or # at line start)
    json_string = re.sub(r'^\s*//.*$', '', json_string, flags=re.MULTILINE)
    json_string = re.sub(r'^\s*#.*$', '', json_string, flags=re.MULTILINE)
    # Remove trailing commas before } or ]
    json_string = re.sub(r',(\s*[}\]])', r'\1', json_string)
    # Replace single quotes with double quotes (be careful: this is naive)
    json_string = json_string.replace("'", '"')
    # Remove f-string expressions and Python variables (replace with dummy values)
    json_string = re.sub(r'\$?\{[^\}]+\}', '""', json_string)  # Remove ${...} or {...}
    json_string = re.sub(r'\b(model|content_text|base64_image)\b', '""', json_string)

    # Log the diff
    print("=== clean_json_string diff (before -> after) ===")
    for line in difflib.unified_diff(
        original.splitlines(), json_string.splitlines(),
        fromfile='before', tofile='after', lineterm=''
    ):
        print(line)
    print("=== end diff ===")
    return json_string


json_string= """
{
    "model": "model",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "content_text"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
}
"""

# Example usage:
# cleaned = clean_json_string(json_string)

# Convert the JSON string to a Python dictionary
try:
    j = json.loads(json_string)
except Exception as e:
    print(f"Error parsing JSON: {e}")
    j = None    



da = {
    'coord': {'lon': 136.7327, 'lat': 35.3967},
    'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
    'base': 'stations',
    'main': { # This is where 'temp' is
        'temp': 296.25,
        'feels_like': 296.03,
        'temp_min': 296.25,
        'temp_max': 296.25,
        'pressure': 1011,
        'humidity': 54,
        'sea_level': 1011,
        'grnd_level': 1005
    },
    'visibility': 10000,
    'wind': {'speed': 5.67, 'deg': 185, 'gust': 5.81},
    'clouds': {'all': 100},
    'dt': 1747984829,
    'sys': { # This is where 'country' is
        'type': 2,
        'id': 2035277,
        'country': 'JP',
        'sunrise': 1747943019,
        'sunset': 1747994174
    },
    'timezone': 32400,
    'id': 1862197,
    'name': 'Honjōchō', # This is where 'name' (the city name) is
    'cod': 200
}


    
# text = dget(j, '/messages/0/content/0/text')
# print(text)