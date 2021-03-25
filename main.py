import urllib
import null
import urllib3
import selenium
import enum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests as requests
import pickle
import os
import sys
import getpass
import re
import time
import glob
import openpyxl
from random import randint
import xlrd

def ExcelFileReader(MasterCardinput):
    #df = pd.read_excel("/home/shobhit/Desktop/excel/MasterCardData_Priscilla_04021019.xlsx", skiprows=1)
    print(MasterCardinput)
    df = pd.read_excel(MasterCardinput, skiprows=1)
    print("number of records to be processed",len(df))
    return df

def FileRename(frompath, topath, Prefix, Suffix, rename):
    all_files = os.listdir(frompath)
    for filename in all_files:
        if (str(filename).startswith(Prefix) and str(filename).endswith(Suffix)):
            old_file = frompath + filename
            print(old_file)
            new_file = topath + rename +"." +Suffix
            print(new_file)
            os.rename(old_file, new_file)
            print("FileRename successfully")

# defining urls and global variables
MASTER_CARD_LOGIN_PAGE = "https://www.mastercardconnect.com/business/public/en-us/public/signin.html"
MERCHANT_PORTAL_LOGIN_PAGE = "https://prodejomsportal.rjil.ril.com//ejoms/#nogo"
MERCHANT_PORTAL_MAIN_PAGE = "https://prodejomsportal.rjil.ril.com//ejoms/"
MASTERCARD_PORTAL_MAIN_PAGE = "https://www.mastercardconnect.com/business/secured/en-us/cmscommon/home.html"
MASTERCARD_PORTAL_AGREEMENT_PAGE = "https://www.mastercardconnect.com/match/start.html"
MASTERCARD_PORTAL_START_PAGE = "https://www.mastercardconnect.com/jct_matchprod_content/MatchUI/Action?operation=gotoPage&pageName=startPage"
MASTERCARD_PORTAL_INQUIRY_PAGE = "https://www.mastercardconnect.com/jct_matchprd_content/match/Action?pageName=inqPage&operation=gotoPage&page=1&next=1&LUWciyfnDBt-UQydAmPENPvj=104139249582830325"

chrome_path=os.getcwd() + '/chromedriver'
print(chrome_path)
DRIVER_PATH = os.getcwd()
MASTER_CARD_LOGIN_PAGE = "https://www.mastercardconnect.com/business/public/en-us/public/signin.html"
wd = webdriver.Chrome(executable_path=chrome_path)

class MasterCardBusinessDataXPath():
    # Sets the hardcoded XPATH Variables
    userName = wd.find_elements_by_xpath("//*[@id=\"userid\"]")
    password = wd.find_elements_by_xpath("/html/body/div[1]/div[1]/section/div/div[4]/div/div[1]/div[1]/div/div/div/signin/form/div[2]/div[2]/input")
    cookiesAgreement = wd.find_elements_by_xpath("//*[@id=\"_ghostery-accept-button\"]")
    loginButton = wd.find_elements_by_xpath("//*[@id=\"btnSubmit\"]")
    matchButton = wd.find_elements_by_xpath("//*[@id =\"vCard-match\"]/p/span[1]")
    moreOption = wd.find_elements_by_xpath("//*[@id=\"more-option-\"]")
    agreementButton = wd.find_elements_by_xpath("//*[@id=\"Content\"]/div/table/tbody/tr/td[1]/div/table/tbody/tr/td[2]/div")
    generalOperation = wd.find_elements_by_xpath("//*[@id=\"refresh\"]/div[5]/div[2]")
    inquiry = wd.find_elements_by_xpath("//*[@id=\"refresh\"]/div[6]/div[3]")
    acquirerId = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[1]/td[3]/input")
    merchantName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[2]/td[3]/input")
    doingBusinessAs = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[3]/td[3]/input")
    businessAddressLine1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[4]/td[3]/input")
    businessAddressLine2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[5]/td[3]/input")
    city = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[6]/td[3]/input")
    country = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[8]/td[3]/input")
    postalCode = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[9]/td[3]/input")
    phoneNumber = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[10]/td[3]/table/tbody/tr/td[1]/input")
    nextButton = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr/td[1]/div/table/tbody/tr/td[2]/div")
    urlDataNextButton = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[2]/div/table/tbody/tr/td[2]/div")
    lastName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[3]/input")
    firstName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/input")
    address1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[3]/input")
    adress2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[4]/td[3]/input")
    checkbox = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[2]/tbody/tr[1]/td[9]/input")
    exportfile = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/div/table/tbody/tr/td[2]/div")

