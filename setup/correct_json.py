"""
This script cleans up the josn file fed to the scrapper

It corrects some invalid values causing the scrapper to fail

Bellow are the details of the correction

sameSite: unspecified -> sameSite: None
sameSite: lax -> sameSite: Lax
 """


import json
from typing import Dict, List, Union
from pprint import pprint as pp

JSON_FILE_PATH = "../cookies/www.cloudskillsboost.google_07-11-2022.json"
JSON_FILE: str

with open(JSON_FILE_PATH, "r") as f:
  JSON_FILE = f.read()

objects: List[Dict[str, str]] = json.loads(JSON_FILE)
JSON_FILE = None

for c in objects["cookies"]:
  for prop, value in c.items():
    if(prop.lower() == "samesite" and value.lower() == "unspecified"):
      c[prop] = "None"
    
    if(prop.lower() == "samesite" and value.lower() == "lax"):
      c[prop] = "Lax"

with open(JSON_FILE_PATH, "w") as f:
  f.write(json.dumps(objects))

pp(objects)
objects = None