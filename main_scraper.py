# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:43:31 2016

@author: Moh2
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import math
import re
import csv

print "Started..."
#link = "http://www.momondo.de/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=MUC&SD0=LCA&SDP0=11-08-2016&SO1=LCA&SD1=MUC&SDP1=18-08-2016&AD=1&TK=ECO&DO=false&NA=false"
tot_res = 1096.0
tot_pages = int(math.ceil(tot_res/20.0))

pg = 1
min_room =1
max_rent = 10000
min_area = 40
link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"


print "Creating driver..."
driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
sleep(2)

print "Setting window size..."
driver.set_window_size(1120,550)
print "Collecting expose IDs.."

apt_ids = []
pg = 1
while pg<(tot_pages+1):
        
    link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"
    driver.get(link)
    sleep(2)
    s = BeautifulSoup(driver.page_source)
    print 'Page : '+str(pg)    
    elements = s.findAll("a",class_="result-list-entry__brand-title-container")
    res_ID = 1    
    for element in elements:
            print 'Result num '+str(res_ID)
            if element.has_attr('data-go-to-expose-id'):
                tmp = element['data-go-to-expose-id'].encode("utf-8")
                apt_ids.append(tmp)
                res_ID = res_ID+1
    pg = pg+1    
    
#print apt_ids


with open("IDs_"+"100917"+".csv",'wb') as resultFile:
    wr = csv.writer(resultFile)
    wr.writerows(apt_ids)

base_link = "https://www.immobilienscout24.de/expose/"

apt_i = 1

while apt_i<len(apt_ids)+1:
    
    link = base_link + apt_ids[apt_i]
    driver.get(link)
    sleep(1)    
    s = BeautifulSoup(driver.page_source)
    
    

    apt_i=apt_i+1    
    
    








if False:
    print "Finished waiting"
    
    base_link = "https://www.immobilienscout24.de/expose/"
    
    
    
    
    
    elements = s.findAll("h1",class_="font-ellipsis font-l font-light font-line-s margin-bottom-none")
    
    for element in elements:
    #    content = element.findNext("span",class_="font-normal")
        content = element.findNext("span")
        print content.string.encode('utf-8')
        
        #print content.string.encode('utf-8')
    
    elements = s.findAll("a",class_="result-list-entry__brand-title-container")
    for element in elements:
            tmp = element['data-go-to-expose-id'].encode("utf-8")
            print tmp
    
    if False:
        r = re.compile(r'height:\s\d+\.*\d*%;')
        elements = s.findAll("div",style=r)
        hlth =[]
        prices=[]
        dates = []
        for element in elements:
            tmp = element['style'].encode("utf-8")
            if tmp:
                kw="%"
                loc = tmp.find(kw)
                tmp = tmp[8:loc]
                hlth.append(tmp)
                dt = element.findNext("span",class_="date")
                if dt:
                    dates.append(dt.string.encode('utf-8'))
                prc = element.findNext("span",class_="price")
                if prc:
                    tmp = prc.string.encode('utf-8')
                    tmp = tmp[3:len(tmp)]
                    prices.append(int(tmp))
        
        print "Grabbing prices"
        elements = s.findAll("span",class_="value")
        if elements:
            prcs = []
            for element in elements:
                if (len(element.attrs)<2 and element.findParent('div',class_='price-pax')):
                    prcs.append(element.string.encode('utf-8'))            
        else:
            print "No prices found"
        
        
        print "Grabbing airports"
        elements = s.findAll("span",class_="iata")
        if elements:
            arps = []
            for element in elements:
                if (len(element.attrs)<2):
                    arps.append(element.string.encode('utf-8'))            
        else:
            print "No airports found"
        
        
        print "Grabbing airlines"
        elements = s.findAll("div",class_="names")
        if elements:
            als = []
            for element in elements:
                if (len(element.attrs)<2):
                    als.append(element.string.encode('utf-8'))            
        else:
            print "No airlines found"
        
        
        print "Grabbing travel times"
        elements = s.findAll("div",class_="travel-time")
        if elements:
            travel_times = []
            for element in elements:
                if (len(element.attrs)<2):
                    travel_times.append(element.string.encode('utf-8'))            
        else:
            print "No travel times found"
        
        
        sleep(1.1)
        #next_page_elem = driver.find_element_by_xpath('//*[@id="results-tickets"]/div[2]div[2]div/ul/li[6]')
        next_page_elem = driver.find_element_by_xpath('//*[@id="results-tickets"]/div[2]/div[2]/div/ul/li[6]')
        next_page_elem.click()
        sleep(0.5)
        driver.save_screenshot('pg2.png')



driver.quit()










