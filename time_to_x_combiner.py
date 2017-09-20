# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 17:06:06 2017

@author: m00760171
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

plz_ref = pd.read_csv('PLZ_ref.csv',encoding='utf-8')
plz_dict = plz_ref.set_index('PLZ').to_dict()


def get_cc_time(inp):
    if inp in list(plz_dict['d_cc']):
        return plz_dict['d_cc'][inp]
    else:
        return 9999
    
    

def get_air_time(inp):
    if inp in list(plz_dict['d_a']):
        return plz_dict['d_a'][inp]
    else:
        return 9999
    

def get_wor_time(inp):
    if inp in list(plz_dict['d_w']):
        return plz_dict['d_w'][inp]
    else:
        return 9999


def get_pr_per_qm(inp):
    return float(inp[5])/float(inp[7])    
    
    
full_pd = pd.read_csv('out.csv',encoding='utf-8')

full_pd['d_cc'] = full_pd['PLZ'].map(get_cc_time)
full_pd['d_a'] = full_pd['PLZ'].map(get_air_time)
full_pd['d_w'] = full_pd['PLZ'].map(get_wor_time)


full_pd_filt= full_pd[ full_pd['d_w'] <100  ]

full_pd_filt['pr_qm']=full_pd_filt.apply(get_pr_per_qm,axis=1)
full_pd_filt=full_pd_filt.drop("Price", axis=1)
full_pd_filt=full_pd_filt.drop('Room count', axis=1)
full_pd_filt=full_pd_filt.drop('Square meter', axis=1)
full_pd_filt=full_pd_filt.drop('Country', axis=1)

full_pd_filt.to_csv('train_ID.csv', header=True, index=False, encoding='utf-8')



clean_df = pd.DataFrame()
clean_df['qm']=full_pd_filt['Square_meter']
clean_df['rm']=full_pd_filt['Room_count']
clean_df['cc']=full_pd_filt['d_cc']
clean_df['pm']=full_pd_filt['pr_qm']
clean_df['pr']=full_pd_filt['Price_i']

clean_df = clean_df[clean_df['pm']<40.0]

clean_df.to_csv('train.csv', header=True, index=False, encoding='utf-8')
