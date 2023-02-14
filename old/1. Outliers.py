# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:30:29 2022

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
country = "CYP"

gdf = gpd.read_file(path_folder + "v0_1-" + country +".gpkg")

if country == "CZE":
    
    gdf1 = gpd.read_file(path_folder + "v0_1-" + country +"_1.gpkg")
    gdf2 = gpd.read_file(path_folder + "v0_1-" + country +"_2.gpkg")
    gdf3 = gpd.read_file(path_folder + "v0_1-" + country +"_3.gpkg")
    gdf4 = gpd.read_file(path_folder + "v0_1-" + country +"_4.gpkg")
    gdf5 = gpd.read_file(path_folder + "v0_1-" + country +"_5.gpkg")
    gdf6 = gpd.read_file(path_folder + "v0_1-" + country +"_6.gpkg")
    gdf7 = gpd.read_file(path_folder + "v0_1-" + country +"_7.gpkg")
    gdf8 = gpd.read_file(path_folder + "v0_1-" + country +"_8.gpkg")
    gdf9 = gpd.read_file(path_folder + "v0_1-" + country +"_9.gpkg")
    gdf10 = gpd.read_file(path_folder + "v0_1-" + country +"_10.gpkg")
    gdf11 = gpd.read_file(path_folder + "v0_1-" + country +"_11.gpkg")
    gdf12 = gpd.read_file(path_folder + "v0_1-" + country +"_12.gpkg")
    gdf13 = gpd.read_file(path_folder + "v0_1-" + country +"_13.gpkg")
    gdf14 = gpd.read_file(path_folder + "v0_1-" + country +"_14.gpkg")
    
    #EUBUCCO1 = pd.read_csv(path_folder + "EUBUCCO/Data/EUBUCCO_COUNTRY/v0_1-BEL_1.csv")
    #EUBUCCO1['geometry'] = EUBUCCO1['geometry'].apply(wkt.loads)
    #gdf1 = gpd.GeoDataFrame(EUBUCCO1, crs='epsg:3035')

    gdf = pd.concat([gdf1, gdf2, gdf3, gdf4, gdf5, gdf6, gdf7, gdf8, gdf9, gdf10, gdf11, gdf12, gdf13, gdf14], ignore_index=True)
    
elif country == "DEU":
    
    gdf1 = gpd.read_file(path_folder + "v0_1-" + country +"_1.gpkg")
    gdf2 = gpd.read_file(path_folder + "v0_1-" + country +"_2.gpkg")
    gdf3 = gpd.read_file(path_folder + "v0_1-" + country +"_3.gpkg")
    gdf4 = gpd.read_file(path_folder + "v0_1-" + country +"_4.gpkg")
    gdf5 = gpd.read_file(path_folder + "v0_1-" + country +"_5.gpkg")
    gdf6 = gpd.read_file(path_folder + "v0_1-" + country +"_6.gpkg")
    gdf7 = gpd.read_file(path_folder + "v0_1-" + country +"_7.gpkg")
    gdf8 = gpd.read_file(path_folder + "v0_1-" + country +"_8.gpkg")
    gdf9 = gpd.read_file(path_folder + "v0_1-" + country +"_9.gpkg")
    
    gdf10 = gpd.read_file(path_folder + "v0_1-" + country +"_10.gpkg")
    gdf11 = gpd.read_file(path_folder + "v0_1-" + country +"_11.gpkg")
    gdf12 = gpd.read_file(path_folder + "v0_1-" + country +"_12.gpkg")
    gdf13 = gpd.read_file(path_folder + "v0_1-" + country +"_13.gpkg")
    gdf14 = gpd.read_file(path_folder + "v0_1-" + country +"_14.gpkg")
    gdf15 = gpd.read_file(path_folder + "v0_1-" + country +"_15.gpkg")
    gdf16 = gpd.read_file(path_folder + "v0_1-" + country +"_16.gpkg")
    
    #EUBUCCO1 = pd.read_csv(path_folder + "EUBUCCO/Data/EUBUCCO_COUNTRY/v0_1-BEL_1.csv")
    #EUBUCCO1['geometry'] = EUBUCCO1['geometry'].apply(wkt.loads)
    #gdf1 = gpd.GeoDataFrame(EUBUCCO1, crs='epsg:3035')

    gdfA = pd.concat([gdf1, gdf2, gdf3, gdf4, gdf5, gdf6, gdf7, gdf8, gdf9], ignore_index=True)
    gdfB = pd.concat([gdf10, gdf11, gdf12, gdf13, gdf14, gdf15, gdf16], ignore_index=True)
    
    
### COUNTRY LEVEL

