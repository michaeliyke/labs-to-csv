# Load the files into a python list

import csv
import json
import bs4
import time
from bs4 import BeautifulSoup as bs
from typing import List, Dict, Union
from pathlib import Path

PAGES: List[bs4.element.Tag] = []
DOWNLOAD_PATH = Path("files")
CSV_HEADERS = ["Activity", "Type", "Started", "Ended", "Score", "Passed"]


# Load files to memory
for f_path in DOWNLOAD_PATH.iterdir():
  if f_path.suffix != ".html":
    continue

  time.sleep(0.5)

  with open(f_path.resolve(), "r", encoding="UTF-8") as _file:
    PAGES.append(bs(_file.read(), "html.parser"))
    print(f_path.name, "has been loaded!")
print("ALL FILES LOADED!")

# Prepare the data for storage
csv_f = "files/cloudskillsbooks.csv"
json_f = "files/cloudskillsbooks.json"

with open(csv_f, "w+", newline="") as file, open(json_f, "w+") as file2:
  writer = csv.writer(file)
  writer.writerow(CSV_HEADERS)

  page: bs4.BeautifulSoup
  row: Dict[str, Union[str, float, int, bool]]
  rows: List[Dict]

  ROWS: List[Dict] = []
  for page in PAGES:
    # rows is an array of json data embedded within HTML
    table_data = page.select_one("ql-table")
    rows = json.loads(table_data.get("data"))

    for row in rows:
      if("name" in row):
        row["activity"] = row["name"]
        del row["name"]

      if("score" in row):
        row["score"] = float(row["score"].split("/")[0])

      writer.writerow(list(row.values()))
      ROWS.append(row)

  file2.write(json.dumps(ROWS))

  print("csv file saved: files/cloudskillsbooks.csv")
