# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 17:20:33 2022

@author: charl
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import sjoin
import copy
from sklearn import linear_model
import math
from os import listdir
import rioxarray as rxr
from shapely.geometry import mapping
import os
import matplotlib.pyplot as plt
from joypy import joyplot

path_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '')
folder_FUA = path_folder + "Data/EUBUCCO_by_OECD_FUA/"
path_outputs = path_folder + "Sorties/charts/"

# CHOOSE COUNTRY AND IMPORT DATA FOR THIS COUNTRY

country = "PL"

res = []
# Iterate directory
for file in listdir(folder_FUA):
    # check only text files
    if (file.endswith('.shp') & file.startswith(country)):
        res.append(file)

d = {}
for name_FUA in res:

    d[str(name_FUA)] = gpd.read_file(folder_FUA + name_FUA)


path_FUA_OECD = path_folder + "Data/FUA_OECD/"
oecd_countries = listdir(path_FUA_OECD)
FUA_OECD = gpd.read_file(path_FUA_OECD + "AUT/AUT_core_commuting.shp")
FUA_OECD = FUA_OECD.to_crs('epsg:3035')
for country in oecd_countries[1:24]:
    df2 = gpd.read_file(path_FUA_OECD + country + "/" +
                        country + "_core_commuting.shp")
    df2 = df2.to_crs('epsg:3035')
    FUA_OECD = gpd.GeoDataFrame(pd.concat([FUA_OECD, df2], ignore_index=True))

GHS_cent_file = gpd.read_file(
    "C:/Users/charl/OneDrive/Bureau/EUBUCCO/Data/GHS_STAT_UCDB2015MT_GLOBE_R2019A/GHS_STAT_UCDB2015MT_GLOBE_R2019A_V1_2.gpkg")
GHS_cent_file = GHS_cent_file.to_crs('epsg:3035')

country = "PL"

# DATA CLEANING

for name_FUA in res:
    print(name_FUA)
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")
    d[name_FUA]["buildings_area"] = d[name_FUA].area
    d[name_FUA]["height"] = d[name_FUA]["height"].astype(float)
    d[name_FUA]["volume"] = d[name_FUA]["buildings_area"] * d[name_FUA]["height"]

print("Missing height feature:")
for name_FUA in res:
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")
    print(name_FUA)
    print(100 * sum(np.isnan(d[name_FUA]["height"]))/len(d[name_FUA]), "%")

for name_FUA in res:
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")
    d[name_FUA] = d[name_FUA].loc[(d[name_FUA]["buildings_area"] > 4) & (
        d[name_FUA]["buildings_area"] < 100000) & (d[name_FUA]["height"] > 2) & (d[name_FUA]["height"] < 320), :]

# DESCRIPTIVE STATISTICS

df = pd.DataFrame(columns=["city", "buildings_area", "height", "fuaname"])
for name_FUA in res:
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")
    d[name_FUA]["city"] = str(name_FUA)
    df = df.append(
        d[name_FUA].loc[:, ["city", "buildings_area", "height", "fuaname"]])

plt.figure()
plt.rcParams.update({'font.size': 12})
joyplot(
    data=df.loc[:, ['fuaname', 'buildings_area']],
    by='fuaname',
    figsize=(12, 12),
    x_range=([4, 1000]), ylim='own',
    title="Buildings area", fade=True

)
plt.savefig(path_outputs+country+"chart1.png")
plt.close()

plt.figure()
plt.rcParams.update({'font.size': 12})
joyplot(
    data=df.loc[:, ['fuaname', 'height']],
    by='fuaname',
    figsize=(12, 12),
    x_range=([0, 25]), ylim='own',
    title="Height", fade=True

)
plt.savefig(path_outputs+country+"chart2.png")
plt.close()

urban_form_metrics = pd.DataFrame(index=res, columns=['n_buildings', 'n_pop', 'UA', 'BA', 'BV', 'density_b',
                                  'avg_height', 'vol_per_cap', 'volume_profile', 'footprint_profile', 'centrality1', 'centrality2', 'agglo_spag'])
urban_form_metrics.index = urban_form_metrics.index.str.replace("/", "-")


