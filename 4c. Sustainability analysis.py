# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:54:34 2023

@author: charl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import os

path_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '')
folder_FUA = path_folder + "Data/EUBUCCO_by_OECD_FUA/"
path_outputs = path_folder + "Sorties/charts/"

urban_form_metrics = pd.read_excel(path_outputs+"BE"+"UFM.xlsx")
urban_form_metrics.columns = ['City', 'n_buildings', 'n_pop', 'UA', 'BA', 'BV', 'density_b',
                              'avg_height', 'vol_per_cap', 'volume_profile', 'footprint_profile',
                              'centrality1', 'centrality2', 'agglo_spag']
urban_form_metrics["Country"] = "BE"

for country in ['CH', 'EE', 'ES', 'LU', 'NL', 'PL', 'SI', 'SK']:
    temp_df = pd.read_excel(path_outputs+country+"UFM.xlsx")
    temp_df.columns = ['City', 'n_buildings', 'n_pop', 'UA', 'BA', 'BV', 'density_b',
                       'avg_height', 'vol_per_cap', 'volume_profile', 'footprint_profile',
                       'centrality1', 'centrality2', 'agglo_spag']
    temp_df["Country"] = country
    urban_form_metrics = urban_form_metrics.append(temp_df)

urban_form_metrics = urban_form_metrics.loc[urban_form_metrics.n_pop > 0, :]

# Sustainability data

sustainability = pd.read_excel(path_folder+'Data/consolidated_FUA_OECD.xlsx')

# Merge
urban_form_metrics["City"] = urban_form_metrics["City"].astype(str).str[0:5]
df = urban_form_metrics.merge(
    sustainability, left_on="City", right_on="fuacode", how="left")

df["l_mor"] = np.log(df["scope1_moran"])
df["l_mor_b"] = np.log(df["buildings_moran"])
df["l_mor_t"] = np.log(df["transport_moran"])
df["l_nan"] = np.log(df["scope1_nangini"])
df["l_tot_nan"] = np.log(df["total_emissions_nangini"])
df["log_pop_nangini"] = np.log(df["population2_nangini"])
df["l_huo_t"] = np.log(df["transport_huo"])
df["l_huo_r"] = np.log(df["residential_huo"])
df["l_kon"] = np.log(df["emissions_kona"])
df["log_pop_kona"] = np.log(df["population_kona"])
df["l_kon_b"] = np.log(df["buildings_kona"])
df["l_kon_t"] = np.log(df["transport_kona"])
df["l_kon_sc1"] = np.log(df["emissions_scope1_kona"])
df["l_kon_b_sc1"] = np.log(df["buildings_scope1_kona"])
df["l_kon_t_sc1"] = np.log(df["transport_scope1_kona"])

df["log_n_pop"] = np.log(df["n_pop"])
df["log_pop_moran"] = np.log(df["population_moran"])
df["log_density_b"] = np.log(df["density_b"])
df["log_avg_height"] = np.log(df["avg_height"])
df["log_vol_per_cap"] = np.log(df["vol_per_cap"])
df["log_cent2"] = np.log(df["centrality2"])
df["log_agglo"] = np.log(df["agglo_spag"])
df["log_vol_prof"] = np.log(np.abs(df["volume_profile"]))

df_dummies = pd.get_dummies(df["Country"])
df = df.join(df_dummies)

df["log_UA"] = np.log(np.abs(df["UA"]))
df["log_BA"] = np.log(np.abs(df["BA"]))
df["log_BV"] = np.log(np.abs(df["BV"]))

df["log_gdp"] = np.log(np.abs(df["gdp_per_cap"]))

GDP_per_cap = pd.read_excel(path_folder+'Data/GDP_per_cap.xlsx')
df = df.merge(GDP_per_cap, on="Country", how="left")
df["log_gdp"] = np.log(np.abs(df["gdp_per_cap"]))

