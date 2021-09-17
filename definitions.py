# definitions to make life easier when using them over and over for figs/etc.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

def monthly_mean_resample(series):
    mean = series.resample('M').mean()
    return mean

def monthly_std_resample(series):
    std = series.resample('M').std()
    return std

def daily_mean_resample(series):
    mean = series.resample('D').mean()
    return mean

def daily_std_resample(series):
    std = series.resample('D').mean()
    return std

def monthly_correlation(series):
    r = series.resample('M').apply(pd.Series.autocorr) # default lag 1
    return r

def monthly_standard_error_mean(series):
    r = monthly_correlation(series)
    n = series.resample('M').count()
    s = monthly_std_resample(series)
    sem = s / np.sqrt(n) * np.sqrt( (1+r) / (1-r) )
    return sem

def co2_tags():
    string_labels = ['Terrestrial Release', 'Terrestrial Uptake', 'Ocean Release', 'Ocean Uptake', 'Fossil Fuel', 'Biomass Burning', '$P(CO_2)$', '$CO_2$' ]
    df_labels = ['CO2terrP', 'CO2terrN', 'CO2ocnP', 'CO2ocnN', 'CO2ff', 'CO2bb', 'CO2ch', 'CO2' ]
    return string_labels, df_labels

def model_obs_diffs(obs_series, gc_series):
    diff = gc_series - obs_series
    return diff

def ob_fig_colors():
    colors = cm.tab20( np.linspace(0,1,20) )
    ob1c = colors[0]
    ob2c = colors[1]
    ob4c = colors[2]
    ob5c = colors[3]
    ob6c = colors[4]
    ob8c = colors[5]
    ob10c = colors[6]
    ob11c = colors[7]
    ob12c = colors[8]
    ob13c = colors[9]
    ob14c = colors[18]
    ob15c = colors[19]
    color_list = [ ob1c, ob2c, ob4c, ob5c, ob6c, ob8c, ob10c, ob11c, ob12c, ob13c, ob14c, ob15c ]
    color_list_iter = iter([ ob1c, ob2c, ob4c, ob5c, ob6c, ob8c, ob10c, ob11c, ob12c, ob13c, ob14c, ob15c ])
    return colors, color_list, color_list_iter

def model_color():
    colors = cm.tab20c( np.linspace(0,1,20) )
    return colors #mod_color[1]

def st_fig_colors():    
    colorsbw = [plt.cm.binary(x) for x in np.linspace(0,1,7)]
    color_list = [ colorsbw[1], colorsbw[2], colorsbw[3], colorsbw[4] ]
    color_list_iter = iter([color_list])
    return colorsbw, color_list, color_list_iter

# primarily used rather than monthly_standard_error_mean def above; this is for autocorrelated data (which i'm using!)
def sem(series):
    n = series.resample('M').count()
    s = series.resample('M').std()
    r = series.resample('M').apply(pd.Series.autocorr) # default is lag 1
    sem = s / np.sqrt(n) * np.sqrt( (1+r) / (1-r) )
    return sem
