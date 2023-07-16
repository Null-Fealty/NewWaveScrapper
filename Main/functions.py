from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import selenium.webdriver.support.expected_conditions as EC

from googletrans import Translator

from random import randint, choice

import math
import os
import requests
import pyautogui
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
    price = float(price.replace("$", ""))
    if price < 1:
        price = math.ceil(price * randint(4, 7)) + .99

    elif price < 3:
        price = math.ceil(price * 4) + .99

    elif price <= 5:
        price = math.ceil(price * 3) + .99

    elif price <= 10:
        price = math.ceil(price * 2) + .99

    return price

def loadImages(driver, images):
    try:
        for image in images:
            filename = image.split('/')[-1].split('.')[0] + ".jpg"
            imgData = requests.get(image).content

            with open(filename, "wb") as f:
                f.write(imgData)

            filepath = os.path.abspath(filename)

            boxx = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='dn_ht']")))
            boxx.click()

            time.sleep(1)
            pyautogui.write(filepath)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)
            os.remove(filename)

    except Exception as e:
        print(e)

def login_shoppify(driver, user, password, name, price, SKU, weight, images):
    print('in login')
    try:
        load(driver, ("https://7318a2.myshopify.com/admin/products/new"))
        try:
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
        except:
            print("already logged in")

        title = driver.find_element(By.XPATH, '//input[@name="title"][@class="Polaris-TextField__Input_30ock"]')
        title.send_keys(name)

        try:
            driver.find_element(By.ID, "magic-popover-activator").click()
            generate_desc = driver.find_element(By.XPATH, '//textarea[@class="Polaris-TextField__Input_30ock"]')
            generate_desc.send_keys(name)

            driver.find_element(By.XPATH, '//option[@value="playful"]').click()
            driver.find_element(By.XPATH, "//button[@class='Polaris-Button_r99lw'][@aria-label='Generate text']").click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='Polaris-Button_r99lw Polaris-Button--primary_7k9zs'][@aria-label='Keep']"))).click()

        except Exception as e:
            print(e)

        priceSellBox = driver.find_element(By.XPATH, '//input[@name="price"]')
        priceSellBox.send_keys(prettyRoundCheap(price))

        if choice((True, False)):
            compareAt = driver.find_element(By.XPATH, '//input[@name="compareAtPrice"]')
            compareAt.send_keys(str(randint(math.ceil(float(price.replace("$", ""))) + 5, math.ceil(float(price.replace("$", ""))) + 10) + .99))

        priceCostBox = driver.find_element(By.XPATH, '//input[@name="unitCost"]')
        priceCostBox.send_keys(price)

        for element in driver.find_elements(By.XPATH, "//label[@class='Polaris-Choice_j5gzq Polaris-Checkbox__ChoiceLabel_16hp3']"):
            text = element.find_element(By.TAG_NAME, "span").text
            if "SKU" in text.split() or "Track quantity":
                if element.get_attribute("aria-checked") == "false":
                    element.click()

            if "Track quantity" in text.split():
                if element.get_attribute("aria-checked") == "true":
                    element.click()

        skuBox = driver.find_element(By.ID, "InventoryCardSku")
        skuBox.send_keys(SKU)

        weightBox = driver.find_element(By.XPATH, "//input[@name='weight'][@id='ShippingCardWeight']")
        weightBox.send_keys(Keys.CONTROL + Keys.BACKSPACE)
        weightBox.send_keys(str(weight))

        for i in driver.find_elements(By.XPATH, "//div[@class='Polaris-LegacyStack__Item_yiyol']//label[@class='Polaris-Choice_j5gzq']"):
            if "Include customs information for international shipping" in i.text:
                if i.find_element(By.TAG_NAME, "input").get_attribute("aria-checked") == "false":
                    i.click()

        for i in driver.find_element(By.XPATH, "//div[@class='Polaris-LegacyStack_eaeo0 Polaris-LegacyStack--vertical_uiuuj']").find_elements(By.TAG_NAME, "select"):
            if i.get_attribute("id") != "ShippingCardWeightUnit":
                internationalBoxOptions = Select(i)

        internationalBoxOptions.select_by_value("US")

        time.sleep(1)
        driver.find_element(By.XPATH, '//input[@name="title"][@class="Polaris-TextField__Input_30ock"]').send_keys("")

        loadImages(driver, images)

        print("Login Success")
    except:
        print("Login Failure")