exp2 = '+ log_UA + log_vol_per_cap + log_avg_height + log_cent2 + log_vol_prof + log_agglo+ gdp_per_cap'
#exp2 = '+ log_UA + log_cent2 + log_vol_prof + log_agglo+ gdp_per_cap+ BE + CH + EE + LU + NL + PL + SI + SK'
#exp2 = '+ log_UA+ log_BA+ log_BV + log_cent2 + log_vol_prof + log_agglo + gdp_per_cap'
#exp2 = '+ log_UA+ log_BA+ log_BV + log_cent2 + log_vol_prof + log_agglo + BE + CH + EE + LU + NL + PL + SI + SK'

mod = smf.ols('l_mor ~ log_pop_moran' + exp2, data=df)
res1 = mod.fit()

mod = smf.ols('l_mor_b ~ log_pop_moran' + exp2,
              data=df.loc[(~np.isnan(df.buildings_moran)) & (df.buildings_moran > 0), :])
res2 = mod.fit()

mod = smf.ols('l_mor_t ~ log_pop_moran' + exp2, data=df)
res3 = mod.fit()

mod = smf.ols('l_nan ~ log_pop_nangini' + exp2, data=df)
res4 = mod.fit()

mod = smf.ols('l_tot_nan ~ log_pop_nangini' + exp2, data=df)
res5 = mod.fit()

mod = smf.ols('l_huo_t ~ log_n_pop' + exp2,
              data=df.loc[(~np.isnan(df.transport_huo)) & (df.transport_huo > 0), :])
res6 = mod.fit()

mod = smf.ols('l_huo_r ~ log_n_pop' + exp2,
              data=df.loc[(~np.isnan(df.residential_huo)) & (df.residential_huo > 0), :])
res7 = mod.fit()

mod = smf.ols('l_kon ~ log_pop_kona' + exp2,
              data=df.loc[(~np.isnan(df.emissions_kona)) & (df.emissions_kona > 0), :])
res8 = mod.fit()

mod = smf.ols('l_kon_b ~ log_pop_kona' + exp2,
              data=df.loc[(~np.isnan(df.buildings_kona)) & (df.buildings_kona > 0), :])
res9 = mod.fit()

mod = smf.ols('l_kon_t ~ log_pop_kona' + exp2,
              data=df.loc[(~np.isnan(df.transport_kona)) & (df.transport_kona > 0), :])
res10 = mod.fit()

mod = smf.ols('l_kon_sc1 ~ log_pop_kona' + exp2, data=df.loc[(
    ~np.isnan(df.emissions_scope1_kona)) & (df.emissions_scope1_kona > 0), :])
res11 = mod.fit()

mod = smf.ols('l_kon_b_sc1 ~ log_pop_kona' + exp2, data=df.loc[(
    ~np.isnan(df.buildings_scope1_kona)) & (df.buildings_scope1_kona > 0), :])
res12 = mod.fit()

mod = smf.ols('l_kon_t_sc1 ~ log_pop_kona' + exp2, data=df.loc[(
    ~np.isnan(df.transport_scope1_kona)) & (df.transport_scope1_kona > 0), :])
res13 = mod.fit()

dfoutput = summary_col([res1, res2, res3, res6, res7,
                       res8, res9, res10, res11, res12, res13], stars=True)
print(dfoutput)


exp2 = '+ log_UA + log_vol_per_cap + log_avg_height + log_cent2 + log_vol_prof + log_agglo+ gdp_per_cap'
#exp2 = '+ log_UA + log_cent2 + log_vol_prof + log_agglo+ gdp_per_cap+ BE + CH + EE + LU + NL + PL + SI + SK'
#exp2 = '+ log_UA+ log_BA+ log_BV + log_cent2 + log_vol_prof + log_agglo + gdp_per_cap'
#exp2 = '+ log_UA+ log_BA+ log_BV + log_cent2 + log_vol_prof + log_agglo + BE + CH + EE + LU + NL + PL + SI + SK'

mod = smf.ols('log_UA ~ log_pop_moran + log_gdp', data=df)
res1 = mod.fit()
res1.summary()
df["resid"] = res1.resid
df["predict"] = res1.fittedvalues

mod = smf.ols('l_mor ~ log_pop_moran + log_gdp + resid + predict', data=df)
res1 = mod.fit()
res1.summary()

# Explain why avg heigth and buildings density are weird (maybe try with total bldings volume and total buildings area instead?)
# Add new version of the carbon monitor data
