# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 21:12:57 2017

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


res_pd = pd.read_csv('16092017_3.csv',encoding='utf-8')
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
