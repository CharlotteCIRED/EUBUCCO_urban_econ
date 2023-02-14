# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:45:32 2022

@author: charl
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas.tools import sjoin
import scipy
from os import listdir
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '')

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

kona = pd.read_excel(path_folder + "Data/GlobalCoM.xlsx", sheet_name="Table 2")
kona_ancillary = pd.read_excel(
    path_folder + "Data/GlobalCoM.xlsx", sheet_name="Table 3")
kona = kona.merge(kona_ancillary, on="GCoM_ID")

kona_gdf = gpd.GeoDataFrame(
    kona, geometry=gpd.points_from_xy(kona["longitude"], kona["latitude"]))

kona_gdf = kona_gdf.set_crs('epsg:4326')
kona_gdf = kona_gdf.to_crs('epsg:3035')

kona_with_FUA = sjoin(kona_gdf, FUA, how="right")
kona_with_FUA = kona_with_FUA.loc[~np.isnan(kona_with_FUA.index_left), :]


if geo_boundary == "GHSL":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'emission_inventory_id', 'emission_inventory_sector', 'type_of_emissions',
                                          'inventory_year', 'population_in_the_inventory_year', 'emissions', 'eFUA_ID', 'eFUA_name', 'FUA_p_2015', 'geometry']]
    kona_with_FUA = kona_with_FUA.pivot(index=['GCoM_ID', 'inventory_year'], columns=[
                                        'emission_inventory_sector', 'type_of_emissions'], values='emissions').reset_index()
elif geo_boundary == "OECD":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'emission_inventory_id', 'emission_inventory_sector', 'type_of_emissions',
                                          'inventory_year', 'population_in_the_inventory_year', 'emissions', 'fuacode', 'fuaname', 'geometry']]
    kona_with_FUA = kona_with_FUA.pivot(index=['GCoM_ID', 'inventory_year'], columns=[
                                        'emission_inventory_sector', 'type_of_emissions'], values='emissions').reset_index()
elif geo_boundary == "UA":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'emission_inventory_id', 'emission_inventory_sector', 'type_of_emissions',
                                          'inventory_year', 'population_in_the_inventory_year', 'emissions', 'URAU_CODE', 'URAU_NAME', 'geometry']]
    kona_with_FUA["dup"] = kona_with_FUA.duplicated(
        subset=['GCoM_ID', 'inventory_year', 'emission_inventory_sector', 'type_of_emissions'], keep='first')
    kona_with_FUA = kona_with_FUA.loc[kona_with_FUA.dup == False, :]
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'emission_inventory_id', 'emission_inventory_sector',
                                          'type_of_emissions', 'inventory_year',
                                          'population_in_the_inventory_year', 'emissions', 'URAU_CODE',
                                          'URAU_NAME', 'geometry']]
    kona_with_FUA = kona_with_FUA.pivot(index=['GCoM_ID', 'inventory_year'], columns=[
                                        'emission_inventory_sector', 'type_of_emissions'], values='emissions').reset_index()

a = kona_with_FUA.columns
ind = pd.Index([e[0] + e[1] for e in a.tolist()])
kona_with_FUA.columns = ind
kona_with_FUA = kona_with_FUA.reset_index()

duplicate_kona = set(
    [x for x in kona_with_FUA.GCoM_ID if list(kona_with_FUA.GCoM_ID).count(x) > 1])

for id_dup in duplicate_kona:
    print(id_dup)
    subset_dup = kona_with_FUA.loc[kona_with_FUA.GCoM_ID == id_dup, :]
    max_year = max(subset_dup.inventory_year)
    kona_with_FUA = kona_with_FUA.loc[(kona_with_FUA.GCoM_ID != id_dup) | (
        (kona_with_FUA.GCoM_ID == id_dup) & (kona_with_FUA.inventory_year == max_year)), :]

kona_with_FUA = kona_with_FUA.merge(kona_gdf.loc[:, ['GCoM_ID', 'geometry', 'population_in_the_inventory_year',
                                    'inventory_year']].drop_duplicates(), on=["GCoM_ID", 'inventory_year'], how='left')
kona_with_FUA = gpd.GeoDataFrame(
    kona_with_FUA, geometry=kona_with_FUA['geometry'])

kona_with_FUA = sjoin(kona_with_FUA, FUA, how="right")
kona_with_FUA = kona_with_FUA.loc[~np.isnan(kona_with_FUA.index_left), :]
kona_with_FUA = kona_with_FUA.merge(
    kona_ancillary.loc[:, ['GCoM_ID', 'signatory name']], on="GCoM_ID")

