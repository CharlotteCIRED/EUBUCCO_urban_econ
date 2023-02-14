# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:20:26 2023

@author: charl
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import json
from pyproj import Proj, transform
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from shapely.geometry import Point
import matplotlib.pyplot as plt
from geopandas.tools import sjoin
import copy
from shapely import wkt
from shapely.geometry import Polygon
from sklearn import linear_model
import math
import csv

path_folder = "C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/v0.1/"
path_ouputs = 'C:/Users/charl/OneDrive/Bureau/EUBUCCO/Sorties/'
df = pd.DataFrame(columns = ["buildings_area", "height", "Country"])

country = "AUT"
countries = listdir(path_folder)

for country in countries:
    gdf = gpd.read_file(path_folder + "v0_1-" + country +".gpkg")
    gdf["buildings_area"] = gdf.area
    gdf = gdf.loc[:,["buildings_area", "height"]]
    gdf["Country"] = "AUT"


df = df.append(gdf)

plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['austria', 'belgium','bulgaria', 'croatia', 'cyprus', 'czechia', 'denmark'])].loc[:,['Country', 'buildings_area']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()

plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['estonia', 'finland','france', 'germany', 'hungary', 'ireland', 'italy'])].loc[:,['Country', 'buildings_area']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()


plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['latvia', 'lithuania','luxembourg', 'malta', 'netherlands', 'poland', 'portugal'])].loc[:,['Country', 'buildings_area']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()


plt.figure()
plt.rcParams.update({'font.size': 40})
joyplot(
    data=df[df.Country.isin(['romania', 'slovakia','slovenia', 'spain', 'sweden', 'switzerland'])].loc[:,['Country', 'buildings_area']], 
    by='Country',
    figsize=(12, 12),
    x_range = ([0,700]),
    title = None, fade = True
    
)
plt.show()
