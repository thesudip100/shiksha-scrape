from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import json
import time
import requests

from requests import head
main_url='https://www.shiksha.com/studyabroad/australia/universities'
urls=[]
def extracturl(page):
    tplwrpr=page.query_selector('#tuplewrapper')
    if tplwrpr:
        x=tplwrpr.query_selector_all('._1822._0fc7._7efa')
        print(len(x))
    # for i in x:
    #     if i:
    #         anchors = i.query_selector_all('a')
    #         for anchor in anchors:
    #             href=anchor.get_attribute('href')
                
    #             print(href)
    #             break

            


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=50)
    page = browser.new_page()

    try:

        page.goto('https://www.shiksha.com/studyabroad/australia/universities')

        page.wait_for_selector('#main-wrapper')
        tuple_wrapper=page.query_selector('#tuplewrapper')

        time.sleep(5)


        for i in range(30):
            page.mouse.wheel(0, 1000)
            time.sleep(5)

            try:
                lazy_button=tuple_wrapper.query_selector('#lazy_load_next_4')
                button = lazy_button.query_selector('#lazy_load_next_btn_4')
                if button and button.is_visible():
                    button.click()
                    page.wait_for_timeout(15000)
                

            except:
                continue        
        extracturl(page)
        time.sleep(5)



    except Exception as e:
        print(e)


        time.sleep(20)

        browser.close()
    except Exception as ex:
        print(ex)



    # Close the browser
    browser.close()