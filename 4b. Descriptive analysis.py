# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:54:34 2023

@author: charl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# SCATTERPLOTS FOR ALL COUNTRIES

urban_form_metrics = urban_form_metrics.loc[urban_form_metrics.n_pop > 0, :]
urban_form_metrics2 = urban_form_metrics.loc[urban_form_metrics.volume_profile < 0, :]

GDP_per_cap = pd.read_excel(path_folder+'Data/GDP_per_cap.xlsx')
urban_form_metrics = urban_form_metrics.merge(
    GDP_per_cap, on="Country", how="left")

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log', yscale='log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, -group.volume_profile, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Volume profile")
coefs = np.polyfit(np.log(urban_form_metrics2.n_pop),
                   np.log((-urban_form_metrics2.volume_profile)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()


large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log', yscale='log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.centrality2, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Centrality index")
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.centrality2)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()


large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log')  # , yscale = 'log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.agglo_spag, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Agglomeration index")
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.agglo_spag)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log')  # , yscale = 'log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.avg_height, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Avg height")
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.avg_height)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log')  # , yscale = 'log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.gdp_per_cap, group.avg_height, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Avg height")
coefs = np.polyfit(np.log(urban_form_metrics.gdp_per_cap),
                   np.log((urban_form_metrics.avg_height)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.gdp_per_cap)), coefs[0])
plt.plot(sorted(urban_form_metrics.gdp_per_cap),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()


large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log')  # , yscale = 'log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.density_b, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Buildings density")
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.density_b)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log', yscale='log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.UA, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Urban area")
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.UA)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': large,
          'axes.titlesize': med,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.gca().set(xlabel='Population',
              xscale='log', yscale='log')
plt.style.use('seaborn-whitegrid')
groups = urban_form_metrics.groupby('Country')
for name, group in groups:
    plt.plot(group.n_pop, group.vol_per_cap, marker='o',
             linestyle='', markersize=12, label=name)
plt.legend()
plt.xlabel("Population")
plt.ylabel("Volume per capita")
plt.ylim(150, 1100)
coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                   np.log((urban_form_metrics.vol_per_cap)), 1)
pred_f = coefs[1] + \
    np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
plt.plot(sorted(urban_form_metrics.n_pop),
         np.exp(pred_f), 'k--')  # exponentiate pre
plt.show()


def export_plots(country, urban_form_metrics):
    urban_form_metrics = urban_form_metrics.loc[urban_form_metrics["Country"] == country, :]
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log', yscale='log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop,
                (-urban_form_metrics.volume_profile), s=40)
    plt.xlabel("Population")
    plt.ylabel("Volume profile")
    coefs = np.polyfit(np.log(urban_form_metrics2.n_pop),
                       np.log((-urban_form_metrics2.volume_profile)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"volume_profile.png")
    plt.close()
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log', yscale='log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop, urban_form_metrics.centrality2, s=40)
    plt.xlabel("Population")
    plt.ylabel("Centrality index")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.centrality2)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"centrality_index.png")
    plt.close()

    fig = plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log')  # , yscale = 'log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop, urban_form_metrics.agglo_spag, s=40)
    plt.xlabel("Population")
    plt.ylabel("Agglomeration index")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.agglo_spag)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    fig.savefig(path_outputs + country+"agglo_index.png")
    plt.close()


export_plots("BE", urban_form_metrics)
export_plots("CH", urban_form_metrics)
export_plots("EE", urban_form_metrics)
export_plots("ES", urban_form_metrics)
export_plots("NL", urban_form_metrics)
export_plots("PL", urban_form_metrics)
export_plots("LU", urban_form_metrics)
export_plots("SI", urban_form_metrics)
export_plots("SK", urban_form_metrics)


