import time

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

driver = Chrome(options=options)
wait = WebDriverWait(driver, 10)
url = "https://us.shein.com/Men-Playing-Card-Print-Tee-p-9847947-cat-1980.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_16%60ps%3D4_10%60jc%3DitemPicking_001121429&src_module=Women&src_tab_page_id=page_home1685728955945&mallCode=1"
driver.get(url)

# wait to close the coupon-box
coupon_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.c-coupon-box')))
coupon_box.find_element(By.CSS_SELECTOR, 'i.iconfont.icon-close.she-close').click()

# # wait to minimize the register-container side box
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.quickg-outside')))
driver.execute_script("document.querySelector('i.svgicon.svgicon-arrow-left').click();")

for color in driver.find_elements(By.CSS_SELECTOR, "div[class^='product-intro__color-radio']"):

    driver.execute_script("arguments[0].click();", color)
    time.sleep(2)
    name = color.get_attribute("aria-label")
    colorPic = color.find_element(By.TAG_NAME, "img").get_attribute("src")
    price = driver.find_element(By.CLASS_NAME, "from").get_attribute("aria-label")

    pictures = []
    for pic in driver.find_element(By.CLASS_NAME, "product-intro__thumbs-inner").find_elements(By.TAG_NAME, "img"):
        pictures.append(pic.get_attribute("src"))

    print(f"color name: {name}, color link: {colorPic}, price: {price}, pictures: {pictures}")