if geo_boundary == "GHSL":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'inventory_year',
                                          'Municipal buildings and facilitiesindirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesindirect_emissions',
                                          'Residential buildings and facilitiesindirect_emissions',
                                          'Transportationdirect_emissions',
                                          'Residential buildings and facilitiesdirect_emissions',
                                          'Municipal buildings and facilitiesdirect_emissions',
                                          'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesdirect_emissions',
                                          'Manufacturing and construction industriesdirect_emissions',
                                          'Manufacturing and construction industriesindirect_emissions',
                                          'population_in_the_inventory_year', 'eFUA_ID',
                                          'eFUA_name', 'FUA_p_2015', 'geometry',
                                          'signatory name']]

    kona_with_FUA = kona_with_FUA.groupby('eFUA_ID').agg({'Municipal buildings and facilitiesindirect_emissions': 'sum',
                                                          'Institutional/tertiary buildings and facilitiesindirect_emissions': 'sum',
                                                          'Residential buildings and facilitiesindirect_emissions': 'sum',
                                                          'Transportationdirect_emissions': 'sum',
                                                          'Residential buildings and facilitiesdirect_emissions': 'sum',
                                                          'Municipal buildings and facilitiesdirect_emissions': 'sum',
                                                          'Transportationindirect_emissions': 'sum',
                                                          'Waste/wastewaterdirect_emissions': 'sum',
                                                          'Institutional/tertiary buildings and facilitiesdirect_emissions': 'sum',
                                                          'Manufacturing and construction industriesdirect_emissions': 'sum',
                                                          'Manufacturing and construction industriesindirect_emissions': 'sum',
                                                          'population_in_the_inventory_year': 'sum',
                                                          'eFUA_name': 'first',
                                                          'FUA_p_2015': 'first', 'geometry': 'first'})

    kona_with_FUA.to_excel(path_folder+'Data/kona_FUA_GHSL.xlsx')

if geo_boundary == "OECD":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'inventory_year',
                                          'Municipal buildings and facilitiesindirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesindirect_emissions',
                                          'Residential buildings and facilitiesindirect_emissions',
                                          'Transportationdirect_emissions',
                                          'Residential buildings and facilitiesdirect_emissions',
                                          'Municipal buildings and facilitiesdirect_emissions',
                                          'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesdirect_emissions',
                                          'Manufacturing and construction industriesdirect_emissions',
                                          'Manufacturing and construction industriesindirect_emissions',
                                          'population_in_the_inventory_year', 'fuacode',
                                          'fuaname', 'geometry',
                                          'signatory name']]

    kona_with_FUA = kona_with_FUA.groupby('fuacode').agg({'Municipal buildings and facilitiesindirect_emissions': 'sum',
                                                          'Institutional/tertiary buildings and facilitiesindirect_emissions': 'sum',
                                                          'Residential buildings and facilitiesindirect_emissions': 'sum',
                                                          'Transportationdirect_emissions': 'sum',
                                                          'Residential buildings and facilitiesdirect_emissions': 'sum',
                                                          'Municipal buildings and facilitiesdirect_emissions': 'sum',
                                                          'Transportationindirect_emissions': 'sum',
                                                          'Waste/wastewaterdirect_emissions': 'sum',
                                                          'Institutional/tertiary buildings and facilitiesdirect_emissions': 'sum',
                                                          'Manufacturing and construction industriesdirect_emissions': 'sum',
                                                          'Manufacturing and construction industriesindirect_emissions': 'sum',
                                                          'population_in_the_inventory_year': 'sum',
                                                          'fuaname': 'first', 'geometry': 'first'})

    kona_with_FUA.to_excel(path_folder+'Data/kona_FUA_OECD.xlsx')

if geo_boundary == "UA":
    kona_with_FUA = kona_with_FUA.loc[:, ['GCoM_ID', 'inventory_year',
                                          'Municipal buildings and facilitiesindirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesindirect_emissions',
                                          'Residential buildings and facilitiesindirect_emissions',
                                          'Transportationdirect_emissions',
                                          'Residential buildings and facilitiesdirect_emissions',
                                          'Municipal buildings and facilitiesdirect_emissions',
                                          'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
                                          'Institutional/tertiary buildings and facilitiesdirect_emissions',
                                          'Manufacturing and construction industriesdirect_emissions',
                                          'Manufacturing and construction industriesindirect_emissions',
                                          'population_in_the_inventory_year', 'URAU_CODE',
                                          'URAU_NAME', 'geometry',
                                          'signatory name']]

    kona_with_FUA = kona_with_FUA.groupby('URAU_CODE').agg({'Municipal buildings and facilitiesindirect_emissions': 'sum',
                                                            'Institutional/tertiary buildings and facilitiesindirect_emissions': 'sum',
                                                            'Residential buildings and facilitiesindirect_emissions': 'sum',
                                                            'Transportationdirect_emissions': 'sum',
                                                            'Residential buildings and facilitiesdirect_emissions': 'sum',
                                                            'Municipal buildings and facilitiesdirect_emissions': 'sum',
                                                            'Transportationindirect_emissions': 'sum',
                                                            'Waste/wastewaterdirect_emissions': 'sum',
                                                            'Institutional/tertiary buildings and facilitiesdirect_emissions': 'sum',
                                                            'Manufacturing and construction industriesdirect_emissions': 'sum',
                                                            'Manufacturing and construction industriesindirect_emissions': 'sum',
                                                            'population_in_the_inventory_year': 'sum',
                                                            'URAU_NAME': 'first', 'geometry': 'first'})

    kona_with_FUA.to_excel(path_folder+'Data/kona_urban_audit.xlsx')
