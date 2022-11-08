import requests
from bs4 import BeautifulSoup as bs
from setup import bs, Edge, EdgeOptions, EdgeService, EdgeDriverManager
import setup, time, bs4
from setup import save_file as save_local

# Python fix not logged in
driver = None
page_objects = []

TEST_NUMBER = 0
visited_urls = []

def check_disabled(tag_object: bs4.Tag):
  """Check if a tag has a class name 'disabled' """

  if(not isinstance(tag_object, bs4.Tag)):
    print(tag_object, "TYPE: ", type(tag_object))
    raise ValueError("check_disabled(): invalid tage object")

  class_names = tag_object.get_attribute_list("class")
  return "disabled" in class_names


def retrieve(url):
  global driver
  # initial run

  if not driver:
    edge_driver_manager = EdgeDriverManager(path="./drivers").install()
    service = EdgeService(edge_driver_manager)
    options = EdgeOptions()

    driver = Edge(service=service, options=options)

    driver.get(url)
    cookies = setup.get_cookies("cookies/www.cloudskillsboost.google_07-11-2022.json")
    
    # Before this step will work clean up the json data as followes:
    # "sameSite": "unspecified" => "sameSite": "None"
    # "sameSite": "lax" => "sameSite": "Lax"
    # TODO: Fix the above problem in the during transform
    setup.add_cookies(setup.transform_cookies(cookies), driver)
    driver.refresh()

  else:
    driver.get(url)

  page = bs(driver.page_source, "html.parser")
  save_local(setup.name_local_file("cloudskillsbooks.html"), page.text)
  
  return page


def initiate():
  global TEST_NUMBER
  url = find_next()

  if TEST_NUMBER > 5:
    return
  else:
    print("TEST_NUMBER: ", TEST_NUMBER)
    TEST_NUMBER += 1

  if not url:
    save_csv()
    return
  page = retrieve(url=url)
  page_objects.append(page)
  visited_urls.append(url)

  time.sleep(2)
  initiate()



"""
import requests
from bs4 import BeautifulSoup as bs
from setup import load_file as load, cls
pg = bs(load("files/cloudskillboost.html"), "html.parser")
"""

def find_next():
  # Furst run
  if not visited_urls and not page_objects:
    return "https://www.cloudskillsboost.google/profile/activity"

  # subsequent runs
  if not page_objects:
    raise Exception("Invalid run")
  
  last_visited = page_objects[len(page_objects) - 1]

  if not isinstance(last_visited, bs4.Tag):
    raise ValueError("find_next(): Invalid page object")
  
  prev_anchor = last_visited.select_one("nav.pagination .previous_page")
  next_anchor = last_visited.select_one("nav.pagination .next_page")

  is_disabled_prev = check_disabled(prev_anchor)
  is_disabled_next = check_disabled(next_anchor)

  if is_disabled_prev:
    anchor = next_anchor.get("href")
    return "https://www.cloudskillsboost.google{}".format(anchor if anchor else "")

  if is_disabled_next:
    return

  #02 Essential Google Cloud Infrastructure- Foundation\4. Virtual Machines
  # video 10


def collect(soup: bs):
  """Collect desired information from a page object"""
  pass


def sort_fn():
  """provide custom sorting of the data"""
  pass


def save_csv():
  """convert data to csv and save"""
  sort_fn()
