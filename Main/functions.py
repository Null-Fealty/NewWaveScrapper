from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import json
import time

def divide():
    print((("###############" * 4 ) + "\n") * 3)

def notify(message):
    print("-" * 20, "\n" + message+ "\n", "-"*20 + "\n")

def closeCoupons(driver):
    wait = WebDriverWait(driver, 5)

    try:
        el = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='suiiconfont sui_icon_closed_18px_1 she-close']")))
        el.find_element(By.TAG_NAME, "i").click()

    except:
        print("N/A")

    try:
        coupon_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.c-coupon-box')))
        coupon_box.find_element(By.CSS_SELECTOR, 'i.iconfont.icon-close.she-close').click()
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
    driver.implicitly_wait(15)

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

def login_shoppify(driver, user, password):
    try:
        load(driver, ("https://7318a2.myshopify.com/admin/products"))

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

def phase1(driver, category, it):
    if it <= 8:
        return False

    try:
        load(driver, category)
        closeCoupons(driver)
        notify("Currently in " + category )

        itemList = []
        elements = driver.find_elements(By.XPATH, "//section[@class='S-product-item j-expose__product-item product-list__item']")
        count = 0
        for i in elements:
            count += 1
            print(str(count) + "/" + str(len(elements)))
            temp = {}
            name = i.find_element(By.TAG_NAME, "a").get_attribute("aria-label")
            link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
            dataIDS = []
            for id in i.find_elements(By.TAG_NAME, "label"):
                if not(id.get_attribute("data-id") is None):
                    dataIDS.append(id.get_attribute("data-id"))

            temp["name"] = name
            temp["link"] = link
            temp["Data ID"] = dataIDS
            itemList.append(temp)

        with(open(str(it) + "_info.txt", "w")) as f:
            f.write(json.dumps(itemList, indent=4))

        return itemList

    except:
        return -1

    finally:
        load(driver, "https://www.google.com")

def phase2(driver, link):
    try:
        load(driver, link)
        item = {}
        sizes = {}
        description = {}
        pictures = []

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

        for i in driver.find_elements(By.XPATH, '//div[@class="product-intro__description-table-item"]'):
            description[i.find_element(By.CLASS_NAME, "key").text] = i.find_element(By.CLASS_NAME, "val").text

        try:
            driver.find_element(By.XPATH, "//div[@class='product-intro__size-choose']")
            for i in driver.find_element(By.XPATH, "//div[@class='product-intro__size-choose']").find_elements(By.TAG_NAME, "span"):
                size, quantity = i.find_element(By.TAG_NAME, "div").get_attribute("aria-label").split()
                sizes[size] = quantity

        except:
            print("")

        for pic in driver.find_element(By.CLASS_NAME, "product-intro__thumbs-inner").find_elements(By.TAG_NAME, "img"):
            pictures.append(pic.get_attribute("src"))

        item[colorName[0]] = colorName[1]
        item[SKU[0]] = SKU[1]
        item["price"] = price
        item["pictures"] = pictures
        item["description"] = description
        item["link"] = link

        try:
            item["sizes"] = sizes
        except:
            print("")

        try:
            item["colorPic"] = colorPic
        except:
            print("")

        return item

    except:
        print("reloading")
        load(driver, "https://www.google.com")
        phase2(driver, link)

    finally:
        load(driver, "https://www.google.com")

def main(driver, item, it):
    itemList = phase1(driver, item, it)
    if itemList == False:
        return

    while itemList == -1:
        itemList = phase1(driver, item, it)

    divide()

    itemD = {}
    count = 0
    for i in itemList:
        itemD[i["name"]] = []
        notify("Currently Getting Details for: " + i["name"])

        if len(i["Data ID"]) > 0:
            for id in i["Data ID"]:
                itemD[i["name"]].append(phase2(driver, variantLink(i["link"],i["name"],id)))
        else:
            itemD[i["name"]].append(phase2(driver,i["link"]))
        divide()
        count += 1
        notify(str(count) + "/" + str(len(itemList)))

    with(open(str(it) + ".txt", "w")) as f:
        f.write(json.dumps(itemD, indent=4))

    divide()

def mainTwo(driver):
    # user = "thenewwaveaesthetic@gmail.com"
    # password = "Stormthec@stl3"
    #
    # login_shoppify(driver, user, password)


    time.sleep(1000)