# file to print basic information about each ID within dataset insitu_data.csv

import numpy as np
import pandas as pd
import insitu_cleanup as ic

# calls cleaned up file and imports as pandas dataframe
df = ic.insitu_obs()

# basic info (dates, locations, num of observations)
def info_calcs(df):
    mindate = df.index[(df.CO2.notnull()) & (df.LAT.notnull()) & (df.LON.notnull())].min()
    maxdate = df.index[(df.CO2.notnull()) & (df.LAT.notnull()) & (df.LON.notnull())].max()
    minlat = np.round(df.LAT[(df.CO2.notnull()) & (df.LAT.notnull())][mindate], decimals=2)
    maxlat = np.round(df.LAT[(df.CO2.notnull()) & (df.LAT.notnull())][maxdate], decimals=2)
    minlon = np.round(df.LON[(df.CO2.notnull()) & (df.LON.notnull())][mindate], decimals=2)
    maxlon = np.round(df.LON[(df.CO2.notnull()) & (df.LON.notnull())][maxdate], decimals=2)
    co2count = df.CO2[(df.CO2.notnull())].count()
    return mindate, maxdate, minlat, maxlat, minlon, maxlon, co2count

# prints basic info once called
def info(df, idnum):
    ob = df
    if (idnum == 8):        # want to separate ID8 since observed with large gap between years
        ob1 = ob[(ob.ID==8) & (ob.index.year == 2012)]
        ob1.ID = '8A'
        ob2 = ob[(ob.ID==8) & (ob.index.year != 2012)]
        ob2.ID = '8B'
        Amindate, Amaxdate, Aminlat, Amaxlat, Aminlon, Amaxlon, Aco2count = info_calcs(ob1)
        Bmindate, Bmaxdate, Bminlat, Bmaxlat, Bminlon, Bmaxlon, Bco2count = info_calcs(ob2) 
        print('ID Number {} info:'.format(idnum))
        print('date: ', Amindate, ' ', Amaxdate)
        print('start: ', Aminlat, ' ', Aminlon)
        print('end: ', Amaxlat, ' ', Amaxlon)
        print('num obs: ', Aco2count)      
        print('O-Buoy {} info:'.format(idnum))
        print('date: ', Bmindate, ' ', Bmaxdate)
        print('start: ', Bminlat, ' ', Bminlon)
        print('end: ', Bmaxlat, ' ', Bmaxlon)
        print('num obs: ', Bco2count)   

    else:
        ob = ob[ob.ID==idnum]
        mindate, maxdate, minlat, maxlat, minlon, maxlon, co2count = info_calcs(ob)
        print('ID Number {} info:'.format(idnum))
        print('date: ', mindate, ' ', maxdate)
        print('start: ', minlat, ' ', minlon)
        print('end: ', maxlat, ' ', maxlon)
        print('num obs: ', co2count)
    
    return None


id_numbers = [1,2,4,5,6,8,10,11,12,13,14,15]
for i in id_numbers:
    info(df, i)
    print('done.')