class MerchantProfileDataXPath():
    # Sets the Merchant XPATHs
    userName = wd.find_elements_by_xpath("//*[@id=\"user_name\"]")
    password = wd.find_elements_by_xpath("//*[@id=\"pwd\"]")
    login = wd.find_elements_by_xpath("/html/body/div/div[1]/div/div[1]/a/span")
    search = wd.find_elements_by_xpath("/html/body/div[1]/div[1]/div/div/div[1]/div/div[1]/div")
    search_mid = wd.find_elements_by_xpath("//*[@id=\"mid\"]")
    mid_search_button = wd.find_elements_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/button")
    mid_click = wd.find_elements_by_xpath("/html/body/div[1]/div[1]/div/div[3]/div[1]/table/tbody/tr[2]/td[2]/a")
    lastName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[3]/input")
    firstName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/input")
    address1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[3]/input")
    adress2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[4]/td[3]/input")
    city = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[5]/td[3]/input")
    country = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[7]/td[3]/input")
    postalCode = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[8]/td[3]/input")
    phoneNumber = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[9]/td[3]/table/tbody/tr/td[1]/input")

class MasterCardProfileDataXPath():
    lastName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[3]/input")
    firstName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/input")
    address1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[3]/input")
    address2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[4]/td[3]/input")
    city = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[5]/td[3]/input")
    country = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[7]/td[3]/input")
    postalCode = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[8]/td[3]/input")
    phoneNumber = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[9]/td[3]/table/tbody/tr/td[1]/input")
    nextProfileButton = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/div")
    dropDownSelect = wd.find_elements_by_xpath("//*[@id=\"mainContent\"]/table[1]/tbody/tr[14]/td[2]/select/option[1]")
    submitButton = wd.find_elements_by_xpath("//*[@id=\"mainContent\"]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/div")
    warningPopupButton = wd.find_elements_by_xpath("/html/body/form/table/tbody/tr[3]/td[1]/table/tbody/tr/td[2]/div")
    possibleMatchesView = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[1]/div/table/tbody/tr/td[2]/div")
    possibleMatchesView1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[5]/td[1]/div/table/tbody/tr/td[2]/div")
    checkBox = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[2]/tbody/tr[1]/td[9]/input")
    exportfile = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/div/table/tbody/tr/td[2]/div")

