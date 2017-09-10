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


base_link = "https://www.immobilienscout24.de/expose/"



link = base_link+str(65107615)
driver.get(link)
sleep(1)    
s = BeautifulSoup(driver.page_source)




# Warmmiete
elements = s.findAll("dd",class_="is24qa-gesamtmiete grid-item three-fifths font-bold")
for element in elements:
    tmp= element.string.encode("utf-8")
    tmp1 = tmp[1:tmp.index('\xe2\x82\xac')-1]   
    WM = float(tmp1.replace(".",""))
    print WM
# Kaltmiete
elements = s.findAll("dd",class_="is24qa-kaltmiete grid-item three-fifths")
for element in elements:
    tmp = element.string.encode("utf-8")
    tmp1 = tmp[1:tmp.index('\xe2\x82\xac')-1]   
    KM = float(tmp1.replace(".",""))
    print KM

# Area
elements = s.findAll("dd",class_="is24qa-wohnflaeche-ca grid-item three-fifths")
for element in elements:
    tmp= element.string.encode("utf-8")
    tmp1 = tmp[1:tmp.index('m')-1] 
    QM=float(tmp1)
    print QM
    
    
# Rooms
elements = s.findAll("dd",class_="is24qa-zimmer grid-item three-fifths")
for element in elements:
    RM = element.string.encode("utf-8")
    RM = RM.replace(' ','')
    RM = float(RM)
# Zip
elements = s.findAll("span",class_="zip-region-and-country")
for element in elements:
    #print element.string.encode("utf-8")
    ZP = int(filter(str.isdigit, element.string.encode("utf-8")))

driver.quit()






