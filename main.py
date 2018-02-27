# -*- coding:utf-8 -*-

from newknn import Captcha
import urllib, http.cookiejar, os, zlib, time, getpass, sys,re
from config import *
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from mail import send_email

captcha = Captcha()

driver = webdriver.PhantomJS()

login_flag = False
pre_login_flag = False
chance = False



print('new start')
newstart = 'new start'
send_email(newstart, newstart.encode('utf-8'))


def pre_login(driver):
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

    if driver.title == "中国科学技术大学研究生信息平台":
        print('pre_login OK')
        return True
    else:
        print('pre_login False')
        return False


def login(driver):

    try:
        assert driver.title == "中国科学技术大学研究生信息平台"
    except Exception as e:
        print('Assertion test fail.', format(e))
        driver.refresh()
        return False

    print(driver.title)

    driver.switch_to.frame("top-frame")

    try:
        driver.execute_script("setmenu(5)")
    except Exception as e:      # 这里因为网页自身原因会产生异常，不用管
        # print(e)
        driver.refresh()

    #driver.get_screenshot_as_file("./test2.jpg")  # 屏幕截图
    driver.switch_to.default_content()
    driver.switch_to.frame("menu-frame")

    aaa=driver.find_element_by_id("mm_2")


    print(aaa.get_attribute('href'))

    driver.get(aaa.get_attribute('href'))

    #driver.get_screenshot_as_file("./test3.jpg")  # 屏幕截图

    driver.switch_to.frame("mainFrame")
    driver.switch_to.frame("I2")
    driver.switch_to.frame("xkpFrame")
    fin=driver.find_element_by_link_text("综合绘画创作")               # 课程名称
    print(fin.get_attribute('href'))

    if 'gradkcjs.do?kcid=6017' in fin.get_attribute('href'):       # 这里是课程连接地址，用于判断是否成功进行到这一步
        print('login OK')
        return True
    else:
        # print('login False')
        return False



def choose(driver):
    for i in range(1,login_max_try):
        try:
            pre_login_flag = pre_login(driver)
        except Exception as e:
            print(e)
            pre_login_flag = False
            pass
        if pre_login_flag:
            break
        time.sleep(1)

    for i in range(1, login_max_try):
        try:
            login_flag = login(driver)
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
        mymail="chance !"
        send_email(mymail, mymail.encode('utf-8'))
        new_driver = webdriver.PhantomJS()
        choose(new_driver)
        chance = True
    time.sleep(interval)


driver.close()
new_driver.close()




# # 以下是识别验证码部分，暂时没用到
#
# headers = {
#      'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
#     'Connection': 'keep-alive'
#  }
# cookie_support = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
# opener = urllib.request.build_opener(cookie_support)
#
# req = urllib.request.Request(
#     url = 'http://yjs.ustc.edu.cn/checkcode.asp',
#     headers=headers
# )
# content = urllib.request.urlopen(req, timeout=req_timeout).read()
#
# code = captcha.hack(content)
#
# print('Recognized captcha code:'+code)


