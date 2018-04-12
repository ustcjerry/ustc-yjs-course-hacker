# -*- coding:utf-8 -*-

from newknn import Captcha
from config import *
from bs4 import BeautifulSoup
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from mail import send_email


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.PhantomJS()

login_flag = False
chance = False

print('new start')
newstart = 'new start'
send_email(newstart, newstart.encode('utf-8'))


def get_captcha(driver, element, path):
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    image = cv2.imread(path)
    image = image[location['y']:location['y']+size['height'],location['x']:location['x']+size['width']]
    captcha = Captcha()
    code = captcha.hack_img(image)
#    print ('Recognized captcha code:'+code)
    return code


def central_auth_login(driver):
    driver.implicitly_wait(req_timeout)
    driver.get('https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fyjs%2Eustc%2Eedu%2Ecn%2Fdefault%2Easp')

    try:
        assert driver.title == "中国科学技术大学统一身份认证系统"
    except Exception as e:
        print('Assertion test fail.', format(e))
        driver.refresh()
        return False

    driver.find_element_by_name("login").send_keys(student_no)
    driver.find_element_by_name("password").send_keys(ustcmis_password)
    driver.find_element_by_name("button").click()

    print(driver.title)

    try:
        assert driver.title == "中国科学技术大学研究生信息平台"
    except Exception as e:
        print('Assertion test fail.', format(e))
        driver.refresh()
        return False

    driver.switch_to.frame("top-frame")

    try:
        driver.execute_script("setmenu(5)")
    except Exception as e:      # 这里因为网页自身原因会产生异常，不用管
        # print(e)
        driver.refresh()

    #driver.get_screenshot_as_file("./test2.jpg")  # 屏幕截图
    driver.switch_to.default_content()
    driver.switch_to.frame("menu-frame")

    driver.get(driver.find_element_by_id("mm_2").get_attribute('href'))

    #driver.get_screenshot_as_file("./test3.jpg")  # 屏幕截图

    driver.switch_to.frame("mainFrame")
    driver.switch_to.frame("I2")
    driver.switch_to.frame("xkpFrame")
    fin = driver.find_element_by_link_text("综合绘画创作")               # 课程名称
    print(fin.get_attribute('href'))

    if 'gradkcjs.do?kcid=6017' in fin.get_attribute('href'):       # 这里是课程连接地址，用于判断是否成功进行到这一步
        print('login OK')
        return True
    else:
        print('login False')
        return False


def classic_login(driver):
    driver.implicitly_wait(req_timeout)
    driver.get('http://yjs.ustc.edu.cn/default_yjsy.asp')

    try:
        assert driver.title == "中国科学技术大学研究生信息平台"
    except Exception as e:
        print('Assertion test fail.', format(e))
        driver.refresh()
        return False

    ele_captcha = driver.find_element_by_xpath("//img[contains(./@src, 'checkcode.asp')]")

    code = get_captcha(driver, ele_captcha, "captcha.png")
    print('Recognized captcha code:' + code)

    driver.find_element_by_name("userid").send_keys(student_no)
    driver.find_element_by_name("userpwd").send_keys(ustcmis_password)
    driver.find_element_by_name("txt_check").send_keys(code)
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/input").click()

    print(driver.title)

    try:
        driver.find_element_by_id("main-frame")
    except Exception as e:
        print('Assertion test fail.', format(e))
        driver.refresh()
        return False

    driver.switch_to.frame("top-frame")

    try:
        driver.execute_script("setmenu(5)")
    except Exception as e:      # 这里因为网页自身原因会产生异常，不用管
        # print(e)
        driver.refresh()

    #driver.get_screenshot_as_file("./test2.jpg")  # 屏幕截图
    driver.switch_to.default_content()
    driver.switch_to.frame("menu-frame")

    driver.get(driver.find_element_by_id("mm_2").get_attribute('href'))

    #driver.get_screenshot_as_file("./test3.jpg")  # 屏幕截图

    driver.switch_to.frame("mainFrame")
    driver.switch_to.frame("I2")
    driver.switch_to.frame("xkpFrame")
    fin = driver.find_element_by_link_text("综合绘画创作")               # 课程名称
    print(fin.get_attribute('href'))

    if 'gradkcjs.do?kcid=6017' in fin.get_attribute('href'):       # 这里是课程连接地址，用于判断是否成功进行到这一步
        print('login OK')
        return True
    else:
        print('login False')
        return False


def choose(driver):
    for i in range(1, login_max_try):
        try:
            login_flag = classic_login(driver)                           # 两种登录方式： 统一身份认证 和 平台登录 方式
            # login_flag = central_auth_login(driver)
        except Exception as e:
            print(e)
            login_flag = False
            pass
        if login_flag:
            break
        time.sleep(1)
    driver.execute_script("xk('AT0400201')")   # 这里是选课按钮对应的 JavaScript




while not chance:
    driver.get('http://mis.teach.ustc.edu.cn/gradXkmd_yx.do?xnxq=20172&kcbjh=AT0400201')      # 这里是查看已选人数的连接
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table', {'id': 'jcxxtable0'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    print(len(rows))
    if len(rows) < 41:                                                                         # 这里是选课人数上限 +1
        mymail = "chance !"
        send_email(mymail, mymail.encode('utf-8'))
        #new_driver = webdriver.PhantomJS()
        new_driver = webdriver.Chrome(chrome_options=chrome_options)
        choose(new_driver)
        chance = True
    time.sleep(interval)


# classic_login(driver)
# central_auth_login(driver)

driver.close()
new_driver.close()

