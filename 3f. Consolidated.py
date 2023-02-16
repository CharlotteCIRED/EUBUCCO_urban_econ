# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 15:51:09 2023

@author: charl
"""

import pandas as pd
import numpy as np
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '')

###### OECD FUA

#moran
moran_OECD = pd.read_excel(path_folder+'Data/moran_aggregated_FUA_OECD/'+'all_countries'+'.xlsx')
moran_OECD = moran_OECD.loc[:,['fuacode', 'fuaname', 'Est. Population', 'Total (t CO2)',
       'buildings', 'fuelstations']]
moran_OECD.columns = ['fuacode', 'fuaname', 'population_moran', 'scope1_moran',
       'buildings_moran', 'transport_moran']

#nangini
nangini_OECD = pd.read_excel(path_folder+'Data/nangini_FUA_OECD.xlsx')
nangini_OECD = nangini_OECD.loc[:,['Scope-1 GHG emissions [tCO2 or tCO2-eq]',
       'Total emissions (CDP) [tCO2-eq]',
       'Population (others)', 'Population (CDP)', 'fuacode']]
nangini_OECD.columns = ['scope1_nangini', 'total_emissions_nangini', 'population2_nangini', 'population1_nangini', 'fuacode']

#kona
kona_OECD = pd.read_excel(path_folder+'Data/kona_FUA_OECD.xlsx')
kona_OECD["emissions_kona"] = np.nansum(kona_OECD.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions',
       'Manufacturing and construction industriesindirect_emissions']], 1)

kona_OECD["buildings_kona"] = np.nansum(kona_OECD.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_OECD["transport_kona"] = np.nansum(kona_OECD.loc[:,[
       'Transportationdirect_emissions',
       'Transportationindirect_emissions']], 1)

kona_OECD["emissions_scope1_kona"] = np.nansum(kona_OECD.loc[:,[
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions']], 1)

kona_OECD["buildings_scope1_kona"] = np.nansum(kona_OECD.loc[:,[
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_OECD["transport_scope1_kona"] = np.nansum(kona_OECD.loc[:,[
       'Transportationdirect_emissions']], 1)

kona_OECD = kona_OECD.loc[:,['fuacode','population_in_the_inventory_year','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']]
kona_OECD.columns = ['fuacode','population_kona','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']

#huo
huo_OECD = pd.read_excel(path_folder+'Data/huo_OECD.xlsx')
huo_OECD = huo_OECD.loc[:,['transport', 'residential', 'fuacode']]
huo_OECD.columns = ['transport_huo', 'residential_huo', 'fuacode']

#consolidated OECD
consolidated_OECD = moran_OECD.merge(huo_OECD, on = "fuacode", how = "outer")
consolidated_OECD = consolidated_OECD.merge(kona_OECD, on = "fuacode", how = "outer")
consolidated_OECD = consolidated_OECD.merge(nangini_OECD, on = "fuacode", how = "outer")

summary = consolidated_OECD.describe()

consolidated_OECD.to_excel(path_folder+'Data/consolidated_FUA_OECD.xlsx')

#### URBAN AUDIT

#moran
moran_UA = pd.read_excel(path_folder+'Data/moran_aggregated_urban_audit/'+'all_countries'+'.xlsx')
moran_UA = moran_UA.loc[:,['URAU_CODE','URAU_NAME', 'Est. Population', 'Total (t CO2)',
       'buildings', 'fuelstations']]
moran_UA.columns = ['URAU_CODE', 'URAU_NAME', 'population_moran', 'scope1_moran',
       'buildings_moran', 'transport_moran']

#nangini
nangini_UA = pd.read_excel(path_folder+'Data/nangini_urban_audit.xlsx')
nangini_UA = nangini_UA.loc[:,['Scope-1 GHG emissions [tCO2 or tCO2-eq]',
       'Total emissions (CDP) [tCO2-eq]',
       'Population (others)', 'Population (CDP)', 'URAU_CODE']]
nangini_UA.columns = ['scope1_nangini', 'total_emissions_nangini', 'population2_nangini', 'population1_nangini', 'URAU_CODE']

#kona
kona_UA = pd.read_excel(path_folder+'Data/kona_urban_audit.xlsx')
kona_UA["emissions_kona"] = np.nansum(kona_UA.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions',
       'Manufacturing and construction industriesindirect_emissions']], 1)

kona_UA["buildings_kona"] = np.nansum(kona_UA.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_UA["transport_kona"] = np.nansum(kona_UA.loc[:,[
       'Transportationdirect_emissions',
       'Transportationindirect_emissions']], 1)

kona_UA["emissions_scope1_kona"] = np.nansum(kona_UA.loc[:,[
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions']], 1)

kona_UA["buildings_scope1_kona"] = np.nansum(kona_UA.loc[:,[
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_UA["transport_scope1_kona"] = np.nansum(kona_UA.loc[:,[
       'Transportationdirect_emissions']], 1)

kona_UA = kona_UA.loc[:,['URAU_CODE','population_in_the_inventory_year','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']]
kona_UA.columns = ['URAU_CODE','population_kona','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']

#Khomenkho
pollution = pd.read_excel(path_folder+'Data/pollution.xlsx')
pollution = pollution.loc[:, ['Ranking position [PM2.5]', 'Ranking position [NO2]','PM2.5 [annual mean]','NO2 [annual mean]','URAU_CODE']]
pollution.columns = ["rank_PM25", "rank_NO2", "PM25", "NO2", "URAU_CODE"]

green_space = pd.read_excel(path_folder+'Data/green_space.xlsx')
green_space = green_space.loc[:,['Ranking position [NDVI]', 'Ranking position [%GA]','% Population below NDVI target [NDVI]','% Population below %GA target [%GA]','URAU_CODE']]
green_space.columns = ['rank_NDVI', 'rank_GA', 'pop_NDVI', 'pop_GA', 'URAU_CODE']


noise = pd.read_excel(path_folder+'Data/noise.xlsx')
noise = noise.loc[:,['% population exposed > 55 dB Lden', 'URAU_CODE']]
noise.columns = ['pop_noise', 'URAU_CODE']

#consolidated UA
consolidated_UA = moran_UA.merge(nangini_UA, on = "URAU_CODE", how = "outer")
consolidated_UA = consolidated_UA.merge(kona_UA, on = "URAU_CODE", how = "outer")
consolidated_UA = consolidated_UA.merge(pollution, on = "URAU_CODE", how = "outer")
consolidated_UA = consolidated_UA.merge(green_space, on = "URAU_CODE", how = "outer")
consolidated_UA = consolidated_UA.merge(noise, on = "URAU_CODE", how = "outer")

summary = consolidated_UA.describe()

consolidated_UA.to_excel(path_folder+'Data/consolidated_urban_audit.xlsx')

###### GHSL FUA

#moran
moran_GHSL = pd.read_excel(path_folder+'Data/moran_aggregated_FUA_GHSL/'+'all_countries'+'.xlsx')
moran_GHSL = moran_GHSL.loc[:,['eFUA_ID', 'eFUA_name', 'Est. Population', 'Total (t CO2)',
       'buildings', 'fuelstations']]
moran_GHSL.columns = ['eFUA_ID', 'eFUA_name', 'population_moran', 'scope1_moran',
       'buildings_moran', 'transport_moran']

#nangini
nangini_GHSL = pd.read_excel(path_folder+'Data/nangini_FUA_GHSL.xlsx')
nangini_GHSL = nangini_GHSL.loc[:,['Scope-1 GHG emissions [tCO2 or tCO2-eq]',
       'Total emissions (CDP) [tCO2-eq]',
       'Population (others)', 'Population (CDP)', 'eFUA_ID']]
nangini_GHSL.columns = ['scope1_nangini', 'total_emissions_nangini', 'population2_nangini', 'population1_nangini', 'eFUA_ID']

#kona
kona_GHSL = pd.read_excel(path_folder+'Data/kona_FUA_GHSL.xlsx')
kona_GHSL["emissions_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Transportationindirect_emissions', 'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions',
       'Manufacturing and construction industriesindirect_emissions']], 1)

kona_GHSL["buildings_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Municipal buildings and facilitiesindirect_emissions',
       'Institutional/tertiary buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesindirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_GHSL["transport_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Transportationdirect_emissions',
       'Transportationindirect_emissions']], 1)

kona_GHSL["emissions_scope1_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Transportationdirect_emissions',
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Waste/wastewaterdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions',
       'Manufacturing and construction industriesdirect_emissions']], 1)

kona_GHSL["buildings_scope1_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Residential buildings and facilitiesdirect_emissions',
       'Municipal buildings and facilitiesdirect_emissions',
       'Institutional/tertiary buildings and facilitiesdirect_emissions']], 1)

kona_GHSL["transport_scope1_kona"] = np.nansum(kona_GHSL.loc[:,[
       'Transportationdirect_emissions']], 1)

kona_GHSL = kona_GHSL.loc[:,['eFUA_ID','population_in_the_inventory_year','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']]
kona_GHSL.columns = ['eFUA_ID','population_kona','emissions_kona', 'buildings_kona', 'transport_kona', 'emissions_scope1_kona', 'buildings_scope1_kona', 'transport_scope1_kona']

#huo
huo_GHSL = pd.read_excel(path_folder+'Data/huo_GHSL.xlsx')
huo_GHSL = huo_GHSL.loc[:,['transport', 'residential', 'eFUA_ID']]
huo_GHSL.columns = ['transport_huo', 'residential_huo', 'eFUA_ID']

#consolidated OECD
consolidated_GHSL = moran_GHSL.merge(huo_GHSL, on = "eFUA_ID", how = "outer")
consolidated_GHSL = consolidated_GHSL.merge(kona_GHSL, on = "eFUA_ID", how = "outer")
consolidated_GHSL = consolidated_GHSL.merge(nangini_GHSL, on = "eFUA_ID", how = "outer")

summary = consolidated_GHSL.describe()

consolidated_GHSL.to_excel(path_folder+'Data/consolidated_FUA_GHSL.xlsx')
