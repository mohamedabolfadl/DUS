# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:53:07 2017

@author: m00760171
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


dataset = pd.read_csv('train_ID.csv')
dataset['score']=0.0

dataset_ID_PLZ = pd.DataFrame()
dataset_ID_PLZ['ID']=dataset['ID']
dataset_ID_PLZ['PLZ']=dataset['PLZ']
dataset_orig = dataset
dataset = dataset.drop('PLZ',axis=1)
dataset = dataset.drop('ID',axis=1)

X = dataset.iloc[:, :].values

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_n = sc_X.fit_transform(X)
sc_X = StandardScaler()
dataset_n = pd.DataFrame(sc_X.fit_transform(dataset))

dataset_n.columns = ['Price','Room_count','Square_meter','d_cc','d_a','d_w','pr_qm','score']


w_qm = 1
w_rm = 0.1
w_pr = 3
w_dw =0
w_dc =1 
w_da = 0


dataset_n['score'] = w_qm*dataset_n['Square_meter']+w_rm*dataset_n['Room_count']-w_pr*dataset_n['Price']-w_dw*dataset_n['d_w']-w_dc*dataset_n['d_cc']-w_da*dataset_n['d_a']


dataset_n = sc_X.inverse_transform(dataset_n)
dataset_n =pd.DataFrame(dataset_n)
dataset_n.columns = ['Price','Room_count','Square_meter','d_cc','d_a','d_w','pr_qm','score']

dataset = pd.concat([dataset_ID_PLZ,dataset_n],axis=1)


# Filtering
dataset = dataset[ dataset['Price']<1300]
dataset = dataset[ dataset['Square_meter']>60]
dataset = dataset[ dataset['Room_count']>2]

dataset_sorted = dataset.sort_values(['score'],ascending = False)



