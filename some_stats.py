import ccg_filter as ccgfilt      # ccgfilt program obtained at https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import insitu_cleanup as ic
import co2_ms_definitions as msd
import barrow_insituandflask_datacleanup as brwfull     # cleanup file not included in repo
from scipy import stats

# Observed OB data and plot formatting colors
ob = ic.insitu_obs()
ob_colors = msd.ob_fig_colors()[1]
mod_color = msd.model_color()

# All in situ and flask data from BRW are used to calculate the trend at Utqiagvik
brw = brwfull.brw_full() 
brw = brw.interpolate(limit_direction='both')
    # all data at BRW (insitu and flask)
    # BRW data is hourly averaged
    # same flask outliers are removed
    # BRW is linearly interpolated to obtain the trend

# Calculating the trend at Utqiagvik with all in situ and flask data
# Not used here (currently) but used in other projects; keep for reference
def brw_trend():
    brwco2 = brw
    t = np.empty((len(brwco2)))
    for i in range(0,len(brwco2.index)):
        ti = brwco2.index[i]
        if ti.year == 2012:
            t[i] = ti.year + (ti.dayofyear -1)/366.
        if ti.year == 2016:
            t[i] = ti.year + (ti.dayofyear -1)/366.
        else:
            t[i] = ti.year + (ti.dayofyear -1)/365.
    xp = t
    yp = brwco2
    filt = ccgfilt.ccgFilter(xp=xp,yp=yp)
    trend = filt.getTrendValue(xp)
    p=np.array([1,1,1,1,1,1,1])
    polyfit=ccgfilt.fitFunc(params=p,x=t,numpoly=3,numharm=2)
    trend = pd.Series(trend)
    trend.index = brwco2.index
    daily_trend = trend.resample('D').mean()
    return trend, daily_trend

# def obtained from stackoverflow?
def datetime2decimal(series):
    times = series.index
    t = np.empty((len(times)))
    for i in range(0,len(times)):
        ti = times[i]
        if ti.year == 2012:
            t[i] = ti.year + (ti.dayofyear -1)/366.
        if ti.year == 2016:
            t[i] = ti.year + (ti.dayofyear -1)/366.
        else:
            t[i] = ti.year + (ti.dayofyear -1)/365.
    return t
  
# stats example of lin regression for time series observations
def multiyear_growth(inputobs, month1, month2):
    ob_month1 = obuoy.OB[obuoy.index.month==month1]
    ob_month2 = obuoy.OB[obuoy.index.month==month2]
    oball = ob_month1.append(ob_month2)
    observed_dtime = datetime2decimal(oball)
    obm, obb, obr, obp, obsem = stats.linregress(observed_dtime, oball)
    print('Observed linear regression for {}-{}: '.format(month1,month2))
    print('slope: {}'.format(np.round(obm,decimals=2)))
    print('yint: {}'.format(np.round(obb,decimals=1)))
    print('r value: {}'.format(np.round(obr,decimals=1)))
    print('p value: {}'.format(np.round(obp,decimals=2)))
    print('standard error: {}'.format(np.round(obsem,decimals=2))   # need autocorrelated SEM definition here
    return None
