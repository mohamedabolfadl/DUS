# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:43:31 2016

@author: Moh2
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import pandas as pd
import math
import re
import csv



def clean_price(inp):
    x = inp.replace(' ','')
    x = x.encode("utf-8")
    x = x.replace('\xe2\x82\xac','')
    x = x.replace('.','')

    if '(' in x:
        ind = x.find('(')
        x=x[:ind]

    
    if ',' in x:
        ind = x.find(',')
        x=x[:ind]
        
    return int(x)

def clean_qm(inp):
    x = inp.replace(' ','')
    x = x.encode("utf-8")
    x = x.replace('m','')
    x = x.replace('\xc2\xb2','')
    x = x.replace('.','')
    if ',' in x:
        ind = x.find(',')
        x=x[:ind]
        
    return int(x)

def clean_rm(inp):
    x = inp.replace(' ','')
    x = inp.replace(',','.')
    x = x.encode("utf-8")
    return float(x)


def clean_zp(inp):
    x = inp.replace(' ','')
    x = x.encode("utf-8")
    return int(x[0:5])



print "Started..."
#link = "http://www.momondo.de/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=MUC&SD0=LCA&SDP0=11-08-2016&SO1=LCA&SD1=MUC&SDP1=18-08-2016&AD=1&TK=ECO&DO=false&NA=false"
tot_res = 1096.0
tot_pages = int(math.ceil(tot_res/20.0))


tot_pages = 53
pg = 1
min_room =1
max_rent = 10000
min_area = 40
link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"


print "Creating driver..."
driver = webdriver.PhantomJS(executable_path='C:/Users/Moh2/Desktop/scraping/phantomjs-2.1.1-windows/bin/phantomjs.exe')
sleep(2)

print "Setting window size..."
#driver.set_window_size(1120,550)
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
                apt_ids.append(int(tmp))
                res_ID = res_ID+1
    pg = pg+1    
    
#print apt_ids


with open("IDs_"+"100917"+".csv",'wb') as resultFile:
    wr = csv.writer(resultFile)
    wr.writerows(zip(apt_ids))

base_link = "https://www.immobilienscout24.de/expose/"
apt_i = 1
pr_list = []
qm_list = []
rm_list = []
zp_list = []
while apt_i<len(apt_ids)+1:
#while apt_i <11:    
    if (apt_i%10)==0:
        print "Item "+str(apt_i)+" of "+str(len(apt_ids))
    
    link = base_link + str(apt_ids[apt_i-1])
    driver.get(link)
    sleep(1)    
    s = BeautifulSoup(driver.page_source)

    # Getting price
    #dd class="is24qa-gesamtmiete grid-item three-fifths font-bold"    
    elements = s.findAll("dd", class_="is24qa-gesamtmiete grid-item three-fifths font-bold")
    for element in elements:
        pr_list.append(element.string)
        break
    
    # Getting qm
    #<div class="is24qa-flaeche is24-value font-semibold"> 95,1 m² </div>  
    elements = s.findAll("div", class_="is24qa-flaeche is24-value font-semibold")
    for element in elements:
        qm_list.append(element.string)
        break
        
    # Getting room count
    #<div class="is24qa-zi is24-value font-semibold"> 2 </div>
    elements = s.findAll("div", class_="is24qa-zi is24-value font-semibold")
    for element in elements:
        rm_list.append(element.string)
        break

    # Getting zip code
    #<span class="zip-region-and-country"> 40213 Düsseldorf</span>
    elements = s.findAll("span", class_="zip-region-and-country")
    for element in elements:
        zp_list.append(element.string)
        break





    apt_i=apt_i+1    


res_mat = np.column_stack((apt_ids,zp_list,pr_list, rm_list, qm_list))
res_pd = pd.DataFrame(res_mat)
res_pd.columns = ['ID','PLZ','Price','Room count','Square meter']

res_pd.to_csv('16092017_3.csv', header=True, index=False, encoding='utf-8')

w_pd = res_pd
w_pd['Price_i'] = w_pd['Price'].map(clean_price)
w_pd['PLZ'] = w_pd['PLZ'].map(clean_zp)
w_pd['Room count'] = w_pd['Room count'].map(clean_rm)
w_pd['Square meter'] = w_pd['Square meter'].map(clean_qm)

w_pd.to_csv('16092017_3_i.csv', header=True, index=False, encoding='utf-8')
missing_heating_pd = w_pd[w_pd['Price'].str.contains('eiz')]
missing_neben_pd = w_pd[w_pd['Price'].str.contains('eben')]

missing_heating_neben_pd = w_pd[w_pd['Price'].str.contains('&')]

heat_factor = 0.9
missing_heating_pd['Price_i'] = missing_heating_pd['Price_i'] + heat_factor*missing_heating_pd['Square meter']



driver.quit()

















