# figure showing lat/lon tracks and points

import insitu_obs as ic
import co2_ms_definitions as msd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as patches
import cartopy.feature as cfeature
import shapely.geometry as sgeom
from matplotlib.pyplot import cm
font = {'fontname':'Arial'}
fsize = {'fontsize':'22'}

# dataset
ob = ic.obuoy_obs()

# map projection and data projection
proj = ccrs.NorthPolarStereo()
dataproj = ccrs.PlateCarree()

# colors for lat/lon tracks
ob_colors = msd.ob_fig_colors()[1]
ob_colors_iter = msd.ob_fig_colors()[2]

# map land points
land_data = [ ('Alert', 82.466666, -62.5, (-23,-20)),
            ('Utqiagvik', 71.323, -156.6114, (10,7)),
            ('Ny-Alesund', 78.9067, 11.8883, (0,-20)),
            ('Tiksi', 71.6, 128.9, (10,5)) ]

# call fig to draw 
def fig():
    fig = plt.figure( figsize=(7,5) )
    ax = plt.axes( projection=proj )
    ax.set_extent( [-180,180,65,90], dataproj )
    ax.add_feature( cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor=cfeature.COLORS['land']) )
    ax.coastlines( resolution='50m',color='gray',alpha=0.6 )
    # Latitude lines are every 5 degrees [90,85,80,75,70,65]
    # Longitude lines are every 60 degrees [0,60,120,180,-120,-60]
    gl = ax.gridlines( dataproj, linestyle='--', draw_labels=False, xlocs=None, ylocs=None, alpha=0.5)
    gl.n_steps = 90

    # Plot each buoy track
    for num in np.sort( ob.ID.unique() ):
        df = ob[ob.ID==num]
        c = next(ob_colors_iter)
        ax.scatter(df.LON, df.LAT, s=0.7, color=c, transform=dataproj, alpha=0.8, label='OB{}'.format(str(int(num))) )

    # Make legend for buoy tracks
    ax.legend( markerscale=10, facecolor='white', loc='lower center', ncol=4 )    

    # Plot point and label for each land station
    for name, lat, lon, textpoint in land_data:
        at_x, at_y = ax.projection.transform_point( lon, lat, src_crs=dataproj )
        t = plt.annotate(
            name, xy=(at_x, at_y), **font, **fsize, xytext=textpoint, textcoords='offset points',
            color='black', size='large' )
        t.set_bbox( dict(facecolor='white', alpha=0.95, edgecolor='white') )
        plt.plot( lon, lat, marker='o', markersize=7.0, markeredgewidth=1.5,
                 markerfacecolor='black', markeredgecolor='black',
                 transform=dataproj )
    
    # Save figure
    #plt.savefig('/Users/kgraham/OBUOY_work/co2_ms_figures/fig1-map.pdf')
    plt.show()
