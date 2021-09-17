# Python Packages
import pandas as pd
import numpy as np

# cleanup definition - called once to run and write file
def insitu_cleanup():
    ob = pd.read_csv('finalized_data.csv')
    ob.index = pd.to_datetime(ob['Unnamed: 0'])
    del ob['Unnamed: 0']
    del ob.index.name
    ob.index.name = 'Time'
    ob.columns = ['LAT', 'LON', 'ID', 'CO2', 'PRESS', 'TEMP', 'WDIR', 'WSPD']
        
    # Filtering test data out (Feb-May 2009)
    ob.loc['2009-02-01':'2009-05-27', :] = np.nan
    ob = ob.dropna(how='all')
    
    # Filtering out ID=3 data
    ob = ob[ob.ID != 3]
    
    # Adding in missing lat/lon for ID8
    ob8_1 = pd.read_csv( '/Users/kgraham/OB/partial/ob8_2012.csv', skiprows=1)
    ob8_2 = pd.read_csv( '/Users/kgraham/OB/partial/ob8_2015.csv', skiprows=1)
    ob8_3 = pd.read_csv( '/Users/kgraham/OB/partial/ob8_2016.csv', skiprows=1)
    test = pd.concat( [ob8_1, ob8_2, ob8_3] )
    test.columns = [ 'Time', 'LAT', 'LON', 'CO2' ]
    test.index = pd.to_datetime(test.Time)
    test = test.resample('H').mean()    # resample for hourly means 
    test['ID'] = 8
    
    # Add missing ID8 lat/lon in to main dataframe
    ob = ob.append(test,sort=True)
    
    # Removing NaN values at identical timesteps (i.e. merging lat/lon with CO2 data)
    df = ob.groupby(['Time','ID']).mean()
    df.reset_index(level=1,inplace=True)
    
    # write to file
    df.to_csv('/Users/kgraham/OB/complete_datasets/full_insitu.csv')
    
    return df
    

# data used after cleanup - program & definition called in all stats/viz projects using this dataset
def insitu_obs():
    df = pd.read_csv('/Users/kgraham/OB/complete_datasets/full_insitu.csv')
    df.index = pd.to_datetime(df.Time)  # much easier to work with pandas datetime
    df = df.drop(['Time'],axis=1)       # drop extra time column
    return df
