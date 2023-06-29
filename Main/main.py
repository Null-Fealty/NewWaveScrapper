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
driver.set_page_load_timeout(120)


## part 1
link = "https://us.shein.com/Women-Clothing-c-2030.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_18%60ps%3D4_11%60jc%3Dreal_2030&src_tab_page_id=page_home1687798867022&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D5589385_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-11_ABT%3D0"
# input("What are we scrapping today sire?(link)\n>>> ")
name = "Ladies"
# input("And what shall we name that sire?(name)\n>>> ")
weight = "0.44"
# input("What's the weight, sire?(LBS)")
load.main(driver, link, name, float(weight))



