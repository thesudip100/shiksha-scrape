import json
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


url = {}
json_file = 'list.json'
data_file = 'data.json'
courses_file = 'courses.json' 
individual_uni = []
data ={}
courses = []
# courses_details = {}

with open(json_file,'r') as file:
    links = json.load(file)


def extractcourses(page):
    courses_main = page.query_selector("#main-wrapper")
    if courses_main:
        y = courses_main.query_selector("._036cde")
        w = y.query_selector_all("._1822._0fc7._80b2")
        for x in w:
            courses_details={}
            #course title
            program_title_div = x.query_selector(".c8ff")
            program_title_locator = program_title_div.query_selector("a.ripple.dark")
            program_title_found = program_title_locator.query_selector("h3")
            program_title = program_title_found.inner_text()
            time.sleep(1)
            if True:
                print(program_title)
                courses_details['Course Name'] = program_title
                # courses.append(courses_details)
                data['Programs and details'] = courses
            
            
            #course duratioin
            course_duration_locator_div = x.query_selector(".edfa")
            course_duration_locator = course_duration_locator_div.query_selector_all("span")
            course_duration_found = course_duration_locator[0]
            course_duration = course_duration_found.inner_text()
            time.sleep(1)
            if True:
                print(course_duration)
                courses_details["Course Duration"] = course_duration
                # courses.append(courses_details)
                data["Programs and details"] =courses

            #course_info
            #accepted_exams
            accepted_exams = []
            course_info_locator_div = x.query_selector(".cd4f._5c64.contentColumn_2")
            course_info_locator = course_info_locator_div.query_selector_all("._77ff")
            exam_accepted_locator = course_info_locator[0].query_selector(".dcfd.undefined")
            if exam_accepted_locator:
                exam_accepted_list = exam_accepted_locator.query_selector_all("li")
                for i in exam_accepted_list:
                    exam_accepted = i.query_selector("a")
                    if exam_accepted:
                        exams = exam_accepted.inner_text()
                        time.sleep(1)
                        if True:
                            print(exams)
                            accepted_exams.append(exams)
                            courses_details['Accepted Exams'] = accepted_exams
                            # courses.append(courses_details)
                            data["Programs and details"] = courses

            # #work-experience,scholarships,12th marks
            # work_experience_locator = course_info_locator[1].query_selector(".dcfd.undefined")
            # if work_experience_locator:
            #     work_experience_found = work_experience_locator.query_selector_all("li")
            #     for i in work_experience_found:
            #         work_experience = i.inner_text()
            #         if work_experience=='– / –':
            #             time.sleep(4)
            #             print('None')
            #         else:    
            #             print(work_experience)

            #first-year tuition fee
            tuition_fee_locator = course_info_locator[3].query_selector(".dcfd.undefined")
            if tuition_fee_locator:
                tuition_fee = tuition_fee_locator.inner_text()
                time.sleep(1)
                if True:
                    print(tuition_fee)
                    courses_details["Tuition Fee"] = tuition_fee
                    # courses.append(courses_details)
                    data['Programs and details'] = courses
            courses.append(courses_details)
            








def courses_mouse_scroll(page):
    for i in range(10):
        page.mouse.wheel(0,1000)
        page.wait_for_selector(".d6db")









