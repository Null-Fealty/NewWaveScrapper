from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import selenium.webdriver.support.expected_conditions as EC

from googletrans import Translator

from random import randint, choice

import math
import json
import time

def divide():
    print((("###############" * 4 ) + "\n") * 3)

def notify(message):
    print("-" * 20, "\n" + message+ "\n", "-"*20 + "\n")

def closeCoupons(driver):
    wait = WebDriverWait(driver, 10)

    try:
        coupon_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//i[@class='iconfont icon-close she-close']")))
        coupon_box.find_element(By.XPATH, "//i[@class='iconfont icon-close she-close']").click()
    except:
        print("N/A")

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.quickg-outside')))
        driver.execute_script("document.querySelector('i.svgicon.svgicon-arrow-left').click();")
    except:
        print("N/A")

    finally:
        notify("popups closed")

def load(driver, link):
    driver.get(link)
    driver.implicitly_wait(120)

##might be useless now
def categories(driver):
    extensions = []
    load(driver, "https://www.shein.com")
    closeCoupons(driver)
    notify("Loading Categories")

    for category in driver.find_element(By.CLASS_NAME, 'home-index__ccc-content').find_elements(By.XPATH, "//a[@class='j-hotZone block']"):
        if ("Return" not in category.get_attribute('href')) and "Shipping" not in category.get_attribute('href') and "user" not in category.get_attribute('href'):
            extensions.append(category.get_attribute('href'))

    return extensions

def login_Chrome(driver, gmailId, passWord):
    link = "https://accounts.google.com/v3/signin/identifier?dsh=S1527745019%3A1685916348871989&continue=https%3A%2F%2Fwww.google.com%3Fhl%3Den-US&ec=GAlA8wE&hl=en&flowName=GlifWebSignIn&flowEntry=AddSession"
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

def prettyRoundCheap(price):
    if price < 1:
        price = math.ceil(price * randint(4, 7)) + .99

    elif price < 3:
        price = math.ceil(price * 4) + .99

    elif price <= 5:
        price = math.ceil(price * 3) + .99

    elif price <= 10:
        price = math.ceil(price * 2) + .99

    return price

