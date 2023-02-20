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
geo_boundary = "OECD"  # GHSL, UA

# Import FUAs delineations

if geo_boundary == "GHSL":
    FUA = gpd.read_file(
        "C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg")
    FUA = FUA.to_crs('epsg:3035')
elif geo_boundary == "OECD":
    path_FUA_OECD = path_folder + "Data/FUA_OECD/"
    oecd_countries = listdir(path_FUA_OECD)
    FUA_OECD = gpd.read_file(path_FUA_OECD + "AUT/AUT_core_commuting.shp")
    FUA_OECD = FUA_OECD.to_crs('epsg:3035')
    for country in oecd_countries[1:24]:
        df2 = gpd.read_file(path_FUA_OECD + country + "/" +
                            country + "_core_commuting.shp")
        df2 = df2.to_crs('epsg:3035')
        FUA_OECD = gpd.GeoDataFrame(
            pd.concat([FUA_OECD, df2], ignore_index=True))
elif geo_boundary == "UA":
    UA = gpd.read_file(
        path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
    UA = UA.to_crs('epsg:3035')

# Import Moran et al.'s data

moran = pd.read_excel(
    path_folder + "Data/Moran/allcountries_onlycities_summary.xlsx")
moran2 = pd.read_excel(path_folder + "Data/Moran/allcountries_summary.xlsx")

# Do the spatial join

list_countries = pd.read_excel(
    path_folder + "Data/Moran/moran_admin_level.xlsx")

for country in list_countries.moran_name:
    print(country)
    country = str(country)
    admin_level = str(
        list_countries.admin_level.loc[list_countries.moran_name == country].squeeze())
    moran3 = gpd.read_file(
        path_folder + "Data/Moran/allcountries.geojson/data/"+country+"/" + admin_level + ".geojson")
    moran3_with_data = moran3.merge(moran.loc[(moran.Country == country) & (
        moran.admin_level == int(admin_level)), :], left_on="rname", right_on="Region Name")
    moran3_with_data = moran3_with_data.drop_duplicates(subset="Region Name")
    moran3_with_data = moran3_with_data.to_crs('epsg:3035')

    if geo_boundary == "GHSL":
        moran_with_FUA = sjoin(FUA, moran3_with_data, how="right")
        moran_with_FUA = moran_with_FUA.loc[~np.isnan(
            moran_with_FUA.eFUA_ID), :]
        emissions_per_FUA = moran_with_FUA.loc[:, [
            'Est. Population', 'Total (t CO2)', 'buildings', 'fuelstations', 'eFUA_ID']].groupby('eFUA_ID').agg('sum')
        emissions_per_FUA = emissions_per_FUA.merge(
            FUA.loc[:, ['FUA_p_2015', 'eFUA_ID', 'eFUA_name', 'Cntry_name']], on="eFUA_ID")
        emissions_per_FUA.to_excel(
            path_folder+'Data/moran_aggregated/'+country+'.xlsx')
    elif geo_boundary == "OECD":
        moran_with_FUA = sjoin(FUA_OECD, moran3_with_data, how="right")
        moran_with_FUA = moran_with_FUA.loc[~np.isnan(
            moran_with_FUA.index_left), :]
        emissions_per_FUA = moran_with_FUA.loc[:, [
            'Est. Population', 'Total (t CO2)', 'buildings', 'fuelstations', 'fuacode']].groupby('fuacode').agg('sum')
        emissions_per_FUA = emissions_per_FUA.merge(
            FUA_OECD.loc[:, ['fuacode', 'fuaname']], on="fuacode")
        emissions_per_FUA.to_excel(
            path_folder+'Data/moran_aggregated_FUA_OECD/'+country+'.xlsx')
    elif geo_boundary == "UA":
        moran_with_FUA = sjoin(UA, moran3_with_data, how="right")
        moran_with_FUA = moran_with_FUA.loc[~np.isnan(
            moran_with_FUA.index_left), :]
        emissions_per_FUA = moran_with_FUA.loc[:, [
            'Est. Population', 'Total (t CO2)', 'buildings', 'fuelstations', 'URAU_CODE']].groupby('URAU_CODE').agg('sum')
        emissions_per_FUA = emissions_per_FUA.merge(
            UA.loc[:, ['URAU_CODE', 'URAU_NAME']], on="URAU_CODE")
        emissions_per_FUA.to_excel(
            path_folder+'Data/moran_aggregated_urban_audit/'+country+'.xlsx')

# Correct for FUAs running over different countries

if geo_boundary == "GHSL":
    df = pd.read_excel(path_folder+'Data/moran_aggregated/' +
                       'austria'+'.xlsx', index_col=0)
elif geo_boundary == "OECD":
    df = pd.read_excel(
        path_folder+'Data/moran_aggregated_FUA_OECD/' + 'austria'+'.xlsx', index_col=0)
elif geo_boundary == "UA":
    df = pd.read_excel(
        path_folder+'Data/moran_aggregated_urban_audit/' + 'austria'+'.xlsx', index_col=0)

for country in list_countries.moran_name[1:]:
    country = str(country)
    if geo_boundary == "GHSL":
        df2 = pd.read_excel(
            path_folder+'Data/moran_aggregated/' + country+'.xlsx', index_col=0)
    elif geo_boundary == "OECD":
        df2 = pd.read_excel(
            path_folder+'Data/moran_aggregated_FUA_OECD/' + country+'.xlsx', index_col=0)
    elif geo_boundary == "UA":
        df2 = pd.read_excel(
            path_folder+'Data/moran_aggregated_urban_audit/' + country+'.xlsx', index_col=0)
    df = df.append(df2)

if geo_boundary == "GHSL":
    duplicate_FUA = set(
        [x for x in df.eFUA_ID if list(df.eFUA_ID).count(x) > 1])
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = df.loc[df.eFUA_ID == id_dup, :]
        df = df.loc[df.eFUA_ID != id_dup, :]
        new_row = {'eFUA_ID': subset_dup.eFUA_ID.iloc[0], 'Est. Population': np.nansum(subset_dup["Est. Population"]), 'Total (t CO2)': np.nansum(subset_dup["Total (t CO2)"]), 'buildings': np.nansum(
            subset_dup["buildings"]), 'fuelstations': np.nansum(subset_dup["fuelstations"]), 'FUA_p_2015': subset_dup.FUA_p_2015.iloc[0], 'eFUA_name': subset_dup.eFUA_name.iloc[0], 'Cntry_name': subset_dup.Cntry_name.iloc[0]}
        df = df.append(new_row, ignore_index=True)
    df.to_excel(path_folder+'Data/moran_aggregated_FUA_GHSL/' +
                'all_countries'+'.xlsx')


elif geo_boundary == "OECD":
    duplicate_FUA = set(
        [x for x in df.fuacode if list(df.fuacode).count(x) > 1])
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = df.loc[df.fuacode == id_dup, :]
        df = df.loc[df.fuacode != id_dup, :]
        new_row = {'fuacode': subset_dup.fuacode.iloc[0], 'Est. Population': np.nansum(subset_dup["Est. Population"]), 'Total (t CO2)': np.nansum(
            subset_dup["Total (t CO2)"]), 'buildings': np.nansum(subset_dup["buildings"]), 'fuelstations': np.nansum(subset_dup["fuelstations"]), 'fuaname': subset_dup.fuaname.iloc[0]}
        df = df.append(new_row, ignore_index=True)
    df.to_excel(path_folder+'Data/moran_aggregated_FUA_OECD/' +
                'all_countries'+'.xlsx')

elif geo_boundary == "UA":
    duplicate_FUA = set(
        [x for x in df.URAU_CODE if list(df.URAU_CODE).count(x) > 1])
    for id_dup in duplicate_FUA:
        print(id_dup)
        subset_dup = df.loc[df.URAU_CODE == id_dup, :]
        df = df.loc[df.fuacode != id_dup, :]
        new_row = {'URAU_CODE': subset_dup.URAU_CODE.iloc[0], 'Est. Population': np.nansum(subset_dup["Est. Population"]), 'Total (t CO2)': np.nansum(
            subset_dup["Total (t CO2)"]), 'buildings': np.nansum(subset_dup["buildings"]), 'fuelstations': np.nansum(subset_dup["fuelstations"]), 'URAU_NAME': subset_dup.URAU_NAME.iloc[0]}
        df = df.append(new_row, ignore_index=True)
    df.to_excel(path_folder+'Data/moran_aggregated_urban_audit/' +
                'all_countries'+'.xlsx')