def crop_density(raster_name):
    try:
        crop_extent = FUA_OECD.loc[FUA_OECD.fuaname == gdf.fuaname.iloc[0], :]
        raster = rxr.open_rasterio(path_folder + raster_name)
        tiff_clipped = raster.rio.clip(
            crop_extent.geometry.apply(mapping), crop_extent.crs)
        tiff_clipped.data[tiff_clipped.data < 0] = 0
        pop_raster = (np.nansum(tiff_clipped))
    except:
        pop_raster = 0
    return pop_raster


for name_FUA in res:
    print(name_FUA)
    name_FUA_old = name_FUA
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")

    gdf = d[name_FUA]

    # 1. DESCRIPTIVE STATISTICS OVER THE DATABASE

    nb_tot_buildings = len(gdf)

    # 2. PHYSICAL CHARACTERISTICS OF THE BUILT ENVIRONMENT

    BA = np.nansum(gdf["buildings_area"])
    gdf["volume"] = gdf["buildings_area"] * gdf["height"]
    BV = np.nansum(gdf["volume"])

    pop_raster1 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C21/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C21.tif')
    pop_raster2 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C20/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C20.tif')
    pop_raster3 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C19/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C19.tif')
    pop_raster4 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C18/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R5_C18.tif')
    pop_raster5 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C21/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C21.tif')
    pop_raster6 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C20/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C20.tif')
    pop_raster7 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C19/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C19.tif')
    pop_raster8 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C18/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R4_C18.tif')
    pop_raster9 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C21/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C21.tif')
    pop_raster10 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C20/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C20.tif')
    pop_raster11 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C19/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C19.tif')
    pop_raster12 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C18/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R3_C18.tif')
    pop_raster13 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C21/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C21.tif')
    pop_raster14 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C20/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C20.tif')
    pop_raster15 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C19/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C19.tif')
    pop_raster16 = crop_density(
        'Data/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C18/GHS_POP_E2015_GLOBE_R2022A_54009_1000_V1_0_R2_C18.tif')

    N = pop_raster1 + pop_raster2 + pop_raster3 + pop_raster4 + pop_raster5 + pop_raster6 + pop_raster7 + pop_raster8 + \
        pop_raster9 + pop_raster10 + pop_raster11 + pop_raster12 + \
        pop_raster13 + pop_raster14 + pop_raster15 + pop_raster16
    UA = FUA_OECD.loc[FUA_OECD.fuaname == gdf.fuaname.iloc[0], :].area
    density_buildings = BA/UA.squeeze()
    avg_height = BV/BA
    volume_per_capita = BV/N

    # SAVE

    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'n_buildings'] = nb_tot_buildings
    urban_form_metrics.loc[urban_form_metrics.index == name_FUA, 'n_pop'] = N
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'UA'] = UA.squeeze()
    urban_form_metrics.loc[urban_form_metrics.index == name_FUA, 'BA'] = BA
    urban_form_metrics.loc[urban_form_metrics.index == name_FUA, 'BV'] = BV
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'density_b'] = density_buildings
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'avg_height'] = avg_height
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'vol_per_cap'] = volume_per_capita

