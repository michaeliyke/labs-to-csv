import requests, bs4
from bs4 import BeautifulSoup as bs
from setup import bs, Edge, EdgeOptions, EdgeService, EdgeDriverManager
import setup, time, bs4
from setup import save_file as save_local
from typing import List, Dict, Union
# Mytype = Dict[str, Union[str, List[str]]] -> {"name": "iyke", "names": ["Iyke", "Michael, Chukwuma"]}

# Python fix not logged in
driver = None
HEADLESS: bool = False # Change to True to make the browser non-headless
soup_objects: List[bs4.PageElement] = []

TEST_NUMBER: int = 0
visited_urls: List[str] = []

def check_disabled(tag_object: bs4.Tag):
  """Check if a tag has a class name 'disabled' """

  if(not isinstance(tag_object, bs4.Tag)):
    print(tag_object, "TYPE: ", type(tag_object))
    raise ValueError("check_disabled(): invalid tage object")

  class_names = tag_object.get_attribute_list("class")
  return "disabled" in class_names


def retrieve(url: str):
  global driver
  # initial run

  if not driver:
    edge_driver_manager = EdgeDriverManager(path="./drivers").install()
    service = EdgeService(edge_driver_manager)
    options = EdgeOptions()

    driver = Edge(service=service, options=options)

    driver.get(url)
    cookies = setup.get_cookies("cookies/www.cloudskillsboost.google_07-11-2022.json")
    
    # If the correct_json script has not been run this step will fail
    setup.add_cookies(setup.transform_cookies(cookies), driver)

    time.sleep(2)
    driver.refresh()

  else:
    driver.get(url)

  return bs(driver.page_source, "html.parser")


def initiate():
  url = find_next()

  if not url:
    dispose()
    return
    
  soup = retrieve(url=url)
  soup_objects.append(soup)
  visited_urls.append(url)

  save_local(setup.name_local_file("cloudskillsbooks.html"), str(soup))
  time.sleep(2)
  initiate()


def find_next():
  # First run
  if not visited_urls and not soup_objects:
    print("First Run")
    return "https://www.cloudskillsboost.google/profile/activity"

  # subsequent runs
  if not soup_objects:
    raise Exception("Invalid run")
  
  last_visited = soup_objects[len(soup_objects) - 1]

  if not isinstance(last_visited, bs4.Tag):
    raise ValueError("find_next(): Invalid page object")
  
  next_anchor = last_visited.select_one("nav.pagination .next_page")
  is_disabled_next = check_disabled(next_anchor)

  if is_disabled_next:
    print("COMPLETED..")
    return ""
  
  anchor = next_anchor.get("href")
  return "https://www.cloudskillsboost.google{}".format(anchor if anchor else "")  

#02 Essential Google Cloud Infrastructure- Foundation\4. Virtual Machines
# video 10


def dispose():
  global driver
  driver.quit()

  driver = None
  global visited_urls

  visited_urls = []
  