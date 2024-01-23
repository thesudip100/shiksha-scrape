from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import json
import time
#import requests
#from requests import head

main_url='https://www.shiksha.com/studyabroad/australia/universities'
extracted_urls = set()
output_file = 'list.json'
def extracturl(page):
    tplwrpr=page.query_selector('#tuplewrapper')
    if tplwrpr:
        x=tplwrpr.query_selector_all('._1822._0fc7._7efa')
        print(len(x))
    for i in x:
        if i:
            anchors = i.query_selector_all('a')
            for anchor in anchors:
                href=anchor.get_attribute('href')
                extracted_urls.add(href)
                

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=50)
    page = browser.new_page()

    try:

        page.goto('https://www.shiksha.com/studyabroad/australia/universities')

        page.wait_for_selector('#main-wrapper')

        tuple_wrapper=page.query_selector('#tuplewrapper')

        time.sleep(7)


        for i in range(12):
            page.mouse.wheel(0, 2400)
            time.sleep(2)

            try:
                lazy_button=tuple_wrapper.query_selector('#lazy_load_next_4')
                button = lazy_button.query_selector('#lazy_load_next_btn_4')
                #this line is hindering the data extraction
                if button and button.is_visible():
                    button.click()
                extracturl(page)    
            except:
                continue
   
                
    except Exception as e:
        print(e)


        time.sleep(3)

        browser.close()
    except Exception as ex:
        print(ex)




    # Close the browser
    browser.close()

    unique_urls = list(extracted_urls)
    with open(output_file, 'w') as json_file:
        json.dump(unique_urls, json_file, indent=3)