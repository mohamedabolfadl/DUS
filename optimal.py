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



w_qm_v = [1,1,1,0.5]
w_rm_v = [0.1,0.1,0.1,0.1]
w_pr_v = [0.5,0.5,0.5,3]
w_dw_v =[1,0.1,0.1,0.1]
w_dc_v =[0.1,1,0.1,0.1] 
w_da_v = [0.1,0.1,1,0.1]


N_top = 5
zero_data = np.zeros(shape=(N_top,4))
result_df = pd.DataFrame(0, index=np.arange(N_top), columns=['Work','CC','Area','Pr'])

#result_df = pd.DataFrame([[0,0,0,0],[0,0,0,0],[0,0,0,0]])
#result_df.columns=['Work','CC','Area','Pr']

i=0


while i<len(result_df.columns):

    w_qm = w_qm_v[i]
    w_rm = w_rm_v[i]
    w_pr = w_pr_v[i]
    w_dw =w_dw_v[i]
    w_dc =w_dc_v[i] 
    w_da = w_da_v[i]
    
    dataset_n = pd.DataFrame(sc_X.fit_transform(dataset))
    dataset_n.columns = ['Price','Room_count','Square_meter','d_cc','d_a','d_w','pr_qm','score']
    dataset_n['score'] = w_qm*dataset_n['Square_meter']+w_rm*dataset_n['Room_count']-w_pr*dataset_n['Price']-w_dw*dataset_n['d_w']-w_dc*dataset_n['d_cc']-w_da*dataset_n['d_a']
    dataset_n = sc_X.inverse_transform(dataset_n)
    dataset_n =pd.DataFrame(dataset_n)
    dataset_n.columns = ['Price','Room_count','Square_meter','d_cc','d_a','d_w','pr_qm','score']
    dataset_f = pd.concat([dataset_ID_PLZ,dataset_n],axis=1)
    # Filtering
    dataset_f = dataset_f[ dataset_f['Price']<1300]
    dataset_f = dataset_f[ dataset_f['Square_meter']>60]
    dataset_f = dataset_f[ dataset_f['Room_count']>2]
    dataset_sorted = dataset_f.sort_values(['score'],ascending = False)
    
    t = np.array(dataset_sorted.head(N_top)['ID'])
    j = 0 
    while j <N_top:
        result_df[result_df.columns[i]][j] = t[j]
        j=j+1
    i=i+1

