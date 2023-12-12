
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import sys
import openpyxl
import os

from datetime import datetime
from openpyxl.styles import Font

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# /home/shreyansh/.config/google-chrome/Default


if len(sys.argv) >= 2:
    url = sys.argv[1]
    print(f"Scraping URL: {url}")
else:
    print("No URL provided.")

custom_dir = '/home/shreyansh/.config/google-chrome/Default'
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f"--user-data-dir={custom_dir}")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# print(1111111111, url)

today_date = datetime.now().strftime('%-m/%-d/%Y')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

driver.get(url)
import time
# time.sleep(30)
# driver.get_screenshot_as_file("url.png")
driver.execute_script("alert('Start Scraping');")
time.sleep(10)
# print(22222222222222222)

driver.implicitly_wait(10)
upwork = {}
# /html/body/div[3]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/section/div[3]/div[2]/div[1]/div[1]/div[2]
# /html/body/div[3]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/section/div[3]/div[2]/div[1]/div[1]/div[2]

fields = {
    'Business Manager': None,
    'Sent from': None,
    'Source': None,
    'Location': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[2]/div[1]/div[4]/span[1]',
    'Template Used': None,
    'Project Name as it appears on site.': "/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[1]/h3",
    'Posted Date': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[1]/ul/li[2]',
    '# of Proposals': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[2]/div[1]/div[4]/div[1]/div',
    'Project Hourly Rate': '/html/body/div[3]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/section/div[1]/div[2]/ul/li[2]/div/div[2]',
    'Our Hourly Rate': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[3]/div[2]/div[1]/div[1]/div[2]',
    'Project Duration': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[2]/ul/li[3]/div/strong',
    'Fixed Price': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[2]/ul/li[2]/small',
    'Date': None,
    'Boosted?': None,
    'Boosted Differiental': None,
    'Client Name as it appears on site.': None,
    'Lead': None,
    'Good Lead': None,
    'Client' : None,
    # 'Project Length': '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[2]/ul/li[3]/small/span[1]'
}

# print(33333333333333333333)



# def login():
#     '''
#     This is for login
#     '''

#     element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "login_username")))
#     element.send_keys('dipali.pdh@gmail.com')
#     driver.find_element(By.ID, "login_password_continue").click()
#     password_input = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.ID, "login_password")))
#     password_input.send_keys("qwerty12345")
#     driver.find_element(By.ID, "login_control_continue").click()


def get_data():
    for field, xpath in fields.items():
        try:
            value = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))).text
            
        except NoSuchElementException:
            value = '' 
        except:
            value = ''
        upwork[field] = value
    # if upwork['Project Length'] == 'Project Length':
        upwork['Project Duration'] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[1]/div[2]/ul/li[3]/div/strong'))).text
    else:
        upwork['Project Duration'] = ''

    if upwork['Fixed Price'] == 'Hourly':
        upwork['Fixed Price'] = 'N/A'
        if upwork['Our Hourly Rate'] == '':
            try:
                upwork['Our Hourly Rate'] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[3]/div[2]/div[1]/div[1]/div[2]'))).text
            except NoSuchElementException:
                upwork['Our Hourly Rate'] = ''
            except TimeoutException:
                upwork['Our Hourly Rate'] = ''
    else:
        try:                                                   
            upwork['Fixed Price'] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/up-app/div/div/main/div[2]/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/section/div[3]/div[2]/div/div[2]/div[2]'))).text
        except NoSuchElementException:
            upwork['Fixed Price'] = 'N/A'
        except TimeoutException:
            upwork['Fixed Price'] = 'N/A'
    upwork['Date'] = today_date
    print(666666666666666666, upwork)
    # breakpoint()
    return upwork



# Function to authenticate the application using token.json
def authenticate(upwork):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    return service

# Function to update Google Spreadsheet
def update_google_sheet(service, upwork):
    spreadsheet_id = '1ldnEqWD-GZtJ7v67tjDNgkhnWR4FPMpNJ7v5nRqaAKc'  # Replace with your spreadsheet ID
    range_name = "New - Bid & Lead Tracker - 2023!A1"  # Replace 'A1' with the cell you want to start appending the data
  # Replace with your sheet name

    
    # Your list of values to be inserted
    values = [[upwork[key] for key in fields.keys()]]
    project_name = upwork['Project Name as it appears on site.']
    hyperlink_formula = f'=HYPERLINK("{url}", "{project_name}")'
    values[0][list(fields.keys()).index('Project Name as it appears on site.')] = hyperlink_formula

    body = {'values': values}

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    print('Data updated successfully.')
    driver.execute_script("alert('Data scraped and saved to excel successfully');")
    time.sleep(10)

# Get your data (upwork_data)
upwork_data = get_data()  # Replace this with your data retrieval function

# Authenticate the application using token.json
service = authenticate(upwork)    

# Update the Google Spreadsheet with the obtained data
update_google_sheet(service, upwork_data)

