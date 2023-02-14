# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 18:04:24 2023

@author: charl
"""

import pandas as pd
import geopandas as gpd
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '')

### Air pollution

pollution = pd.read_excel(path_folder + "Data/ISGlobal-Ranking-table-AP-GS-Noise-23032022.xlsx")
UA = gpd.read_file(path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
UA = UA.to_crs('epsg:3035')
supp = pd.read_excel(path_folder + "Data/supp_green_spaces.xlsx")
for i in range(len(pollution)):
    pollution.loc[:,"City"].iloc[i] = pollution.loc[:,"City"].iloc[i].replace(' (metropolitan area) ', ' (Greater city)')
    pollution.loc[:,"City"].iloc[i] = pollution.loc[:,"City"].iloc[i].replace(' (metropolitan area)', ' (Greater city)')

pollution = pollution.merge(supp.loc[:,["City Code", "City Name"]], left_on = "City", right_on = "City Name", how = "inner")
pollution = pollution.merge(UA, left_on = "City Code", right_on = "FID", how ="inner")
pollution.to_excel(path_folder+'Data/pollution.xlsx')

### Green space

green_space = pd.read_excel(path_folder + "Data/ISGlobal-Ranking-table-AP-GS-Noise-23032022.xlsx", sheet_name = "ISGlobalCityRanking_GreenSpace")
supp = pd.read_excel(path_folder + "Data/supp_green_spaces.xlsx")
for i in range(len(green_space)):
    green_space.loc[:,"City"].iloc[i] = green_space.loc[:,"City"].iloc[i].replace(' (metropolitan area) ', ' (Greater city)')
    green_space.loc[:,"City"].iloc[i] = green_space.loc[:,"City"].iloc[i].replace(' (metropolitan area)', ' (Greater city)')

green_space = green_space.merge(supp.loc[:,["City Code", "City Name"]], left_on = "City", right_on = "City Name", how = "inner")
UA = gpd.read_file(path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
UA = UA.to_crs('epsg:3035')
green_space = green_space.merge(UA, left_on = "City Code", right_on = "FID", how ="inner")
green_space.to_excel(path_folder+'Data/green_space.xlsx')

### Noise

noise = pd.read_excel(path_folder + "Data/ISGlobal-Ranking-table-AP-GS-Noise-23032022.xlsx", sheet_name = "ISGlobalCityRanking_Noise")
UA = gpd.read_file(path_folder + "Data/ref-urau-2018-01m.shp/URAU_LB_2018_3035_CITIES.shp")
UA = UA.to_crs('epsg:3035')
supp = pd.read_excel(path_folder + "Data/noise_supplementary.xlsx", sheet_name = "Page 2 - Baseline exposure")
for i in range(len(noise)):
    noise.loc[:,"City"].iloc[i] = noise.loc[:,"City"].iloc[i].replace(' (metropolitan area) ', ' (greater city)')
    noise.loc[:,"City"].iloc[i] = noise.loc[:,"City"].iloc[i].replace(' (metropolitan area)', ' (greater city)')
    noise.loc[:,"City"].iloc[i] = noise.loc[:,"City"].iloc[i].replace('Zürich (greater city)', 'Zürich (greater city) ')
noise = noise.merge(supp.loc[:,["City code", "City name"]], left_on = "City", right_on = "City name", how = "inner")
noise = noise.merge(UA, left_on = "City code", right_on = "FID", how ="inner")
noise.to_excel(path_folder+'Data/noise.xlsx')