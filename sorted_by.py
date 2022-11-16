import json
from pathlib import Path
import sys
from typing import Dict, List
from personal import load_file, write_csv, md, write_json

# LOAD THE JSON FILE
JSON_FILE = "files/cloudskillsbooks.json"
CSV_FILE = "files/cloudskillsbooks.csv"
ROWS: List[Dict] = json.loads(load_file(JSON_FILE))

ARGS = sys.argv[1:]
ARG2 = None
if(not ARGS):
  raise ValueError("Data attribute e.g 'score' required to sort with")

criterion: str = ARGS[0]
if(criterion.lower() not in ROWS[0]):
  raise ValueError(f"{criterion} is not a know attribute")

# FACTOR SORTING DIRECTION
SORT_DESCENDING = True

if(len(ARGS) > 1):
  SORT_DESCENDING = None
  ARG2 = ARGS[1].lower()

  if(ARG2 == "desc" or ARG2 == "descending"):
    SORT_DESCENDING = True

  if(ARG2 == "asc" or ARG2 == "ascending"):
    SORT_DESCENDING = False

  if (SORT_DESCENDING == None):
    raise ValueError("Invalid sort direction: 'ASC' or 'DESC' expected")


def sort_by(row: Dict):
  return row[criterion]


ROWS.sort(key=sort_by, reverse=SORT_DESCENDING)

# Does data already exists?
criterion_dir = Path(criterion)
if(criterion_dir.exists()):
  contents = list(criterion_dir.iterdir())
  # if(len(contents) > 0):
  #   raise FileExistsError(f"{criterion} data already exists")
else:
  md(criterion)

new_json = JSON_FILE.replace("files", criterion)
new_csv = CSV_FILE.replace("files", criterion)

if(ARG2):
  new_json = new_json.replace(".json", f"-{ARG2}.json")
  new_csv = new_csv.replace(".csv", f"-{ARG2}.csv")

write_json(ROWS, new_json)
write_csv(ROWS, new_csv)

print("ALL DONE!")
