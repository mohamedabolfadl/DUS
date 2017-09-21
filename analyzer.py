# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 21:12:57 2017
@author: Moh2
"""
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import pandas as pd

import math
import re
import csv
import numpy as np

import matplotlib.pyplot as plt



def clean_price(inp):
    #x = inp.encode("utf-8")
    x = inp
    x = x.replace(" ","")
    #x = x.replace('\xe2\x82\xac','')
    x = x.replace('€','')
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
    #x = x.encode("utf-8")
    x = x.replace('m','')
#    x = x.replace('\xc2\xb2','')
    x = x.replace('²','')

    
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

def make_string(inp):
    return str(inp)+" Germany"

res_pd = pd.read_csv('16092017_3.csv',encoding='utf-8')
#res_pd = pd.read_csv('16092017_3.csv')

w_pd = res_pd

#a = w_pd['Price'].iloc[0]

w_pd['Price_i'] = w_pd['Price'].map(clean_price)
w_pd['PLZ'] = w_pd['PLZ'].map(clean_zp)
w_pd['Room_count'] = w_pd['Room count'].map(clean_rm)
w_pd['Square_meter'] = w_pd['Square meter'].map(clean_qm)
w_pd['Country'] = ' Germany'
#w_pd['City'] = ' Dusseldorf'
#w_pd['Full_address'] = w_pd['PLZ'].map(make_string)
#w_pd['Full_address'] = str(w_pd['PLZ']) + w_pd['City'] + w_pd['Country']




w_pd.to_csv('16092017_3_i.csv', header=True, index=False, encoding='utf-8')

# Full rent
pure_pd =w_pd[~w_pd['Price'].str.contains('eben')]
pure_pd =pure_pd [~pure_pd['Price'].str.contains('eiz')]

# Missing heat and negelectinf those without nebenkosten
missing_heating_pd = w_pd[w_pd['Price'].str.contains('eiz')]
missing_heating_pd = missing_heating_pd[~missing_heating_pd['Price'].str.contains('eben')]

# Adding heat
heat_factor = 0.9
missing_heating_pd['Price_i'] = missing_heating_pd['Price_i'] + heat_factor*missing_heating_pd['Square_meter']

# Concatenating with and without heating
full_pd = pd.concat([pure_pd,missing_heating_pd])

full_pd.to_csv('out.csv', header=True, index=False, encoding='utf-8')

# Preliminary plot of area vs Price
plt.scatter(list(full_pd['Square_meter']), list(full_pd['Price_i']))
plt.show()


