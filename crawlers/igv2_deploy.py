from time import sleep
from selenium import webdriver
import json
import re
import pandas as pd
from datetime import datetime
import csv
from os.path import join

global code_list
global handle
global json
global driverPath
driverPath = join('..','assets','dependency','chromedriver.exe')
browser = webdriver.Chrome(executable_path=driverPath)
directory = join('..','assets','csv','')
global_csvname = ''
global global_csvfilename

with open('input.txt', "r") as file:
    lines = file.readlines()
    print('lines: ', end='')
    print(lines)
    keyword = lines[0].strip('\n')
    num_post = lines[1].strip('\n')
    num_post =eval(num_post)

def login():

    username = '1906837crawler'
    pw = '1906837'

    browser.get('https://www.instagram.com/')
    sleep(5)

    namefield = browser.find_element_by_xpath(
        '//*[@id="loginForm"]/div/div[1]/div/label/input')
    namefield.send_keys(username)

    password = browser.find_element_by_xpath(
        '//*[@id="loginForm"]/div/div[2]/div/label/input')
    password.send_keys(pw)

    signin = browser.find_element_by_xpath(
        '//*[@id="loginForm"]/div/div[3]/button/div')
    signin.click()

    sleep(4)

    try:
        popup = browser.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]')
        popup.click()
    except:
        pass


def getShortCode(handle,n):

    browser.get('https://www.instagram.com/'+handle+'/?__a=1')

    resp = browser.find_element_by_tag_name('body').text

    code_list = re.findall(r"\"shortcode\":\"(.*?)\",", resp)

    return code_list[n]


def getComments(code_list):
    text_list = list()
    counter = 0
    for code in code_list:
        counter += 1
        print("done" + str(counter) + ", " + str(len(code_list)) + " Maximum runs.")
        browser.get('https://www.instagram.com/p/'+code+'/?__a=1')
        try:
            pageJSON = json.loads(
                browser.find_element_by_tag_name('body').text)
            edges = pageJSON['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
        except:
            print("Fail to load " + code + " reloading to next page.")
            continue

        for node in edges:
            text_list = re.findall(r"'text': '(.*?)',", str(node))

            for text in text_list:
                writeCSV(text)
        # sleep(3)


def initCSV(csvfilename):
    csvfile = open(csvfilename, 'w', newline='', encoding='utf-8')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['comment'])


def closeCSV(csvfile):
    csvfile.close()


def writeCSV(comment):  # append
    with open(global_csvfilename, 'a+', encoding='utf-8', newline='') as csvfile:
        fnames = ['comment']
        wr = csv.DictWriter(csvfile, fieldnames=fnames)
        wr.writerow({
            'comment': comment
        })


def createCSV():
    global global_csvfilename
    anow = datetime.now()
    adatetime = anow.strftime("%m%d%Y_%H%M%S")
    global_csvfilename = directory+"instagram_"+handle+"_"+adatetime+".csv"
    print(global_csvfilename+" is created.")
    return global_csvfilename


login()
# handle = setHandle()
handle = keyword
global_csvname = createCSV()
initCSV(global_csvname)
code_list = getShortCode(handle,num_post)
getComments(code_list)

print("Done Crawled.")
