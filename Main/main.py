import functions as load
from selenium.webdriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
import json

options = ChromeOptions()
# options.add_argument("--start-minimized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")

options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = uc.Chrome(options=uc.ChromeOptions())
driver.set_page_load_timeout(30)


## part 1
categories = load.categories(driver)

print(categories)

it = 0
for item in categories:
        load.main(driver, item, it)
        it += 1
        load.notify(str(it) + " out of " + str(len(categories)))


### part 2
with open("8.txt", "r") as jsonFile:
    data = json.loads(jsonFile)
    print(data)

# load.mainTwo(driver)

