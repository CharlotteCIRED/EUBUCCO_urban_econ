# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:28:14 2023

@author: charl
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:12:11 2023

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
from esda.moran import Moran
import scipy
from os import listdir
import fiona

path_folder = "C:/Users/charl/OneDrive/Bureau/EUBUCCO/"

path_FUA_OECD = path_folder + "Data/FUA_OECD/"
UA = gpd.read_file(path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
UA = UA.to_crs('epsg:3035')

for name_file in listdir(path_folder + "Data/v0.1/"):
    
    print(name_file)
    name_file = str(name_file)
    #data = pd.read_csv(path_folder + "Data/v0.1/" + name_file)
    #data['geometry'] = data['geometry'].apply(wkt.loads)
    #gdf = gpd.GeoDataFrame(data, crs='epsg:3035')

    gdf = gpd.read_file(path_folder + "Data/v0.1/" + name_file)
     
    inter_FUA = sjoin(UA, gdf, how='inner')
    name_inter_FUA = list(np.unique(inter_FUA.URAU_CODE))
     
    print(name_inter_FUA)
    
    for name_FUA in name_inter_FUA:
          
        FUA_here = UA.loc[UA.URAU_CODE == name_FUA,:]
        gdf_FUA = sjoin(gdf, FUA_here, how='left')
        gdf_FUA = gdf_FUA.loc[gdf_FUA.URAU_CODE == name_FUA,:]
        
        if name_FUA.find('/')!=-1:
            name_FUA=name_FUA.replace("/", "-")
            
        gdf_FUA.to_file(path_folder + "Data/EUBUCCO_by_UA/"+str((FUA_here.URAU_CODE.squeeze()))+"_" + name_file[:-5]+ '.shp')
        
#Correction for FUAs over different countriesgpkg = gpd.read_file('path_to_file.gpkg')