#1b. Geometry quality.
#Are small buidings included or not?
#Do buidings tend to be merged or not?
#Are geometries precise or not?

gdf["buildings_area"] = gdf.area
gdf["volume"] = gdf["buildings_area"] * gdf["height"]

#gdf["buildings_area"].describe()
#gdf["height"].describe()
#gdf["volume"].describe()

#plt.hist(gdf["buildings_area"][gdf["buildings_area"]<1000], bins = 50)
#plt.hist(gdf["height"][gdf["height"] < 25], bins = 50)
#plt.hist(gdf["volume"][gdf["volume"]<20000], bins = 50)
#plt.close()

#gdf["buildings_area"][gdf["buildings_area"]<1000].plot(kind='density')
#gdf["height"][gdf["height"] < 25].plot(kind='density')

#gdf.loc[[4500],'geometry'].plot()
#plt.savefig(path_folder + "EUBUCCO/Sorties/" + country + "_example.png")
#plt.close()

#1c. Attribute quality
unique_height = len(np.unique(gdf["height"].astype(str)))
unique_age = len(np.unique(gdf["age"].astype(str)))
unique_type = len(np.unique(gdf["type"].astype(str))) #fit_transform(gdf["type"].astype(str))

gdf["count"] = 1
gdf.loc[:,["type", "count"]].groupby("type").sum()

#2a. Outlier assessment
 
over_320_height = sum(gdf["height"] > 320) / len(gdf)
over_3000_area = sum(gdf["buildings_area"] > 3000) / len(gdf)
over_100000_area = sum(gdf["buildings_area"] > 100000) / len(gdf)
under_2_height = sum(gdf["height"] < 2) / len(gdf)
under_4_area = sum(gdf["buildings_area"] < 4) / len(gdf)

#gdf.iloc[80882]['geometry']
#Differdange = gdf.loc[gdf.id_source.str.startswith("Differdange"),:]
#fig, ax = plt.subplots(figsize=(15, 15))
#Differdange.plot(ax=ax, alpha=0.7, color="grey") #ARCELOR-MITTAL

#gdf.iloc[88159]['geometry']
#Esch = gdf.loc[gdf.id_source.str.startswith("Esch-sur-Alzette"),:]
#fig, ax = plt.subplots(figsize=(15, 15))
#Esch.plot(ax=ax, alpha=0.7, color="grey") #ARCELOR-MITTAL

#2b. Attribute distribution assessment

def outlier_aware_hist(data, param_bins, lower=None, upper=None, filename = None):
    if not lower:# or lower < data.min():
        lower = data.min()
        lower_outliers = False
    else:
        lower_outliers = True

    if not upper or upper > data.max():
        upper = data.max()
        upper_outliers = False
    else:
        upper_outliers = True

    n, bins, patches = plt.hist(data, range=(lower, upper), bins=param_bins)

    if lower_outliers:
        n_lower_outliers = (data < lower).sum()
        patches[0].set_height(patches[0].get_height() + n_lower_outliers)
        patches[0].set_facecolor('c')
        patches[0].set_label('Lower outliers: ({:.2f}, {:.2f})'.format(data.min(), lower))

    if upper_outliers:
        n_upper_outliers = (data > upper).sum()
        patches[-1].set_height(patches[-1].get_height() + n_upper_outliers)
        patches[-1].set_facecolor('m')
        patches[-1].set_label('Upper outliers: ({:.2f}, {:.2f})'.format(upper, data.max()))

    if lower_outliers or upper_outliers:
        plt.legend()
        
    plt.ylim(0, 30000)
        
    plt.savefig(filename)
    plt.close()

outlier_aware_hist(gdf["height"], 50, lower=2, upper=25, filename = path_ouputs + country + "_height.png")
outlier_aware_hist(gdf["buildings_area"], 50, lower=4, upper=1000, filename = path_ouputs + country + "_area.png")
outlier_aware_hist(gdf["volume"], 50, lower=8, upper=20000, filename = path_ouputs + country + "_volume.png")

thisdict = {
  "unique_height": unique_height,
  "unique_age": unique_age,
  "unique_type": unique_type,
  "over_320_height": over_320_height,
  "over_3000_area": over_3000_area,
  "over_100000_area": over_100000_area,
  "under_2_height": under_2_height,
  "under_4_area": under_4_area,
  "nb": len(gdf)
  
}

w = csv.writer(open(path_ouputs + country + ".csv", "w"))
    
with open(path_ouputs + country + ".csv", 'w') as f:
    w = csv.DictWriter(f, thisdict.keys())
    w.writeheader()
    w.writerow(thisdict)


