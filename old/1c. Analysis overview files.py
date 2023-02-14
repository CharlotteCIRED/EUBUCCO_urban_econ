# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:18:04 2023

@author: charl
"""

import pandas as pd
import numpy as np
import requests
import json
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import copy
from sklearn import linear_model
import math
import csv
from joypy import joyplot
from os import listdir

path_folder = "C:/Users/charl/OneDrive/Bureau/EUBUCCO/city-level-overview-tables-v0.1/"
countries = listdir(path_folder)
df = pd.DataFrame(columns = ['Country', 'id', 'region', 'city', 'a_mean', 'a_med', 'height_mean',
                         'height_med', 'a_max', 'a_min', 'height_p_inf_0', 'height_p_26_inf'])

for country in countries[1:]:
    country = country[0:-13]
    df_country = pd.read_csv(path_folder + country + "_overview.csv")
    df_country = df_country.loc[:,['id', 'region', 'city', 'a_mean', 'a_med', 'height_mean',
                         'height_med', 'a_max', 'a_min', 'height_p_inf_0', 'height_p_26_inf']]
    df_country["Country"] = country
    df = df.append(df_country)


plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['austria', 'belgium','bulgaria', 'croatia', 'cyprus', 'czechia', 'denmark'])].loc[:,['Country', 'a_mean']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()

plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['estonia', 'finland','france', 'germany', 'hungary', 'ireland', 'italy'])].loc[:,['Country', 'a_mean']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()


plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['latvia', 'lithuania','luxembourg', 'malta', 'netherlands', 'poland', 'portugal'])].loc[:,['Country', 'a_mean']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()


plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['romania', 'slovakia','slovenia', 'spain', 'sweden', 'switzerland'])].loc[:,['Country', 'a_mean']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()
