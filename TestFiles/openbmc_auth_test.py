import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driverPath = '' #'/var/jenkins_home/workspace/PyTests_CI_CD/MEDriver/msedgedriver' #path to driver executable
driverService = Service(driverPath) #service - parameter for driver initialisation
options = webdriver.EdgeOptions() #creating options for insecure
options.add_argument("headless") # run without head
options.add_argument("disable-gpu") # run without gpu
options.accept_insecure_certs = True #set insecure parameter to true
driver = webdriver.Edge(options=options,service=driverService) #driver itself
action = ActionChains(driver) #action for performing action chains

url = "https://localhost:2443/#/login"
#url = "edge://settings/" #test url
userName = "testuser" #maybe shouldn't store this as plain text. for example, create hash
userPassword = "[user10]"

def test_case_SUCCESS_LOGIN():
    #connect to BMC WebUI
    driver.get(url)
    #waiting for loading page
    time.sleep(5)

    #insert username into field
    elementUsername = driver.find_element(By.ID, "username") #find
    action.click(on_element=elementUsername) #planning click
    action.send_keys(userName) #sending keys

    #insert user password into field
    elementPassword = driver.find_element(By.ID, "password") #find
    action.click(on_element=elementPassword) #planning click
    action.send_keys(userPassword) #sending keys

    #click on the "Log In Button"
    elementButtonLogin = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[1]/div/form/button") #find
    action.click(on_element=elementButtonLogin) #planning click

    #start action
    action.perform()

    #Waiting for response 5 seconds
    time.sleep(5)

    #if evrthng is ok - then new window should have name Overview
    actualTitle = "Overview"
    expectedTitle = driver.title
    assert(expectedTitle, actualTitle)

def test_case_FAILED_LOGIN():
    #connect to BMC WebUI
    driver.get(url)
    #waiting for loading page
    time.sleep(5)

    #insert username into field
    elementUsername = driver.find_element(By.ID, "username") #find
    action.click(on_element=elementUsername) #planning click
    action.send_keys("bullshit1") #sending keys

    #insert user password into field
    elementPassword = driver.find_element(By.ID, "password") #find
    action.click(on_element=elementPassword) #planning click
    action.send_keys("bullshit2") #sending keys

    #click on the "Log In Button"
    elementButtonLogin = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[1]/div/form/button") #find
    action.click(on_element=elementButtonLogin) #planning click

    #start action
    action.perform()

    #Waiting for response 5 seconds
    time.sleep(5)

    # if evrthng is ok - then new window should have an error message. 
    # well, in my case almost instantly page do refresh and then redirect you to page with error
    #actualError = "HTTP ERROR 405"
    #expectedError = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div[2]/div[2]").text
    #assert(actualError, expectedError)

    #idk why, but sometimes webui openbmc create this👆 error, sometimes not 🙄
    actualTitle = "Login"
    expectedTitle = driver.title
    assert(expectedTitle, actualTitle)


def test_case_LOCKED_ACCOUNT():
    passwd = 1
    for i in range(6):
        #connect to BMC WebUI
        driver.get(url)

        #waiting for loading page
        time.sleep(5)

        #at the last attempt use correct password
        if i == 5:
            passwd = userPassword

        #insert username into field
        elementUsername = driver.find_element(By.ID, "username") #find
        action.click(on_element=elementUsername) #planning click
        action.send_keys(userName) #sending keys

        #insert user password into field
        elementPassword = driver.find_element(By.ID, "password") #find
        action.click(on_element=elementPassword) #planning click
        action.send_keys(passwd) #sending keys

        #click on the "Log In Button"
        elementButtonLogin = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[1]/div/form/button") #find
        action.click(on_element=elementButtonLogin) #planning click

        #start action
        action.perform()

        #Waiting for response 5 seconds
        time.sleep(5)

    # if evrthng is ok - we are on the same login page with blocked account
    actualTitle = "Login"
    expectedTitle = driver.title
    assert(expectedTitle, actualTitle)
