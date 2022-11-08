from setup import options, service, edge_driver_manager, webdriver, Edge
import setup, time

def show_facebook():
    driver = Edge(service=service, options=options)
    driver.get("https://www.facebook.com")
    
    cookies = setup.get_cookies("cookies/www.facebook.com_06-11-2022.json")
    setup.add_cookies(setup.transform_cookies(cookies), driver)

    driver.refresh()
    time.sleep(10)
    
    driver.quit()


def show_cloudskillsboost():
  # options.headless = True
  driver = Edge(service=service, options=options)
  page = driver.get("https://www.cloudskillsboost.google/profile/activity")

  cookies = setup.get_cookies("cookies/www.cloudskillsboost.google_07-11-2022.json")

  # Before this step will work clean up the json data as followes:
  # "sameSite": "unspecified" => "sameSite": "None"
  # "sameSite": "lax" => "sameSite": "Lax"
  # TODO: Fix the above problem in the during transform
  setup.add_cookies(setup.transform_cookies(cookies), driver)

  driver.refresh()
  # driver.quit()
  return page