for name_FUA in res:
    print(name_FUA)
    name_FUA_old = name_FUA
    if name_FUA.find('/') != -1:
        name_FUA = name_FUA.replace("/", "-")

    # 3. CENTRALITY/MONOCENTRICITY

    gdf = d[name_FUA]

    #GHS_cent = GHS_cent_file.loc[GHS_cent_file.UC_NM_MN == gdf.fuaname.iloc[0],:]

    #gdf_center = sjoin(gdf.drop(columns = "index_right"), GHS_cent, how='left')

    #gdf_centroid = copy.deepcopy(gdf_center)
    gdf_centroid = copy.deepcopy(gdf)
    gdf_centroid["geometry"] = gdf_centroid.centroid

    cx = np.average(gdf_centroid["geometry"].x[~np.isnan(
        gdf_centroid["volume"])], weights=gdf_centroid["volume"][~np.isnan(gdf_centroid["volume"])])
    cy = np.average(gdf_centroid["geometry"].y[~np.isnan(
        gdf_centroid["volume"])], weights=gdf_centroid["volume"][~np.isnan(gdf_centroid["volume"])])
    center_gdf2 = gpd.GeoSeries((Point(cx, cy)))

    # centrality_index
    gdf["distance_center"] = gdf.distance(center_gdf2.geometry[0])
    avg_dist = np.average(a=gdf["distance_center"][~np.isnan(
        gdf["volume"])], weights=gdf["volume"][~np.isnan(gdf["volume"])])
    R1 = np.sqrt(np.nansum(gdf["buildings_area"])/np.pi)
    R2 = np.sqrt(UA/np.pi)

    centrality_index1 = avg_dist/R1
    centrality_index2 = avg_dist/R2

    # SAVE

    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'centrality1'] = centrality_index1
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'centrality2'] = centrality_index2.squeeze()

    # density profile

    max_dist = math.ceil(np.nanmax(gdf["distance_center"])/1000)
    buffer_df = pd.DataFrame(columns=[
                             "dist_center", "volume", "footprint", "area_buffer"], index=np.arange(1, max_dist+1))
    buffer_df.dist_center = buffer_df.index
    for i in buffer_df.index:
        print(i)
        buffer = center_gdf2.buffer(i*1000)
        buffer_df.area_buffer.loc[buffer_df.dist_center == i] = buffer[0].intersection(
            FUA_OECD.loc[FUA_OECD.fuaname == gdf.fuaname.iloc[0], :].geometry.iloc[0]).area

        inter_buffer = sjoin(gdf, gpd.GeoDataFrame(
            geometry=buffer), how='inner')
        buffer_df.volume.loc[buffer_df.dist_center ==
                             i] = np.nansum(inter_buffer.volume)
        buffer_df.footprint.loc[buffer_df.dist_center ==
                                i] = np.nansum(inter_buffer.buildings_area)

    for i in (np.arange(max_dist, 1, -1)):
        buffer_df.volume.loc[buffer_df.dist_center == i] = buffer_df.volume.loc[buffer_df.dist_center == i].squeeze(
        ) - buffer_df.volume.loc[buffer_df.dist_center == i-1].squeeze()
        buffer_df.area_buffer.loc[buffer_df.dist_center == i] = buffer_df.area_buffer.loc[buffer_df.dist_center == i].squeeze(
        ) - buffer_df.area_buffer.loc[buffer_df.dist_center == i-1].squeeze()
        buffer_df.footprint.loc[buffer_df.dist_center == i] = buffer_df.footprint.loc[buffer_df.dist_center == i].squeeze(
        ) - buffer_df.footprint.loc[buffer_df.dist_center == i-1].squeeze()

    buffer_df["gradient_volume"] = buffer_df.volume / buffer_df.area_buffer
    buffer_df["gradient_footprint"] = buffer_df.footprint / \
        buffer_df.area_buffer

    model = linear_model.LinearRegression()
    results_model = model.fit(np.array(buffer_df.dist_center).reshape(-1, 1)[buffer_df["gradient_volume"].astype(float) > 0], np.log(buffer_df["gradient_volume"].astype(
        float))[buffer_df["gradient_volume"].astype(float) > 0], buffer_df["gradient_volume"].astype(float)[buffer_df["gradient_volume"].astype(float) > 0])
    volume_profile = results_model.coef_

    model = linear_model.LinearRegression()
    results_model = model.fit(np.array(buffer_df.dist_center).reshape(-1, 1)[buffer_df["gradient_footprint"].astype(float) > 0], np.log(buffer_df["gradient_footprint"].astype(
        float))[buffer_df["gradient_footprint"].astype(float) > 0], (buffer_df["gradient_footprint"].astype(float))[buffer_df["gradient_footprint"].astype(float) > 0])
    footprint_profile = results_model.coef_

    # SAVE

    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'volume_profile'] = volume_profile
    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'footprint_profile'] = footprint_profile

    gdf_centroid = copy.deepcopy(gdf)
    gdf_centroid["geometry"] = gdf_centroid.centroid

    coef_radius = (UA.squeeze() / np.nansum(gdf_centroid["volume"]))

    gdf_centroid["areas_for_spag"] = gdf_centroid["volume"] * coef_radius
    gdf_centroid["radius_spag"] = np.sqrt(
        gdf_centroid["areas_for_spag"] / np.pi)

    gdf_centroid['geometry'] = gdf_centroid.buffer(
        gdf_centroid['radius_spag'], resolution=16)

    spag = gdf_centroid.dissolve()
    agglo_spag = spag.area.squeeze() / UA.squeeze()

    # SAVE

    urban_form_metrics.loc[urban_form_metrics.index ==
                           name_FUA, 'agglo_spag'] = agglo_spag


urban_form_metrics.to_excel(path_outputs+country+"UFM.xlsx")
