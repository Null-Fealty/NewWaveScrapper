import functions as load
from selenium.webdriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
import json

options = uc.ChromeOptions()
options.add_argument("--start-Maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = uc.Chrome(options=uc.ChromeOptions())
driver.set_page_load_timeout(120)


## part 1
link = "https://us.shein.com/Women-Tops,-Blouses-Tee-c-1766.html?ici=us_tab01navbar07&src_module=topcat&src_tab_page_id=page_home1688049567200&src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&srctype=category&userpath=category-TOPS"
# input("What are we scrapping today sire?(link)\n>>> ")
name = "Tops and Blouses"
# input("And what shall we name that sire?(name)\n>>> ")
weight = "0.44"
# input("What's the weight, sire?(LBS)")
load.main(driver, link, name, float(weight))



