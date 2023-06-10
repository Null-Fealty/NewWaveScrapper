import functions as load
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
# options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

driver = Chrome(options=options)

itemList = load.phase1(driver)

# for item in itemList:
#     load.phase2(itemList["link"])

load.phase2(driver, itemList[0]["link"])