def export_height(country, urban_form_metrics):
    urban_form_metrics = urban_form_metrics.loc[urban_form_metrics["Country"] == country, :]
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log')  # , yscale = 'log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop,
                (urban_form_metrics.avg_height), s=40)
    plt.xlabel("Population")
    plt.ylabel("Avg height")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.avg_height)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"avg_height.png")
    plt.close()


export_height("BE", urban_form_metrics)
export_height("CH", urban_form_metrics)
export_height("EE", urban_form_metrics)
export_height("ES", urban_form_metrics)
export_height("NL", urban_form_metrics)
export_height("PL", urban_form_metrics)
export_height("LU", urban_form_metrics)
export_height("SI", urban_form_metrics)
export_height("SK", urban_form_metrics)


def export_density_b(country, urban_form_metrics):
    urban_form_metrics = urban_form_metrics.loc[urban_form_metrics["Country"] == country, :]
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log')  # , yscale = 'log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop, (urban_form_metrics.density_b), s=40)
    plt.xlabel("Population")
    plt.ylabel("Buildings_density")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.density_b)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"_density_b.png")
    plt.close()


export_density_b("BE", urban_form_metrics)
export_density_b("CH", urban_form_metrics)
export_density_b("EE", urban_form_metrics)
export_density_b("ES", urban_form_metrics)
export_density_b("NL", urban_form_metrics)
export_density_b("PL", urban_form_metrics)
export_density_b("LU", urban_form_metrics)
export_density_b("SI", urban_form_metrics)
export_density_b("SK", urban_form_metrics)


def export_vol_per_cap(country, urban_form_metrics):
    urban_form_metrics = urban_form_metrics.loc[urban_form_metrics["Country"] == country, :]
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log')  # , yscale = 'log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop,
                (urban_form_metrics.vol_per_cap), s=40)
    plt.xlabel("Population")
    plt.ylabel("Volume per capita")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.vol_per_cap)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"_vol_per_cap.png")
    plt.close()


export_vol_per_cap("BE", urban_form_metrics)
export_vol_per_cap("CH", urban_form_metrics)
export_vol_per_cap("EE", urban_form_metrics)
export_vol_per_cap("ES", urban_form_metrics)
export_vol_per_cap("NL", urban_form_metrics)
export_vol_per_cap("PL", urban_form_metrics)
export_vol_per_cap("LU", urban_form_metrics)
export_vol_per_cap("SI", urban_form_metrics)
export_vol_per_cap("SK", urban_form_metrics)


def export_urban_area(country, urban_form_metrics):
    urban_form_metrics = urban_form_metrics.loc[urban_form_metrics["Country"] == country, :]
    plt.figure()
    large = 22
    med = 16
    small = 12
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': large,
              'axes.titlesize': med,
              'xtick.labelsize': large,
              'ytick.labelsize': large,
              'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.gca().set(xlabel='Population',
                  xscale='log')  # , yscale = 'log')
    plt.style.use('seaborn-whitegrid')
    plt.scatter(urban_form_metrics.n_pop, (urban_form_metrics.UA), s=40)
    plt.xlabel("Population")
    plt.ylabel("Urban area")
    coefs = np.polyfit(np.log(urban_form_metrics.n_pop),
                       np.log((urban_form_metrics.UA)), 1)
    pred_f = coefs[1] + \
        np.multiply(sorted(np.log(urban_form_metrics.n_pop)), coefs[0])
    plt.plot(sorted(urban_form_metrics.n_pop),
             np.exp(pred_f), 'k--')  # exponentiate pre
    plt.savefig(path_outputs + country+"_urban_area.png")
    plt.close()


export_urban_area("BE", urban_form_metrics)
export_urban_area("CH", urban_form_metrics)
export_urban_area("EE", urban_form_metrics)
export_urban_area("ES", urban_form_metrics)
export_urban_area("NL", urban_form_metrics)
export_urban_area("PL", urban_form_metrics)
export_urban_area("LU", urban_form_metrics)
export_urban_area("SI", urban_form_metrics)
export_urban_area("SK", urban_form_metrics)