with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=50)
    page = browser.new_page()
    for link in links:
        data = {}
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
        
        #trying to get the about us section

        try:
            for i in range(3):
                page.mouse.wheel(0,750)
                time.sleep(3)
            for i in range(2):
                page.mouse.wheel(0,-750)
                time.sleep(3)
                
            info_section_locator = page.query_selector(".de91")
            about_us_locator = info_section_locator.query_selector("._8efd._57fd.bb73._48ca.expanded" )
            read_more_button_locator = about_us_locator.query_selector("span._5ee4")
            if read_more_button_locator and read_more_button_locator.is_visible:
                read_more_button_locator.click()
                time.sleep(2)
            info_locator = about_us_locator.query_selector(".faq__according-wrapper")
            info = info_locator.inner_text()
            if True:
                data['About University'] = info
        except:
            pass


        #trying to get the table info
        try:
            table_info = page.query_selector(".table.d00e.d8b0.b3f1")
            more_info = {}
            if table_info:
                rows = table_info.query_selector_all("tr")
                for row in rows:
                    row_locator = row.query_selector_all("td")
                    for outputs in row_locator:
                        table_content_title = outputs.query_selector_all("._98ab")
                        for title in table_content_title:
                            table_title = title.inner_text()
                        table_content_data = outputs.query_selector_all(".bcb8")
                        for output in table_content_data:
                            table_data = output.inner_text()
                    more_info[f'{table_title}'] = table_data
                    unwanted_keys = ["Website","Accepted Exams", "International Students Website"]
                    for key in unwanted_keys:
                        more_info.pop(key, None)
                    
                    data['More info'] = more_info
        except:
            pass

        individual_uni.append(data)

        time.sleep(3)

        #accessing courses and fees button
        navigation_locator = page.query_selector(".cd4637.navbarSlider")
        courses_button_locator = navigation_locator.query_selector_all("li")
        courses_button = courses_button_locator[1]
        courses_anchor = courses_button.query_selector("a")
        courses_link = courses_anchor.get_attribute('href')
        courses_url = urljoin(link,courses_link)
        

        #courses and fees page
        page.goto(courses_url)
        time.sleep(2)
        page.wait_for_selector("#main-wrapper")
    
        page.mouse.wheel(0,500)
        time.sleep(2)
        page.wait_for_selector("#acp-tuples")
    
        
        for i in range(10):
            page.mouse.wheel(0,1000)
            time.sleep(1)
            page.wait_for_selector(".d6db")
        extractcourses(page)
        page.wait_for_selector(".d6db")
        while True:
            pagination_locator_div = page.query_selector(".d6db")
            pagination_locator = pagination_locator_div.query_selector("._6583")
            numbers_arrows = pagination_locator.query_selector_all("li")
            # forward_arrow = numbers_arrows[6]
            if len(numbers_arrows) >= 7 and numbers_arrows[6].is_visible():
                numbers_arrows[6].click()
                time.sleep(1)
                courses_mouse_scroll(page)
                extractcourses(page)
            else:
                extractcourses(page)
                break





            

            
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
        # try:
        #     page.mouse.wheel(0,700)
        #     scholarship_locator = page.query_selector(".c221")
        #     scholarship = scholarship_locator.get_attribute("a")
        #     print(scholarship)
        #     # if True:
        #     #     data['scholarships'] = scholarship
        # except:
        #     pass
        
    # try:
    #     data1 = {}
    #     with open (data_file,'r') as f:
    #         data1 = json.load(f)
    #     with open(data_file,'w')as f:
    #         main_data = {**data1,**data}
    #         json.dump(main_data,f,indent=3)

    # except Exception as e:
    #     with open(data_file,'w')as f: 
    #         json.dump(data,f,indent=3)
    # with open (courses_file,'w') as f:
    #     json.dump(courses,f,indent=3)


        # try:
        #     with open(data_file,'r') as f:
        #         existing_data = json.load(f)

        #     with open(data_file,'w') as f:
        #         individual_uni.extend(existing_data)
        #         json.dump(individual_uni,f,indent=3)
        # except:
        #     with open (data_file,'w') as f:
        #         json.dump(individual_uni,f,indent=3)

        try:
            with open(data_file, 'r') as f:
                existing_data = json.load(f)

            # Check if the current university's data already exists in the existing data
            updated_existing_data = existing_data[:]  # Create a copy to avoid modifying the original list
            for idx, uni_data in enumerate(updated_existing_data):
                if uni_data['University name'] == data['University name']:
                    # Update existing data with new data
                    updated_existing_data[idx] = data
                    break  # Stop searching as the university's data is found

            # If the current university's data doesn't exist, append it
            if data not in updated_existing_data:
                updated_existing_data.append(data)

            with open(data_file, 'w') as f:
                json.dump(updated_existing_data, f, indent=3)
        except FileNotFoundError:
            # If the file doesn't exist, write the current university's data directly
            with open(data_file, 'w') as f:
                json.dump([data], f, indent=3)

    