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

path_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '')
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

name_file = "v0_1-LUX.gpkg"
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
        ame_FUA = name_FUA.replace("/", "-")

    gdf_FUA.to_file(path_folder + "Data/EUBUCCO_by_OECD_FUA/" +
                    str((FUA_here.fuacode.squeeze()))+"_" + name_file[:-5] + '.shp')
