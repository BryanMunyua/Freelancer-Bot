import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re
import openai
import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv

def nameCheck(namesToCheck, sentence):
    count = 0
    for i in namesToCheck:
        if i in sentence:
            count = count + 1

    return count

driver = webdriver.Chrome()
url = 'https://www.freelancer.com/login'
driver.get(url)
sleep(2)

driver.maximize_window()
sleep(2)

username = 'bryanmunyua@gmail.com'
password = 'Dexter_#254'

usernameField = driver.find_element(By.ID,'emailOrUsernameInput')
usernameField.send_keys(username)
sleep(2)

passwordField = driver.find_element(By.ID,'passwordInput')
passwordField.send_keys(password)
sleep(2)

submitButton = driver.find_element(By.XPATH,'/html/body/app-root/app-logged-out-shell/app-login-page/fl-container/fl-bit/app-login/app-credentials-form/form/app-login-signup-button/fl-button/button')
submitButton.click()

while driver.title != 'Dashboard | Freelancer':
    sleep(1)
    if driver.title == 'Dashboard | Freelancer':
        break

input("Cancel the notifications and press enter")

apply = True
while apply == True:
    try:
        #click the recent jobs icon
        driver.execute_script("document.getElementsByClassName('ButtonElement ng-star-inserted')[16].click()")
        sleep(2)

        #Click on the first job
        driver.execute_script("document.getElementsByClassName('NotificationDetail')[0].click()")
        sleep(5)

        #Get the topic
        pageCode = BeautifulSoup(driver.page_source, "html.parser")
        packageInfo = pageCode.find('fl-bit', {'class': 'ng-star-inserted'})
        topic = packageInfo.find('span', class_='NativeElement Span ng-star-inserted').get_text().strip()


        #Check for the key words in the topic
        sentence = topic
        namesToCheck = ["Website", "website", "seo", "SEO", "Python", "Python","MySQL","Data", "data", "machine", "Forex","forex","Wordpress","wordpress","Autom","autom"]

        checkResult = nameCheck(namesToCheck, sentence)

        if checkResult >= 1:
            #Get the price
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('fl-bit',{'class':'ProjectViewDetails-budget'})
            priceString = info_div.find('div',class_='NativeElement ng-star-inserted').get_text().strip()


            #Extract the first part of the price
            # Define a regular expression pattern to match the currency value
            pattern = r'\$([\d.]+)'
            pattern2 = r'€([\d.]+)'
            # Use re.search to find the first match in the string
            match = re.search(pattern, priceString)
            match2 = re.search(pattern2, priceString)

            # Check if a match is found and extract the value
            if match:
                currency_value = match.group(1)
            elif match2:
                currency_value = match2.group(1)
            else:
                print("No match found.")


            #Get job content
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('fl-bit',{'class':'ProjectDescription'})
            jobContent = info_div.find('span',class_='NativeElement Span ng-star-inserted').get_text().strip()


            # Set your OpenAI GPT-3 API key here
            openai.api_key = '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'

            def chat_with_gpt(prompt):
                # Define the API endpoint
                endpoint = "https://api.openai.com/v1/chat/completions"

                # Prepare the data payload
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }

                try:
                    # Make the API request
                    response = openai.ChatCompletion.create(**data)

                    # Extract and return the assistant's reply
                    choices = response['choices']
                    assistant_reply = choices[0]['message']['content']
                    return assistant_reply

                except Exception as e:
                    print(f"Error: {e}")
                    return None


            # Example usage
            user_prompt = "Please bid for me this job in one paragraph. Write the proposal in about 500 words. Use the pronoun I and not we. Also, do not leave fields for me to fill in (Please do not leave for me fields to fill) and the proposal should be less than 1500 charachters: " + jobContent
            response = chat_with_gpt(user_prompt)

            #Scroll to the bottom to apply
            driver.execute_script("window.scrollTo(0, 700);")
            sleep(3)

            """
            #Add the price
            priceField = driver.find_element(By.XPATH,'/html/body/app-root/app-logged-in-shell/div/fl-container/div/div/app-project-view/app-project-view-logged-in/app-project-view-details/fl-page-layout/main/fl-container/fl-page-layout-single/fl-grid/fl-col[1]/app-project-details-freelancer/app-bid-form/fl-card/div/div[2]/fl-bit[1]/fl-bit[1]/fl-bit[1]/fl-bit[1]/fl-input/div/div/div[2]/input')
            driver.execute_script("document.getElementsByClassName('NativeElement ng-tns-c109-109 ng-valid ng-star-inserted ng-touched ng-dirty')[0].value = ''")
    
            # Remove the decimal point.
            currency_value = currency_value.replace(".", "")
    
            # Remove the last two digits.
            currency_value = currency_value[:-2]
    
            print("The amount is: ",currency_value)
    
            priceField.send_keys(currency_value)
            sleep(3)
            """

            #Add the time
            timeField = driver.find_element(By.XPATH,'/html/body/app-root/app-logged-in-shell/div/fl-container/div/div/app-project-view/app-project-view-logged-in/app-project-view-details/fl-page-layout/main/fl-container/fl-page-layout-single/fl-grid/fl-col[1]/app-project-details-freelancer/app-bid-form/fl-card/div/div[2]/fl-bit[1]/fl-bit[1]/fl-bit[1]/fl-bit[2]/fl-input/div/div/div[1]/input')
            timeField.clear()
            timeField.send_keys('3')
            sleep(3)

            #Add the response
            proposalField = driver.find_element(By.XPATH,'/html/body/app-root/app-logged-in-shell/div/fl-container/div/div/app-project-view/app-project-view-logged-in/app-project-view-details/fl-page-layout/main/fl-container/fl-page-layout-single/fl-grid/fl-col[1]/app-project-details-freelancer/app-bid-form/fl-card/div/div[2]/fl-bit[1]/fl-textarea/textarea')
            proposalField.send_keys(response)
            sleep(3)

            #Scroll to the submit button
            driver.execute_script("window.scrollTo(0, 1650)")
            sleep(2)

            #Click the submit button
            applicationButton = driver.find_element(By.XPATH,'/html/body/app-root/app-logged-in-shell/div/fl-container/div/div/app-project-view/app-project-view-logged-in/app-project-view-details/fl-page-layout/main/fl-container/fl-page-layout-single/fl-grid/fl-col[1]/app-project-details-freelancer/app-bid-form/fl-card/div/div[2]/fl-bit[2]/fl-button/button')
            applicationButton.click()
            sleep(3)

        sleep(20)

    except:
        sleep(20)
        pass

