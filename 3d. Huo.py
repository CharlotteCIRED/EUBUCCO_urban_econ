# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:05:25 2023

@author: charl
"""

import pandas as pd
import geopandas as gpd
from os import listdir
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '')


huo = pd.read_csv(path_folder + "Data/Near-real-time daily estimates of CO2 emissions from 1500 cities worldwide/carbon-monitor-cities-all-cities-FUA-v0325.csv")
huo.columns = ['city', 'country', 'date', 'sector', 'value', 'timestamp']
huo = huo.loc[:,['city', 'date', 'sector', 'value']].sort_values('date').groupby(['city','sector']).tail(1)
huo = huo.loc[(huo.sector == "Residential")|(huo.sector == "Ground Transport"),:]

FUA_GHSL = gpd.read_file("C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg")
FUA_GHSL = FUA_GHSL.to_crs('epsg:3035')

path_FUA_OECD = path_folder + "Data/FUA_OECD/"
oecd_countries = listdir(path_FUA_OECD)
FUA_OECD = gpd.read_file(path_FUA_OECD + "AUT/AUT_core_commuting.shp")
FUA_OECD = FUA_OECD.to_crs('epsg:3035')
for country in oecd_countries[1:24]:
    df2 = gpd.read_file(path_FUA_OECD + country + "/" + country + "_core_commuting.shp")
    df2 = df2.to_crs('epsg:3035')
    FUA_OECD = gpd.GeoDataFrame(pd.concat([FUA_OECD, df2], ignore_index=True) )


huo_OECD = huo.merge(FUA_OECD, left_on = "city", right_on = "fuaname", how = "inner")
huo_GHSL = huo.merge(FUA_GHSL, left_on = "city", right_on = "eFUA_name", how = "inner")
huo_GHSL["to_drop"] = huo_GHSL.city.isin(list(huo_OECD.city))
huo_GHSL = huo_GHSL.loc[huo_GHSL.to_drop == False,:]

huo_OECD_transport = huo_OECD.loc[huo_OECD.sector == "Ground Transport", ["city", "value"]]
huo_OECD_resid = huo_OECD.loc[huo_OECD.sector == "Residential", ["city", "value", "date", "fuacode", "fuaname", "geometry"]]
huo_OECD_transport.columns = ["city", "transport"]
huo_OECD_resid.columns = ["city", "residential", "date", "fuacode", "fuaname", "geometry"]
huo_OECD = huo_OECD_transport.merge(huo_OECD_resid, on = "city")

huo_GHSL_transport = huo_GHSL.loc[huo_GHSL.sector == "Ground Transport", ["city", "value"]]
huo_GHSL_resid = huo_GHSL.loc[huo_GHSL.sector == "Residential", ["city", "value", "date", "eFUA_ID", "eFUA_name", "geometry"]]
huo_GHSL_transport.columns = ["city", "transport"]
huo_GHSL_resid.columns = ["city", "residential", "date", "eFUA_ID", "eFUA_name", "geometry"]
huo_GHSL = huo_GHSL_transport.merge(huo_GHSL_resid, on = "city")

huo_GHSL = huo_GHSL.drop_duplicates('city')
huo_OECD = huo_OECD.drop_duplicates('city')

huo_GHSL.to_excel(path_folder+'Data/huo_GHSL.xlsx')

huo_OECD.to_excel(path_folder+'Data/huo_OECD.xlsx')