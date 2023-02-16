# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:12:11 2023

@author: charl
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin
from os import listdir
import os
import collections

path_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '')
path_FUA_OECD = path_folder + "Data/FUA_OECD/"

# Load OECD FUAs

oecd_countries = listdir(path_FUA_OECD)
FUA_OECD = gpd.read_file(path_FUA_OECD + "AUT/AUT_core_commuting.shp")
FUA_OECD = FUA_OECD.to_crs('epsg:3035')
for country in oecd_countries[1:24]:
    df2 = gpd.read_file(path_FUA_OECD + country + "/" +
                        country + "_core_commuting.shp")
    df2 = df2.to_crs('epsg:3035')
    FUA_OECD = gpd.GeoDataFrame(pd.concat([FUA_OECD, df2], ignore_index=True))

# Do the spatial join

for name_file in listdir(path_folder + "Data/v0.1/"):

    print(name_file)
    name_file = str(name_file)

    gdf = gpd.read_file(path_folder + "Data/v0.1/" + name_file)

    inter_FUA = sjoin(FUA_OECD, gdf, how='inner')
    name_inter_FUA = list(np.unique(inter_FUA.fuaname))

    print(name_inter_FUA)

    for name_FUA in name_inter_FUA:

        FUA_here = FUA_OECD.loc[FUA_OECD.fuaname == name_FUA, :]
        gdf_FUA = sjoin(gdf, FUA_here, how='left')
        gdf_FUA = gdf_FUA.loc[gdf_FUA.fuaname == name_FUA, :]

        if name_FUA.find('/') != -1:
            name_FUA = name_FUA.replace("/", "-")

        gdf_FUA.to_file(path_folder + "Data/EUBUCCO_by_OECD_FUA/" +
                        str((FUA_here.fuacode.squeeze()))+"_" + name_file[:-5] + '.shp')

# Correct for FUAs that extend over different countries

folder_FUA = path_folder + "Data/EUBUCCO_by_OECD_FUA/"

res = []

for file in listdir(folder_FUA):
    if file.endswith('.shp'):
        res.append(file)

y = [z[:5] for z in res]

list_duplicates = [item for item,
                   count in collections.Counter(y).items() if count == 2]
list_triplicates = [item for item,
                    count in collections.Counter(y).items() if count == 3]

for city_id in list_duplicates:
    res = []

    for file in listdir(folder_FUA):
        if (file.endswith('.shp') & file.startswith(city_id)):
            res.append(file)
    print(city_id)
    print(res)
    city1 = gpd.read_file(folder_FUA + res[0])
    city2 = gpd.read_file(folder_FUA + res[1])
    city = city1.append(city2)
    city.to_file(path_folder + "Data/EUBUCCO_by_OECD_FUA/" +
                 city_id+res[0][-8:-4]+res[1][-8:])
    os.remove(folder_FUA + res[0])
    os.remove(folder_FUA + res[1])

for city_id in list_triplicates:
    res = []
    for file in listdir(folder_FUA):
        if (file.endswith('.shp') & file.startswith(city_id)):
            res.append(file)
    print(city_id)
    print(res)
    city1 = gpd.read_file(folder_FUA + res[0])
    city2 = gpd.read_file(folder_FUA + res[1])
    city3 = gpd.read_file(folder_FUA + res[2])
    city = city1.append(city2)
    city = city.append(city3)
    city.to_file(path_folder + "Data/EUBUCCO_by_OECD_FUA/" +
                 city_id+res[0][-8:-4]+res[1][-8:-4]+res[2][-8:])
    os.remove(folder_FUA + res[0])
    os.remove(folder_FUA + res[1])
    os.remove(folder_FUA + res[2])
