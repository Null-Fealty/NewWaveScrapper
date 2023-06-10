from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time
import json

def load(driver, link):
    driver.get(link)
    driver.implicitly_wait(15)

def login(driver):
    link = "https://accounts.google.com/v3/signin/identifier?dsh=S1527745019%3A1685916348871989&continue=https%3A%2F%2Fwww.google.com%3Fhl%3Den-US&ec=GAlA8wE&hl=en&flowName=GlifWebSignIn&flowEntry=AddSession"
    gmailId = "thenewwaveaesthetic@gmail.com"
    passWord = "Stormthec@stl3"

    try:
        load(driver, link)

        loginBox = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
        loginBox.send_keys(gmailId)

        nextButton = driver.find_element(By.ID, "identifierNext")
        nextButton.click()


        passWordBox = driver.find_element(By.XPATH, '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(passWord)

        nextButton = driver.find_element(By.XPATH, '//*[@id ="passwordNext"]')
        nextButton.click()

        print('Login Successful...!!')
    except:
        print('Login Failed')

def closeCoupons(driver):
    wait = WebDriverWait(driver, 10)

    try:
        coupon_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.c-coupon-box')))
        coupon_box.find_element(By.CSS_SELECTOR, 'i.iconfont.icon-close.she-close').click()
    except:
        print("not found")

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.quickg-outside')))
        driver.execute_script("document.querySelector('i.svgicon.svgicon-arrow-left').click();")
    except:
        print("you good G")

def variantLink(link, itemName, ID):
    itemName = itemName.replace("&", "").split()
    itemName = "-".join(itemName) + "-p-"
    linkOne = link[:link.find(itemName)]
    linkTwo = link[link.find(itemName) + len(itemName):][link[link.find(itemName) + len(itemName):].find("-"):]
    return linkOne + ID + linkTwo

def phase1(driver):
    driver.get("https://us.shein.com/style/Men-Clothing-sc-001121429.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_16%60ps%3D4_10%60jc%3DitemPicking_001121429&src_tab_page_id=page_home1685728955945&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D4814191_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-10_ABT%3DSPcCccWomenHomepage_expgroup_100004156")
    closeCoupons(driver)

    itemList = []
    for i in driver.find_elements(By.CLASS_NAME, "S-product-item__info"):
        temp = {}
        name = i.find_element(By.TAG_NAME, "a").get_attribute("aria-label")
        link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
        dataIDS = []
        for id in i.find_element(By.XPATH, '//section[@role="radiogroup"]').find_elements(By.TAG_NAME, "label"):
            dataIDS.append(id.get_attribute("data-id"))

        temp["name"] = name
        temp["link"] = link
        temp["Data ID"] = dataIDS
        itemList.append(temp)

    with(open("info.txt", "w")) as f:
        f.write(json.dumps(itemList, indent=4))

    driver.close()
    return itemList

def phase2(driver, link):
    load(driver, link)
    closeCoupons(driver)
    item = {}

    SKU = driver.find_element(By.XPATH, "//div [@class='product-intro__head-sku']").text
    colorName = driver.find_element(By.XPATH, "//div[@class='color-block'").get_attribute("aria-label")
    colorPic = driver.find_element(By.XPATH, "//div [@class='product-intro__color-radio product-intro__color-radio_active'").find_element(By.TAG_NAME, "img").get_attribute("src")
    price = driver.find_element(By.XPATH, "//div[@class='from'").get_attribute("aria-label")

    sizes = {}
    pictures = []
    description = {}
    item["SKU"] = SKU
    item["color name"] = colorName
    item["colorPic"] = colorPic
    item["price"] = price
    item["sizes"] = sizes
    item["pictures"]





for i in driver.find_element(By.XPATH, "//div[@class='product-intro__size-choose'").find_elements(By.TAG_NAME, "span"):
        size, quantity = i.get_attribute("aria-label").split()
        sizes[size] = quantity

    driver.find_element(By.XPATH, "//h2 [@class = 'product-intro__description-head']").click()

    for i in driver.find_elements(By.XPATH, "//div[@class='product-intro__description-table'").find_elements(By.XPATH, "//div[@class='product-intro__description-table-item'"):
        description[i.find_element(By.XPATH, "//div[@class='key'").text] = i.find_element(By.XPATH, "//div[@class='val'").text

    for pic in driver.find_element(By.CLASS_NAME, "product-intro__thumbs-inner").find_elements(By.TAG_NAME, "img"):
        pictures.append(pic.get_attribute("src"))

    with(open("indepth.txt", "w")) as f:
        f.write(json.dumps(item, indent=4))









