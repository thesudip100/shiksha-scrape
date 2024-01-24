import json
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import requests


url = {}
json_file = 'list.json'
data_file = 'data.json'


with open(json_file,'r') as file:
    links = json.load(file)


data = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=50)
    page = browser.new_page()
    for link in links:
        page.goto(link)
        page.wait_for_selector("#main-wrapper")
        time.sleep(2)
        #to get the title of university
        try:
            titles_locator = page.query_selector(".e70a13")
            titles = titles_locator.inner_text()
            clean_title = titles.split(':')
            if True:
                data['University name'] = clean_title[0]
        except: 
            pass  
        #to get the location of the university
        try:
             location_locator = page.query_selector("._7164e4.ece774.ece774")
             location = location_locator.inner_text()
             
             if True:
                  data['University_location'] = location
        except:
             pass
        
        #trying to get the accepted exams
        # try:
        #     page.mouse.wheel(0,500)
        #     accepted_exams_button = page.query_selector("._7ed9")
        #     if accepted_exams_button and accepted_exams_button.is_visible():
        #          accepted_exams_button.click()
        #          accepted_exam_div = page.query_selector("._17b3")
        #          for i in accepted_exam_div:
        #             accepted_exam = i.query_selector(".e3f3.ripple.dark")
        #             clean_accepted_exam = accepted_exam.inner_text()
        #             if True:
        #                     data[f'accepted exams{i}'] = clean_accepted_exam
        # except:
        #      pass
        
        #to get scholarships
        try:
            page.mouse.wheel(0,700)
            scholarship_locator = page.query_selector(".c221")
            scholarship = scholarship_locator.get_attribute("a")
            print(scholarship)
            # if True:
            #     data['scholarships'] = scholarship
        except:
            pass
        
    try:
        data1 = {}
        with open (data_file,'r') as f:
            data1 = json.load(f)
        with open(data_file,'w')as f:
            data1 = {**data1,**data}
            json.dump(data1,file,indent=3)

    except Exception as e:
        with open(data_file,'w')as f: 
            print('No value',e)
            json.dump(data,f,indent=3)