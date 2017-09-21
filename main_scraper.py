# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:21:33 2017

@author: m00760171
"""

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



print("Started...")
#link = "http://www.momondo.de/flightsearch/?Search=true&TripType=2&SegNo=2&SO0=MUC&SD0=LCA&SDP0=11-08-2016&SO1=LCA&SD1=MUC&SDP1=18-08-2016&AD=1&TK=ECO&DO=false&NA=false"
tot_res = 1096.0
tot_pages = int(math.ceil(tot_res/20.0))


tot_pages = 53
pg = 1
min_room =1
max_rent = 10000
min_area = 40
link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"


print("Creating driver...")
driver = webdriver.PhantomJS(executable_path='C:/Users/m00760171/Desktop/DUS/phantomjs-2.1.1-windows/bin/phantomjs.exe')
sleep(2)


#driver.set_window_size(1120,550)
print("Collecting expose IDs..")

apt_ids = []
pg = 1
while pg<(tot_pages+1):
        
    link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"
    driver.get(link)
    #sleep(2)
    s = BeautifulSoup(driver.page_source)
    print('Page : '+str(pg))    
    elements = s.findAll("a",class_="result-list-entry__brand-title-container")
    res_ID = 1    
    for element in elements:
            print('Result num '+str(res_ID))
            if element.has_attr('data-go-to-expose-id'):
                tmp = element['data-go-to-expose-id'].encode("utf-8")
                apt_ids.append(int(tmp))
                res_ID = res_ID+1
    pg = pg+1    
    

base_link = "https://www.immobilienscout24.de/expose/"
apt_i = 1
pr_list = []
qm_list = []
rm_list = []
zp_list = []

while apt_i<len(apt_ids)+1:
#while apt_i <11:    
    if (apt_i%10)==0:
        print("Item "+str(apt_i)+" of "+str(len(apt_ids)))
    
    link = base_link + str(apt_ids[apt_i-1])
    driver.get(link)
    #sleep(1)    
    s = BeautifulSoup(driver.page_source)

    # Getting price
    #dd class="is24qa-gesamtmiete grid-item three-fifths font-bold"    
    elements = s.findAll("dd", class_="is24qa-gesamtmiete grid-item three-fifths font-bold")
    pr_found=False
    
    for element in elements:
        curr_pr = element.string
        pr_found = len(curr_pr)>0
        
        break
    
    # Getting qm
    #<div class="is24qa-flaeche is24-value font-semibold"> 95,1 m² </div>  
    elements = s.findAll("div", class_="is24qa-flaeche is24-value font-semibold")
    qm_found=False    
    for element in elements:
        curr_qm = element.string
        qm_found = len(curr_qm)>0

        
        break
        
    # Getting room count
    #<div class="is24qa-zi is24-value font-semibold"> 2 </div>
    elements = s.findAll("div", class_="is24qa-zi is24-value font-semibold")
    rm_found=False
    for element in elements:
        curr_rm = element.string
        rm_found = len(curr_rm)>0

        
        break

    # Getting zip code
    #<span class="zip-region-and-country"> 40213 Düsseldorf</span>
    elements = s.findAll("span", class_="zip-region-and-country")
    zp_found=False
    for element in elements:
        curr_zp = element.string
        zp_found = len(curr_zp)>0

        
        break


    if pr_found and qm_found and zp_found and rm_found:
        pr_list.append((apt_ids[apt_i-1],curr_pr))
        qm_list.append((apt_ids[apt_i-1],curr_qm))
        rm_list.append((apt_ids[apt_i-1],curr_rm))
        zp_list.append((apt_ids[apt_i-1],curr_zp))
    else:
        print(str(apt_i))
        del apt_ids[apt_i-1]

    apt_i=apt_i+1    

zp_dict = dict(zp_list)
pr_dict = dict(pr_list)
rm_dict = dict(rm_list)
qm_dict = dict(qm_list)


comb_list = [(k, zp_dict[k], pr_dict[k], rm_dict[k], qm_dict[k]) for k in sorted(zp_dict)]
res_pd = pd.DataFrame(comb_list)
res_pd.columns = ['ID','PLZ','Price','Room count','Square meter']


res_pd.to_csv('20092017_pack.csv', header=True, index=False, encoding='utf-8')