def login_shoppify(driver, user, password, name, price, SKU, weight):
    print('in login')
    try:
        translator = Translator()
        load(driver, ("https://7318a2.myshopify.com/admin/products/new"))

        loginBox = driver.find_element(By.ID, 'account_email')
        loginBox.send_keys(user)

        nextButton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@name='commit']")))
        nextButton.click()

        nextButton = driver.find_element(By.ID, "identifierNext")
        nextButton.click()

        passWordBox = driver.find_element(By.XPATH, '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(password)

        nextButton = driver.find_element(By.XPATH, '//*[@id ="passwordNext"]')
        nextButton.click()

        title = driver.find_element(By.XPATH, '//input[@name="title"][@class="Polaris-TextField__Input_30ock"]')
        title.send_keys(name)

        driver.find_element(By.ID, "magic-popover-activator").click()
        generate_desc = driver.find_element(By.XPATH, '//textarea[@class="Polaris-TextField__Input_30ock"]')
        generate_desc.send_keys(name)

        driver.find_element(By.XPATH, '//option[@value="playful"]').click()
        driver.find_element(By.XPATH, "//button[@class='Polaris-Button_r99lw'][@aria-label='Generate text']").click()

        desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_TextOutput_r18hq_1"]')))
        desc = desc.find_element(By.TAG_NAME, "p").text
        driver.find_element(By.XPATH, "//button[@class='Polaris-Button_r99lw Polaris-Button--primary_7k9zs'][@aria-label='Keep']").click()

        # descBox = driver.find_element(By.ID, "richtexteditor_text_area-product-description")
        # descBox.send_keys(Keys.CONTROL + "a")
        # descBox.send_keys(translator.translate(desc, dest="es"))

        priceSellBox = driver.find_element(By.XPATH, '//input[@name="price"]')
        priceSellBox.send_keys(prettyRoundCheap(float(price.replace("$", ""))))

        if choice((True, False)):
            compareAt = driver.find_element(By.XPATH, '//input[@name="compareAtPrice"]')
            compareAt.send_keys(str(randint(math.ceil(float(price.replace("$", ""))) + 5, math.ceil(float(price.replace("$", ""))) + 10) + .99))

        # taxBox = driver.find_element(By.ID, ":r84:")
        # taxBox.click()

        priceCostBox = driver.find_element(By.XPATH, '//input[@name="unitCost"]')
        priceCostBox.send_keys(price)

        driver.find_element(By.XPATH, "//label[@class='Polaris-Choice_j5gzq'][@for='InventoryTrackingTracked']").click()

        for element in driver.find_elements(By.XPATH, '//span[@class="Polaris-Choice__Label_2vd36"]'):
            text = element.find_element(By.TAG_NAME, "span").text
            if "SKU" in text.split():
                element.click()
                break

        skuBox = driver.find_element(By.ID, "InventoryCardSku")
        skuBox.send_keys(SKU)

        weight = driver.find_element(By.XPATH, "//input[@name='weight'][@id='ShippingCardWeight']")
        weight.send_keys(Keys.CONTROL + Keys.BACKSPACE)
        weight.send_keys(str(weight))

        internationalBox = driver.find_element(By.XPATH, "//div[@class='Polaris-LegacyStack_eaeo0 Polaris-LegacyStack--vertical_uiuuj']").find_element(By.CLASS_NAME, "Polaris-Checkbox__Backdrop_1x2i2")
        internationalBox.click()

        for i in driver.find_element(By.XPATH, "//div[@class='Polaris-LegacyStack_eaeo0 Polaris-LegacyStack--vertical_uiuuj']").find_elements(By.TAG_NAME, "select"):
            if i.get_attribute("id") != "ShippingCardWeightUnit":
                internationalBoxOptions = Select(i)

        internationalBoxOptions.select_by_value("US")

        hsCode = driver.find_element(By.ID, "ShippingCardHarmonizedSystemCode-Prefix")
        hsCode.send_keys("6306.90") #clothing

        time.sleep(200)
        print("Login Success")

    except:
        print("Login Failure")

def variantLink(link, itemName, ID):
    try:
        itemName = itemName.replace("&", "").split()
        itemName = "-".join(itemName) + "-p-"
        linkOne = link[:link.find(itemName)] + itemName
        linkTwo = link[link.find(itemName) + len(itemName):][link[link.find(itemName) + len(itemName):].find("-"):]
        return linkOne + ID + linkTwo

    except:
        return link

def phase1(driver, category, catName):
    try:
        load(driver, category)
        closeCoupons(driver)
        notify("Currently in " + catName)

        itemList = []
        elements = driver.find_elements(By.XPATH, "//section[@class='S-product-item j-expose__product-item product-list__item']")
        count = 0

        for i in elements:
            if count == 1:
                break

            count += 1
            print(str(count) + "/" + str(len(elements)))

            if float(i.find_element(By.TAG_NAME, "a").get_attribute("data-price")) > 10:
                count == 0
                pass

            temp = {}
            dataIDS = []

            name = i.find_element(By.TAG_NAME, "a").get_attribute("aria-label")
            link = i.find_element(By.TAG_NAME, "a").get_attribute("href")

            for id in i.find_elements(By.TAG_NAME, "label"):
                if not(id.get_attribute("data-id") is None):
                    dataIDS.append(id.get_attribute("data-id"))

            temp["name"] = name
            temp["link"] = link
            temp["Data ID"] = dataIDS
            itemList.append(temp)

        return itemList

    except:
        print("reloading")
        return -1

    finally:
        load(driver, "https://www.google.com")

def phase2(driver, link):
    try:
        load(driver, link)
        item = {}
        sizes = {}
        pictures = []
        name = driver.find_element(By.XPATH, "//h1[@class='product-intro__head-name']").text

        try:
            SKU = driver.find_element(By.XPATH, "//div [@class='product-intro__head-sku']").text.replace(":", "").split()
        except:
            print("")

        try:
            colorName = driver.find_element(By.XPATH, "//div [@class='color-block']").get_attribute("aria-label").replace(":", "").split()
            colorPic = driver.find_element(By.XPATH, "//div [@class='product-intro__color-radio product-intro__color-radio_active']").find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            print("")

        price = driver.find_element(By.XPATH, "//div[@class='from']").get_attribute("aria-label")

        try:
            driver.find_element(By.XPATH, "//div[@class='product-intro__size-choose']")
            for i in driver.find_element(By.XPATH, "//div[@class='product-intro__size-choose']").find_elements(By.TAG_NAME, "span"):
                size, quantity = i.find_element(By.TAG_NAME, "div").get_attribute("aria-label").split()
                sizes[size] = quantity

        except:
            print()

        for pic in driver.find_element(By.CLASS_NAME, "product-intro__thumbs-inner").find_elements(By.TAG_NAME, "img"):
            pictures.append(pic.get_attribute("src"))

        item["name"] = name
        item[colorName[0]] = colorName[1]
        item[SKU[0]] = SKU[1]
        item["price"] = price
        item["pictures"] = pictures
        item["link"] = link

        try:
            item["sizes"] = sizes
        except:
            print()

        try:
            item["colorPic"] = colorPic
        except:
            print()

        return item

    except:
        print("reloading")
        load(driver, "https://www.google.com")
        phase2(driver, link)

    finally:
        load(driver, "https://www.google.com")

def main(driver, item, it, weight):
    # itemList = phase1(driver, item, it)
    #
    # itemD = {}
    # count = 0
    #
    # while itemList == -1:
    #     itemList = phase1(driver, item, it)
    #
    # divide()
    #
    #
    # for i in itemList:
    #     itemD = []
    #     notify("Currently Getting Details for: " + i["name"])
    #
    #     itemD.append(phase2(driver,i["link"]))
    #
    #     #finds all variants
    #     # if len(i["Data ID"]) > 0:
    #     #     for id in i["Data ID"]:
    #     #         itemD[i["name"]].append(phase2(driver, variantLink(i["link"],i["name"],id)))
    #     # else:
    #     #     itemD[i["name"]].append(phase2(driver,i["link"]))
    #
    #     divide()
    #     count += 1
    #     notify(str(count) + "/" + str(len(itemList)))
    itemD = [{'name': 'Eyelet Embroidery Batwing Sleeve Tee', 'Color': 'Redwood', 'SKU': 'sw2302089539602212', 'price': '$4.76', 'pictures': ['https://img.ltwebstatic.com/images3_pi/2023/02/15/1676453841d5ddb07116e314c790dcf7c0be5c1b52_thumbnail_220x293_thumbnail_80x.webp', 'https://img.ltwebstatic.com/images3_pi/2023/02/15/1676453844ee76b304267b2042f0022a2483d1e54d_thumbnail_220x293_thumbnail_80x.webp', 'https://img.ltwebstatic.com/images3_pi/2023/02/15/1676453849144bea239c5a90f329ef60d2cc8c7dcd_thumbnail_220x293_thumbnail_80x.webp', 'https://img.ltwebstatic.com/images3_pi/2023/02/15/167645385257762b5bf58a448c9e683ccb8936602f_thumbnail_220x293_thumbnail_80x.webp', 'https://img.ltwebstatic.com/images3_pi/2023/02/15/1676453854a8d8eb44f83b7a6882d59e2fdc526150_thumbnail_220x293_thumbnail_80x.webp', 'https://img.ltwebstatic.com/images3_pi/2023/02/15/167645385257762b5bf58a448c9e683ccb8936602f_thumbnail_80x.webp'], 'link': 'https://us.shein.com/Eyelet-Embroidery-Batwing-Sleeve-Tee-p-13138402-cat-1738.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_18%60ps%3D4_11%60jc%3Dreal_2030&src_module=Women&src_tab_page_id=page_home1687798867022&mallCode=1', 'sizes': {'4': '(S)', '6': '(M)', '8/10': '(L)', '12': '(XL)'}, 'colorPic': '//img.ltwebstatic.com/images3_pi/2023/02/15/16764538589dd366e6a56b397411ff87d1e8621339.webp'}]
    print(itemD)
    for item in itemD:
        login_shoppify(driver, "thenewwaveaesthetic@gmail.com", "Stormthec@stl3", item["name"].replace("SHEIN", "New Wave"), item["price"], item["SKU"], weight)
    return

    divide()

    time.sleep(1000)