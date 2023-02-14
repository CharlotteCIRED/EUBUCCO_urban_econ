# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 09:39:44 2022

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

data = pd.read_pickle("C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/df-FRA-preliminary.pkl")

gadm = gpd.read_file(path_folder + "EUBUCCO/Data/gadm41_FRA.gpkg")
with open(path_folder + "EUBUCCO/Data/gadm41_FRA_4.json/gadm41_FRA_4.json", 'r') as f:
    data = json.load(f)
    
gdf = gpd.GeoDataFrame.from_features(data["features"])
gdf.plot()

FUA = gpd.read_file(path_folder + "Data/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg")
FUA.Cntry_name.unique()
europe = ['Germany', 'France', 'Italy', 'Spain', 'Poland','Belgium','Netherlands','Austria', 
          'Denmark', 'Finland', 'CzechRepublic', 'Sweden', 'Switzerland', 'Slovakia', 'Hungary', 
          'Portugal', 'Romania', 'Lithuania', 'Ireland', 'Greece', 'Slovenia','Croatia',
          'Bulgaria','Estonia','Latvia', 'Cyprus', 'Luxembourg', 'Malta']

FUA_FR = FUA.loc[FUA.Cntry_name.isin(europe),:]
FUA_FR["ID"] = 1
stats_ctry = FUA_FR.loc[:,["ID","Cntry_name","FUA_p_2015"]].groupby("Cntry_name").sum()

GHS_cent = gpd.read_file(path_folder + "EUBUCCO/Data/GHS_STAT_UCDB2015MT_GLOBE_R2019A/GHS_STAT_UCDB2015MT_GLOBE_R2019A_V1_2.gpkg")
GHS_cent.CTR_MN_NM.unique()
europe = ['Germany', 'France', 'Italy', 'Spain', 'Poland','Belgium','Netherlands','Austria', 
          'Denmark', 'Finland', 'Czech Republic', 'Sweden', 'Switzerland', 'Slovakia', 'Hungary', 
          'Portugal', 'Romania', 'Lithuania', 'Ireland', 'Greece', 'Slovenia','Croatia',
          'Bulgaria','Estonia','Latvia', 'Cyprus', 'Luxembourg', 'Malta']

GHS_cent = GHS_cent.loc[GHS_cent.CTR_MN_NM.isin(europe),:]
GHS_cent["ID"] = 1
stats_ctry = GHS_cent.loc[:,["ID","CTR_MN_NM"]].groupby("CTR_MN_NM").sum()

GHS_cent = GHS_cent.loc[GHS_cent.CTR_MN_NM == "Luxembourg",:]

