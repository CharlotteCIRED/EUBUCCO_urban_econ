# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:46:05 2022

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

path_folder = "C:/Users/charl/OneDrive/Bureau/"

FUA = gpd.read_file(path_folder + "Data/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg")

eubucco_spain = pd.read_csv(path_folder + "EUBUCCO/Data/v0_1-ESP_2.csv")
eubucco_spain['geometry'] = eubucco_spain['geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(eubucco_spain, crs='epsg:3035')

FUA = FUA.loc[FUA.eFUA_name == "Zaragoza",:]
FUA = FUA.to_crs('epsg:3035')

gdf = sjoin(gdf, FUA, how='left')
gdf = gdf.loc[gdf.eFUA_name == "Zaragoza",:]

gdf.plot()

#### MORAN'I
gdf = gdf.loc[gdf["type"] != "unknown",:]
weight_spatial = gdf.centroid.apply(lambda g: gdf.centroid.distance(g))
Moran(gdf["type"], weight_spatial)