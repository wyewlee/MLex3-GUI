from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import csv
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import demoji as dj
from datetime import datetime
import csv

with open("input.txt", "r") as file:
    lines = file.readlines()
    print('lines: ', end='')
    print(lines)
    handle = lines[0].strip('\n')
    num_post = lines[1].strip('\n')
    num_post =eval(num_post)

browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
global global_csvfilename
directory=r'../csv/'

def loginIG():
    username = '1906837crawler'
    pw = '1906837CRAWLERyewlee'
    
    browser.get('https://www.instagram.com/')
    sleep(5)

    namefield = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    namefield.send_keys(username)

    password = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password.send_keys(pw)

    signin = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
    signin.click()

    sleep(4)

    try:
        popup = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        popup.click()
    except:
        pass

def goToPage(handle):   
    browser.get('https://instagram.com/'+handle)
    
def clickPost(n):
    #many classname same, comment 24+12
    post = browser.find_elements_by_class_name('_9AhH0')
    post[n].click()
    actions = ActionChains(browser)
    sleep(4)

def getOriPost():
    xpath = '/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span'
    oriText = browser.find_element_by_xpath(xpath)
    return oriText.text
    
def getDate():
    xpath = '/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/div/div/time'
    date = browser.find_element_by_xpath(xpath)
    return date.get_attribute("datetime")

def loadMore():
    try:
        selectorpath = 'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > ul:nth-child('+str(12)+') > div > li > div > div.C7I1f > div.C4VMK > span'
        comment = browser.find_element_by_css_selector(selectorpath)
        actions = ActionChains(browser)
        actions.move_to_element(comment).perform()#scroll to bottom    
        loadmorecomment = browser.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > li > div > button > span')
        loadmorecomment.click()
        sleep(1)
    except:
        print("endofpage")
        
def getComments(iter):
    start = 2*iter
    end = 14*iter
    text = []
    for n in range(start,end):
        selectorpath = 'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > ul:nth-child('+str(n)+') > div > li > div > div.C7I1f > div.C4VMK > span'
        comment = browser.find_element_by_css_selector(selectorpath)
        #write
        writeCSV(getDate(),getCurrentURL(),getOriPost(),comment.text)
        #loadmore
        if n %13 == 0:
            loadMore()
    return "done"

def getCurrentURL():
    return browser.current_url


def initCSV(csvfilename):
    csvfile=open(csvfilename, 'w', newline='', encoding='utf-8')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['post_date','post_url','ori_post','comment'])  

def closeCSV(csvfile):
    csvfile.close()    
    
def writeCSV(post_date,post_url,ori_post,comment): #append
    with open (global_csvfilename, 'a+', encoding='utf-8',newline='') as csvfile:
        fnames = ['post_date','post_url','ori_post','comment']
        wr = csv.DictWriter(csvfile, fieldnames=fnames)
        wr.writerow({
            'post_date':post_date,
            'post_url':post_url,
            'ori_post':ori_post,
            'comment':comment
        })

def createCSV():
    global global_csvfilename
    anow = datetime.now()
    adatetime = anow.strftime("%m%d%Y_%H%M%S")
    global_csvfilename = directory+"instagram_"+handle+"_"+adatetime+".csv"
    print (global_csvfilename+" is created.")
    return global_csvfilename
        
#Main
loginIG()
goToPage(handle)
global_csvname = createCSV()
initCSV(global_csvname)

for z in range(0,num_post): #crawl latest 6 postc
    goToPage(handle)
    clickPost(z)
    for x in range(0,6): #crawl 20 iteration, 20x11
        getComments(x)
        print("done"+str(x))
 

print("All Done! Crawled 6 post, 20 iteration each post. ")
    