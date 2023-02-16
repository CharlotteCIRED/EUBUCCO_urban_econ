# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:45:32 2022

@author: charl
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 11:09:19 2022

@author: charl
"""


import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin
from os import listdir
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '')

geo_boundary = "UA"  # OECD, UA

if geo_boundary == "GHSL":
    FUA = gpd.read_file(
        "C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg")
    FUA = FUA.to_crs('epsg:3035')
elif geo_boundary == "OECD":
    path_FUA_OECD = path_folder + "Data/FUA_OECD/"
    oecd_countries = listdir(path_FUA_OECD)
    FUA = gpd.read_file(path_FUA_OECD + "AUT/AUT_core_commuting.shp")
    FUA = FUA.to_crs('epsg:3035')
    for country in oecd_countries[1:24]:
        df2 = gpd.read_file(path_FUA_OECD + country + "/" +
                            country + "_core_commuting.shp")
        df2 = df2.to_crs('epsg:3035')
        FUA = gpd.GeoDataFrame(pd.concat([FUA, df2], ignore_index=True))
elif geo_boundary == "UA":
    FUA = gpd.read_file(
        path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
    FUA = FUA.to_crs('epsg:3035')
    FUA['geometry'] = FUA.geometry.buffer(6000)


nangini = pd.read_excel(
    path_folder + 'Data/Nangini/Scripts_and_datafiles/SCRIPTS/DATA/' + "D_FINAL.xlsx")
nangini_gdf = gpd.GeoDataFrame(
    nangini, geometry=gpd.points_from_xy(nangini["Longitude (others) [degrees]"], nangini["Latitude (others) [degrees]"]))

nangini_gdf = nangini_gdf.set_crs('epsg:4326')
nangini_gdf = nangini_gdf.to_crs('epsg:3035')
nangini_gdf = nangini_gdf.loc[nangini_gdf.Region == "Europe", :]

nangini_with_FUA = sjoin(nangini_gdf, FUA, how="right")  # right
nangini_with_FUA = nangini_with_FUA.loc[~np.isnan(
    nangini_with_FUA.index_left), :]

if geo_boundary == "GHSL":
    nangini_with_FUA = nangini_with_FUA.loc[:, ['City name', 'Scope-1 GHG emissions [tCO2 or tCO2-eq]',
                                                'Scope-2 (CDP) [tCO2-eq]', 'Total emissions (CDP) [tCO2-eq]',  'Population (others)',  'Population (CDP)', 'eFUA_ID', 'eFUA_name', 'FUA_p_2015']]
    duplicate_FUA = set([x for x in nangini_with_FUA.eFUA_ID if list(
        nangini_with_FUA.eFUA_ID).count(x) > 1])
elif geo_boundary == "OECD":
    nangini_with_FUA = nangini_with_FUA.loc[:, ['City name', 'Scope-1 GHG emissions [tCO2 or tCO2-eq]',
                                                'Scope-2 (CDP) [tCO2-eq]', 'Total emissions (CDP) [tCO2-eq]',  'Population (others)',  'Population (CDP)', 'fuacode', 'fuaname']]
    duplicate_FUA = set([x for x in nangini_with_FUA.fuacode if list(
        nangini_with_FUA.fuacode).count(x) > 1])
elif geo_boundary == "UA":
    nangini_with_FUA = nangini_with_FUA.loc[:, ['City name', 'Scope-1 GHG emissions [tCO2 or tCO2-eq]',
                                                'Scope-2 (CDP) [tCO2-eq]', 'Total emissions (CDP) [tCO2-eq]',  'Population (others)',  'Population (CDP)', 'URAU_CODE', 'URAU_NAME']]
    duplicate_FUA = set([x for x in nangini_with_FUA.URAU_CODE if list(
        nangini_with_FUA.URAU_CODE).count(x) > 1])

if geo_boundary == "GHSL":
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = nangini_with_FUA.loc[nangini_with_FUA.eFUA_ID == id_dup, :]
        nangini_with_FUA = nangini_with_FUA.loc[nangini_with_FUA.eFUA_ID != id_dup, :]
        new_row = {'City name': subset_dup['City name'].iloc[0],
                   'Scope-1 GHG emissions [tCO2 or tCO2-eq]': sum(subset_dup['Scope-1 GHG emissions [tCO2 or tCO2-eq]']),
                   'Scope-2 (CDP) [tCO2-eq]': sum(subset_dup['Scope-2 (CDP) [tCO2-eq]']),
                   'Total emissions (CDP) [tCO2-eq]': sum(subset_dup['Total emissions (CDP) [tCO2-eq]']),
                   'Population (others)': sum(subset_dup['Population (others)']),
                   'Population (CDP)': sum(subset_dup['Population (CDP)']),
                   'eFUA_ID': subset_dup['eFUA_ID'].iloc[0],
                   'eFUA_name': subset_dup['eFUA_name'].iloc[0],
                   'FUA_p_2015': subset_dup['FUA_p_2015'].iloc[0]}
        nangini_with_FUA = nangini_with_FUA.append(new_row, ignore_index=True)
if geo_boundary == "OECD":
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = nangini_with_FUA.loc[nangini_with_FUA.fuacode == id_dup, :]
        nangini_with_FUA = nangini_with_FUA.loc[nangini_with_FUA.fuacode != id_dup, :]
        new_row = {'City name': subset_dup['City name'].iloc[0],
                   'Scope-1 GHG emissions [tCO2 or tCO2-eq]': sum(subset_dup['Scope-1 GHG emissions [tCO2 or tCO2-eq]']),
                   'Scope-2 (CDP) [tCO2-eq]': sum(subset_dup['Scope-2 (CDP) [tCO2-eq]']),
                   'Total emissions (CDP) [tCO2-eq]': sum(subset_dup['Total emissions (CDP) [tCO2-eq]']),
                   'Population (others)': sum(subset_dup['Population (others)']),
                   'Population (CDP)': sum(subset_dup['Population (CDP)']),
                   'fuacode': subset_dup['fuacode'].iloc[0],
                   'fuaname': subset_dup['fuaname'].iloc[0]}
        nangini_with_FUA = nangini_with_FUA.append(new_row, ignore_index=True)
if geo_boundary == "UA":
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = nangini_with_FUA.loc[nangini_with_FUA.URAU_CODE == id_dup, :]
        nangini_with_FUA = nangini_with_FUA.loc[nangini_with_FUA.URAU_CODE != id_dup, :]
        new_row = {'City name': subset_dup['City name'].iloc[0],
                   'Scope-1 GHG emissions [tCO2 or tCO2-eq]': sum(subset_dup['Scope-1 GHG emissions [tCO2 or tCO2-eq]']),
                   'Scope-2 (CDP) [tCO2-eq]': sum(subset_dup['Scope-2 (CDP) [tCO2-eq]']),
                   'Total emissions (CDP) [tCO2-eq]': sum(subset_dup['Total emissions (CDP) [tCO2-eq]']),
                   'Population (others)': sum(subset_dup['Population (others)']),
                   'Population (CDP)': sum(subset_dup['Population (CDP)']),
                   'URAU_CODE': subset_dup['URAU_CODE'].iloc[0],
                   'URAU_NAME': subset_dup['URAU_NAME'].iloc[0]}
        nangini_with_FUA = nangini_with_FUA.append(new_row, ignore_index=True)

if geo_boundary == "GHSL":
    nangini_with_FUA.to_excel(path_folder+'Data/nangini_FUA_GHSL.xlsx')
if geo_boundary == "OECD":
    nangini_with_FUA.to_excel(path_folder+'Data/nangini_FUA_OECD.xlsx')
if geo_boundary == "UA":
    nangini_with_FUA.to_excel(path_folder+'Data/nangini_urban_audit.xlsx')