def addVariant(driver, color, unitPrice, sellprice, first, SKU):
    for temp in driver.find_elements(By.XPATH, "//div[@class='AnU1b']"):
        try:
            currentPrice = float(driver.find_element(By.XPATH, '//input[@name="price"]').get_attribute("value"))
        except:
            currentPrice = 0
        if temp.find_element(By.TAG_NAME, "input").get_attribute("placeholder") == "Add another value" or first == True:# or temp.get_attribute("value") is None:
            newEntry = temp.find_element(By.TAG_NAME, "input")
            newEntry.send_keys(color)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
            if sellprice > currentPrice:
                driver.find_element(By.XPATH, '//input[@name="price"]').send_keys(sellprice)
                driver.find_element(By.XPATH, '//input[@name="unitCost"]').send_keys(unitPrice)


            # editButton = driver.find_element(By.XPATH, "//button[@aria-label='Edit variant " + color + "']")
            # editButton.click()
            #
            # for i in driver.find_elements(By.XPATH, "//button[@aria-label='Edit variant " + color + "']//input[@name='price']"):
            #     print(i.get_attribute("placeholder") == "0.00")
            #     if i.get_attribute("placeholder") == "0.00":
            #         i.send_keys(str(sellprice))
            #
            # for i in driver.find_elements(By.XPATH, "//button[@aria-label='Edit variant " + color + "']//input[@name='unitCost']"):
            #     if i.get_attribute("placeholder") == "0.00":
            #         i.send_keys(str(price))
            #
            # for i in driver.find_elements(By.XPATH, "//button[@aria-label='Edit variant " + color + "']//input[@name='sku']"):
            #     if i.get_attribute("value") is None:
            #         i.send_keys(str(SKU))
            # print("in")
            # done = driver.find_element(By.XPATH, "//div[@style='--pc-horizontal-stack-align: space-between; --pc-horizontal-stack-block-align: center; --pc-horizontal-stack-wrap: wrap; --pc-horizontal-stack-gap-xs: var(--p-space-4);']//button[@class='Polaris-Button_r99lw Polaris-Button--primary_7k9zs']//span[@class='Polaris-Button__Text_yj3uv']")
            # done.click()
            # print("out")
            #
            # time.sleep(1.5)
            # break

    return

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
            if count == 4:
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

        for pic in driver.find_elements(By.XPATH, "//div[@class='product-intro__thumbs-item']"):
            pic.click()
            pictures.append(pic.find_element(By.XPATH, "//div[@class='swiper-slide product-intro__main-item cursor-zoom-in swiper-slide-active']").find_element(By.TAG_NAME, "img").get_attribute("src"))

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
    itemList = phase1(driver, item, it)
    print(itemList)

    itemD = {}
    count = 0

    while itemList == -1:
        itemList = phase1(driver, item, it)

    divide()

    for i in itemList:
        notify("Currently Getting Details for: " + i["name"])

        item = phase2(driver,i["link"])

        login_shoppify(driver, "thenewwaveaesthetic@gmail.com", "Stormthec@stl3", item["name"].replace("SHEIN", "New Wave"), item["price"], item["SKU"], weight, item["pictures"])

        if len(i["Data ID"]) >= 0:
            addButton = driver.find_element(By.XPATH, "//span[@class='vNeOG']")
            addButton.click()

            variantBox = driver.find_element(By.XPATH, "//div[@class='e157U']").find_element(By.TAG_NAME, "input")
            variantBox.send_keys("Color")

            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)

            temp = []
            for id in i["Data ID"]:
                variant = phase2(driver, variantLink(i["link"], i["name"], id))
                addVariant(driver, variant["Color"], variant["price"], prettyRoundCheap(variant["price"]), variant["SKU"])
                loadImages(driver, variant["pictures"])

        divide()
        count += 1
        notify(str(count) + "/" + str(len(itemList)))

    # print(itemD)
    #
    # itemD = [
    #     {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223', 'price': '$3.99',
    #      'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #      'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #      'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #      'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #     [
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #         {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #          'price': '$4.49', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #         {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}],
    #     [{'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #      {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #       'price': '$4.49', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #      {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}], [
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #         {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #          'price': '$4.49', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #         {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}],
    #     [{'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #      {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #       'price': '$4.49', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #      {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}], [
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #         {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #          'price': '$4.49', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #         {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}],
    #     [{'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #      {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #       'price': '$4.49', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #      {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #       'price': '$3.99', 'pictures': [
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #          'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #      {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954', 'price': '$3.99',
    #       'pictures': [
    #           'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #           'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #       'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #       'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #       'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}], [
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'White', 'SKU': 'sw2202160411077223',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914354b21656b79db4d2d96b00994c758e93c8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/1647914361dfc0a57e70d017d3bf28284d96427388_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143594e3b80233a07eac36080eb3b586dda71_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/16479143639d242b16becdca7e153cf78c50f927e4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/05/1688563540798ed98685ea875bbf32adb97a7cf2d4_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/11/09/1667955985c548d35366c04c859a51df2c4e2a124b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/22/164791435684e49e16f7280b077fb3170300567987_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10079191-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/22/1647914366f6485a9111b460d3303e0337148259f9.webp'},
    #         {'name': 'SHEIN BASICS Solid Round Neck Slim Tee', 'Color': 'Maroon', 'SKU': 'sw2202160411085833',
    #          'price': '$4.49', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/1647841928741c0ca1702d0b739132999c9b4297f9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419331e4c778441957dfe644cea46af2d1296_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419359176ec45434382e9e739ff8fc8c98276_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/21/16478419319aae8f33de6a854bc8a090228cc63f30_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10069281-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/21/16478419381d5b2c61653a114f63e57eea56eed315.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Black', 'SKU': 'sw2202160411088321',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908791c93a7e013f4a200f8bde9bd714447e8_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/164869088119e7fe510cc94f6c46d6e9c4742303e0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/1648690883c0a1513a3e5331384704d7ee4e3e83cc_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/03/31/16486908855b523bbffa92165cd887ee1a0b083a07_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10179239-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/03/31/1648690888c843d2154afff492cc3edb0b270fdf3c.webp'},
    #         {'name': 'SHEIN BASICS Cap Sleeve Solid Crop Top', 'Color': 'Lilac', 'SKU': 'sS2012140040195252',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217481176504f5b8e762b2a6c1ecab3d466161_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174853cc203bb2659dcbfd49f4829a48e1780_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/16512174878f45a4636477929b16ead7ced3d8cc99_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217483432b1fdb8edb3f7df1903018ddab9560_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/04/29/1651217489e656f30bdd4c2bed5661fdba5d658e3a_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10447828-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/04/29/16512174923467c6e083c086528ab765d344f60111.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Blue', 'SKU': 'sw2204246799905548',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534562985e09524a2e4603235a668139e8435494_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/165345630307e4b2c816671d10fb01019ce3675d73_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563057c9a3fd7b509b82061c4f4c1e3514f88_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653456307e6c526e7bb1b24873da7362f2bb1f5ed_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534563006c4fb98d729de7c7386c71ad40bd64a0_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660054-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653456310a7f5dfb45f519c11ec583842223726ba.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mustard', 'SKU': 'sw2204246799954958',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459262cbe98e0280d867a3a3c8821581b507d2_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592666271ed625c276d375ddfa62071700b3b_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459269421609d831a4b6a59f6299da6f7d3f78_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/16534592715fdd749673940c6bfbbca85d1cc616af_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459273684a833544b77bb55a33be0b305858c9_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/25/1653459265f8ed194a73758397bfc6e6d58ab0371d_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10660174-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/25/1653459276226bfeb9c0e99278fea54f0c601bcb96.webp'},
    #         {'name': 'SHEIN BASICS Solid Form Fitted Tee', 'Color': 'Mocha', 'SKU': 'sw2204246799959954',
    #          'price': '$3.99', 'pictures': [
    #             'https://img.ltwebstatic.com/images3_pi/2023/07/08/1688801384e4c699359773006e670a396a5e64c57f_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537351b97ed94452d5d41e079d8c14e75d8783_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/165353735686188621feb58e135d68825c67314a40_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/16535373530412ad04e803c7d7f0e8eb93a4f97445_thumbnail_600x.webp',
    #             'https://img.ltwebstatic.com/images3_pi/2022/05/26/1653537359baced4e93ad6576b1d34f52a9db37d27_thumbnail_600x.webp'],
    #          'link': 'https://us.shein.com/SHEIN-BASICS-Solid-Form-Fitted-Tee-p-10673185-cat-1738.html?src_identifier=fc%3DWomen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar07%60jc%3Dreal_1766&src_module=topcat&src_tab_page_id=page_home1688049567200&mallCode=1',
    #          'sizes': {'2': '(XS)', '4': '(S)', '6': '(M)', '8/10': '(L)'},
    #          'colorPic': '//img.ltwebstatic.com/images3_pi/2022/05/26/1653537362d909b80e00fb14aa42dcd00dd4a63305.webp'}]]
    #
    # for item in itemD:
    #     if isinstance(item, dict):
    #         login_shoppify(driver, "thenewwaveaesthetic@gmail.com", "Stormthec@stl3", item["name"].replace("SHEIN", "New Wave"), item["price"], item["SKU"], weight, item["pictures"])
    #
    #     elif isinstance(item, list):
    #         first = True
    #
    #         login_shoppify(driver, "thenewwaveaesthetic@gmail.com", "Stormthec@stl3", item[0]["name"].replace("SHEIN", "New Wave"), item[0]["price"], item[0]["SKU"], weight, item[0]["pictures"])
    #
    #         addButton = driver.find_element(By.XPATH, "//span[@class='vNeOG']")
    #         addButton.click()
    #
    #         variantBox = driver.find_element(By.XPATH, "//div[@class='e157U']").find_element(By.TAG_NAME, "input")
    #         variantBox.send_keys("Color")
    #
    #         driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
    #
    #         for variant in item:
    #             addVariant(driver, variant["Color"], variant["price"], prettyRoundCheap(variant["price"]), first, variant["SKU"])
    #             # loadImages(driver, variant["pictures"])
    #             first = False
    #             print('--__________--')

        for x in driver.find_elements(By.XPATH, "//div[@class='Polaris-LegacyStack__Item_yiyol']//button"):
            if x.get_attribute("aria-label") == "Save":
                x.click()
                break

    return