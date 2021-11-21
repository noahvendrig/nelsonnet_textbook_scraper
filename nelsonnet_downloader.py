from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time

import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import cv2
import os
import random, string

from PIL import Image
def path():
    global chrome
    # Starts new chrome session
    chrome = webdriver.Chrome('D:\\noah\\py\\instamsger\\chromedriver_win32\\chromedriver.exe')# Add path if required

def url_name(url):
    chrome.get(url)
    # Adjust sleep
    time.sleep(3)


def login(username, password):
    time.sleep(1)
    usern = chrome.find_element_by_name("defaultControl$ctl00$place34$ctl00$PreLoginUserName")

    # sends the entered username
    usern.send_keys(username)
    usern.send_keys(Keys.RETURN)
    time.sleep(1.5)
    # finds the password box
    passw = chrome.find_element_by_name("defaultControl$ctl00$place34$ctl00$Password")

    # sends the entered password box
    passw.send_keys(password)

    # press enter after sending password
    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)
    

def grab_images(dir_name):

    

    os.mkdir(f'./{dir_name}')
    os.mkdir(f'./{dir_name}/raw')
    os.mkdir(f'./{dir_name}/cropped')
    
    time.sleep(10)
    

    # zoom_out = chrome.find_element_by_id("minimize-zoom")
    zoom_out = chrome.find_element_by_id("fitToHeight")
    zoom_out.click()

    fullscreen = chrome.find_element_by_id("fulscrnBtn")
    fullscreen.click()

    time.sleep(0.4)
    max_page_element = chrome.find_element_by_id("right-jump-input")
    max_page = max_page_element.get_attribute('value')
    print(max_page)
    page_num = 0
    counter = 1
    while page_num != max_page:
        
        page_num_element = chrome.find_element_by_id("jumpToPageInput")
        page_num = page_num_element.get_attribute('value')
        # print(page_num)

        content = chrome.find_element_by_id("page-wrap")
        # chrome.execute_script("document.body.style.zoom = '25%'")
        content.screenshot(f'./{dir_name}/raw/{counter}.png')

        # print("screenshotted!")

        next_btn = chrome.find_element_by_id('next-page-button')
        next_btn.click()
        # print("clicked next page")
        counter += 1
        time.sleep(1)

def crop_images(dir_name):#image_path, coords, saved_location
    dir = f"./{dir_name}/raw"
    for filename in os.listdir(dir):
        if filename.endswith('.png'): 
            im = cv2.imread(f'{dir}/{filename}')
            cropped_img = im[27: 860, 520:1165]
            cv2.imwrite(f'./{dir_name}/cropped/{filename}', cropped_img)
    
def make_pdf(dir_name):
    
    dir = f"./{dir_name}/cropped"
    images = [Image.open(f'{dir}/{img}').convert('RGB') for img in os.listdir(dir)]
    im1 = images[0]

    im1.save(f'./{dir}/{dir_name}.pdf',save_all=True, append_images=images[1:])

def main(url):
    dir_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    path()
    time.sleep(1)
    url_name(url)
    # login(username, password)
    grab_images(dir_name)
    crop_images(dir_name)
    make_pdf(dir_name)
    time.sleep(1)
    # chrome.close()
    print("closed")

url = "https://redirect.nelsonnet.com.au/?token=5C840EC2B256A62D01ECB1D834704A8567C2624D1570901E35521CD4516260CCE879B1982065CBEC5DCE1F8FA8AC66915A881B9C8FBE506501FABB97B0A91401EE9480A684543A2F&pid=553606&eISBN=9780170409049&titleIsbn=9780170408998&ptoken=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3VzZXJkYXRhIjoie1wiTG9naW5TdGF0dXNcIjpcIlNTTyBBdXRob3Jpc2VkXCIsXCJDdXN0b21EYXRhXCI6e30sXCJDaGVja1BvaW50QVwiOlwiXCIsXCJDaGVja1BvaW50UVwiOlwiXCIsXCJDb3VudHJ5XCI6XCJBVVNcIixcIkVtYWlsXCI6XCJub2FoLnZlbmRyaWdAZWR1Y2F0aW9uLm5zdy5nb3YuYXVcIixcIkZpcnN0TmFtZVwiOlwiTm9haFwiLFwiSW5zdGl0dXRpb25JZFwiOlwiXCIsXCJJbnN0aXR1dGlvbk5hbWVcIjpcIkZPUlQgU1RSRUVUIEhJR0ggU0NIT09MXCIsXCJJc0luc3RydWN0b3JcIjpmYWxzZSxcIklzUGVuZGluZ0luc3RydWN0b3JcIjpmYWxzZSxcIkxhc3ROYW1lXCI6XCJWZW5kcmlnXCIsXCJNYWdlbGxhbklkXCI6XCJcIixcIlVzZXJHcm91cHNcIjpudWxsLFwiUGFzc3dvcmRcIjpudWxsLFwiU2Nob29sQWZmaWxpYXRpb25cIjpcIjEtMjdJMS05MzRcIixcIlNzb0d1aWRcIjpcIjk2MWEwYWMxNjFmMGU5ZWY6NTY5MWNhYWM6MTc4MWY1NmJjMTc6NDZjNFwiLFwiU3NvVG9rZW5cIjpcIjNFREExNENCNkFGQkNCQTQzN0MyOENEMDk1NDgzMEJERjY5N0RDNDZEMDY4REI1NjQwMTJEMDkyQkYzRUM2QkMzNkQ4QkUxODREOTk0Njc0NUI0ODJCRTlDOTVBRDY3NkIxOUI4RUM3RkY0MUEzNDNEODlCNTU1REY2ODI5Q0RFMkEyRTNBNUEyNTFFQkUwM1wiLFwiU3RhdGVcIjpcIk5TV1wiLFwiU3RhdHVzXCI6NCxcIkRpdmlzaW9uXCI6XCJcIixcIlVzZXJUeXBlXCI6XCJzdHVkZW50XCJ9IiwibmJmIjoxNjM3NDE5NjQzLCJleHAiOjE2Mzc0MjA4NDMsImlhdCI6MTYzNzQxOTY0M30.jN8NWbAIby8lG1ekjHM6DZJw0ktkxENMGtn4QeT7UknjWTmZvINDWCCgSadZn3gPX-YJWq31VT8y_e8-bKMWNg"
# url = "https://www.nelsonnet.com.au/login"

main(url)

# crop_images('BjF3qJcsnakJ3jDI')
# make_pdf('BjF3qJcsnakJ3jDI')