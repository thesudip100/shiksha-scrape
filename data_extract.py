from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import json
import time
#import requests
#from requests import head

main_url='https://www.shiksha.com'

data_list = []
data = {}

output_file = 'data.json'

def extractdata(page):
    tplwrpr=page.query_selector('#tuplewrapper')
    if tplwrpr:
        x=tplwrpr.query_selector_all('._1822._0fc7._7efa')
        print(len(x))
    for i in x:
        if i:
            #for title
            title_finder = i.query_selector('h3.f7cc')
            title = title_finder.inner_text()
            data['University Name'] = title

            #for location
            location_locator = i.query_selector('span._5588')
            location = location_locator.inner_text()
            data['Location'] = location

            #for courses offered, tuition fee, scholarships
            column_div = i.query_selector('.cd4f._5c64.contentColumn_3')
            columns = column_div.query_selector_all('._77ff')
            info = {}
            for column in columns:
                heading =column.query_selector('.abce')
                information = column.query_selector('.dcfd.undefined')
                if heading and information:
                    info[f'{heading.inner_text()}']=information.inner_text()
            data['Additional info']=info




            print(data)

                
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=50)
    page = browser.new_page()

    try:

        page.goto('https://www.shiksha.com/studyabroad/australia/universities')

        page.wait_for_selector('#main-wrapper')

        tuple_wrapper=page.query_selector('#tuplewrapper')

        time.sleep(7)


        for i in range(1):
            page.mouse.wheel(0, 500)
            time.sleep(2)
            extractdata(page)
            try:
                lazy_button=tuple_wrapper.query_selector('#lazy_load_next_4')
                button = lazy_button.query_selector('#lazy_load_next_btn_4')
                if button and button.is_visible():
                    button.click()
                    page.mouse.wheel(0,-5000)
                extractdata(page)
            except:
                continue
            
                
    except Exception as e:
        print(e)


        time.sleep(3)

        browser.close()
    except Exception as ex:
        print(ex)

    # try: 
    #     url={}
    #     with open(output_file,'r') as file:
    #         url = json.load(file)
        
    #     with open(output_file,'w') as file:
    #         url = {**url,**unique_urls}
    #         json.dump(url,file,indent=3)

    # except Exception as e:
    #     print("Error opening file ",e)
    #     with open(output_file,'w') as file:
    #      json.dump(unique_urls,file,indent = 3)


    # Close the browser
    browser.close()