def main():
    exceldata = ExcelFileReader(sys.argv[1])
    wd.get(MASTER_CARD_LOGIN_PAGE)
    time.sleep(50)
    isFirstTime = True
      # dataframe
    print("excel file executed", len(exceldata))
    if True:
        # Match button processing
        matchButton = wd.find_elements_by_xpath("//*[@id=\"vCard-match\"]")  # ("//*[@id=\"vCard-match\"]/button[2]/i")
        for element in matchButton:
            element.click()
        print("1. match button over")
        pickle.dump(wd.get_cookies(), open("cookies.pkl", "wb"))
        time.sleep(5)
        # Agreement button processing
        agreementButton = wd.find_elements_by_xpath("//*[@id=\"Content\"]/div/table/tbody/tr/td[1]/div/table/tbody/tr/td[2]/div")
        for element in agreementButton:
            element.click()
        print("2.agreement button over")
        time.sleep(5)
        chwd = wd.window_handles
        for w in chwd:
            wd.switch_to.window(w)
        wd.get(MASTERCARD_PORTAL_START_PAGE)

        for index, row in exceldata.iterrows():
            print(row)
            columnsList = list(exceldata.iloc[index, :])  # row.to_list()
            print(columnsList)
             # processing general option button
            generalOperation = wd.find_elements_by_xpath("//*[@id=\"refresh\"]/div[5]/div[2]")
            for element in generalOperation:
                element.click()
            print("3. General operation button")
            # processing inquiry button
            time.sleep(5)
            inq = wd.find_elements_by_xpath("//*[@id=\"refresh\"]/div[6]/div[3]")
            for element in inq:
                element.click()
            print("4. Enquiry  operation button")
            #Processing filling the Merchant data
            acquirerId = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[1]/td[3]/input")
            for element in acquirerId:
                element.send_keys((columnsList[1]).astype(tuple))
                #print(acquirerId)
            merchantName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[2]/td[3]/input")
            for element in merchantName:
                element.send_keys(columnsList[2])
                #print(merchantName)
            doingBusinessAs = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[3]/td[3]/input")
            for element in doingBusinessAs:
                element.send_keys(columnsList[3])
                #print(doingBusinessAs)
            businessAddressLine1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[4]/td[3]/input")
            for element in businessAddressLine1:
                element.send_keys(columnsList[4])
                #print(businessAddressLine1)
            businessAddressLine2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[5]/td[3]/input")
            for element in businessAddressLine2:
                element.send_keys(columnsList[5])
               # print(businessAddressLine2)
            city = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[6]/td[3]/input")
            for element in city:
                element.send_keys(columnsList[6])
                #print(city)
            country = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[8]/td[3]/input")
            for element in country:
                element.send_keys(columnsList[7])
                #print(country)
            postalCode = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[9]/td[3]/input")
            for element in postalCode:
                element.send_keys(columnsList[8].astype(tuple))
                #print(postalCode)
            phoneNumber = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[1]/tbody/tr[10]/td[3]/table/tbody/tr/td[1]/input")
            for element in phoneNumber:
                element.send_keys(columnsList[9].astype(tuple))
                #print(phoneNumber)
            nextButton = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr/td[1]/div/table/tbody/tr/td[2]/div")
            for element in nextButton:
                element.click()
                #print(nextButton)
            print("5 Next Button click")
            time.sleep(5)
            urlDataNextButton = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[2]/div/table/tbody/tr/td[2]/div")
            for element in urlDataNextButton:
                element.click()
            #print(urlDataNextButton)
            time.sleep(5)
            lastName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[1]/td[3]/input")
            for element in lastName:
                element.send_keys(columnsList[10])
                #print(lastName)
            firstName = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/input")
            for element in firstName:
                element.send_keys(columnsList[11])
                #print(firstName)
            address1 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[3]/input")
            for element in address1:
                element.send_keys(columnsList[12])
                #print(address1)
            address2 = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[4]/td[3]/input")
            for element in address2:
                element.send_keys(columnsList[13])
                #print(address2)
            city = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[5]/td[3]/input")
            for element in city:
                element.send_keys(columnsList[14])
                #print(city)
            country = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[7]/td[3]/input")
            for element in country:
                element.send_keys(columnsList[15])
               #print(country)
            postalCode = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[8]/td[3]/input")
            for element in postalCode:
                element.send_keys(columnsList[16].astype(tuple))
                #print(postalCode)
            phoneNumber = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[9]/td[3]/table/tbody/tr/td[1]/input")
            for element in phoneNumber:
                element.send_keys(columnsList[17].astype(tuple))
                #print(phoneNumber)
            nextProfileButton = wd.find_elements_by_xpath(
                "//*[@id=\"PageBody\"]/table[3]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/div")
            for element in nextProfileButton:
                element.click()
                #print(nextProfileButton)
            dropDownSelect = wd.find_elements_by_xpath("//*[@id=\"mainContent\"]/table[1]/tbody/tr[14]/td[2]/select/option[1]")
            for element in dropDownSelect:
                element.click()
                #print(dropDownSelect)
            print("6. dropDownSelect ok")
            submitButton = wd.find_elements_by_xpath("//*[@id=\"mainContent\"]/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/div")
            for element in submitButton:
                element.click()
                #print(submitButton)
            print("7.submit_Button_done")
            time.sleep(20)

            new_window = wd.window_handles
            if (len(new_window) == 3):
                time.sleep(20)

            warningPopupButton = wd.find_elements_by_xpath("/html/body/form/table/tbody/tr[3]/td[1]/table/tbody/tr/td[2]/div")
            for element in warningPopupButton:
                element.click()
                #print(warningPopupButton)

                chwd = wd.window_handles
                for w in chwd:
                    wd.switch_to.window(w)

            print("8.Warning button done")
            time.sleep(5)
            possibleMatchesView = wd.find_elements_by_xpath("//*[@id=\"PageBody\"]/table[2]/tbody/tr[3]/td[1]/div/table/tbody/tr/td[2]/div")
            for element in possibleMatchesView:
                element.click()
                #print(possibleMatchesView)
            print("9.Possible_match_view_done")
            time.sleep(5)
            checkBox = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[2]/tbody/tr[1]/td[9]/input")
            for element in checkBox:
                element.click()
                #print(checkBox)
                exportfile = wd.find_elements_by_xpath("//*[@id=\"PageContent\"]/form/table[1]/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/div/table/tbody/tr/td[2]/div")
                for element in exportfile:
                    element.click()
                #print(exportfile)
            print("10.export file done")
            time.sleep(5)
            file1 = (sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], (str(columnsList[0]).rstrip()))
            print(file1)
            FileRename(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], (str(columnsList[0]).rstrip()))
            print("11.rename file done")

    chwd = wd.window_handles
    for w in chwd:
        wd.switch_to.window(w)
    wd.get(MASTERCARD_PORTAL_START_PAGE)

    time.sleep(10)

if __name__ == "__main__":
    main()
