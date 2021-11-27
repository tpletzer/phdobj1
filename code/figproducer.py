import defopt
import xarray as xr
import re
import glob
import math
import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file

def get_varproj(ds_grid, ds_clim, var):
    ds_data = xr.open_dataset(ds_clim)

    ds_data = ds_data.expand_dims('Time')

    #ds_grid = ds_grid.rename_dims({'time':'Time'})
    # ds_grid = ds_grid.drop_dims('soil_layers')  ##this is only if its og wrf data not just sfc fields
    # ds_grid = ds_grid.drop_dims('bottom_top')

    ds_new = ds_grid.merge(ds_data[var], combine_attrs="override")

    return ds_new

def get_monthyear(filename):
    m = re.search(r'(\d\d\d\d)(\d\d)\.nc$', filename)
    month = m.group(2)
    year = m.group(1)

    return month, year

def main(*, varname: str, wrfgridfile: str, inputfiles: str, outputfile: str):
    """
    Plotting subplots

    @param varname (str) variable name
    @param wrfgridfile (str) wrf file with grid info
    @param inputfiles (str) input files
    @param outputfile (str) name of output file

    """

    ds_grid = xr.open_dataset(wrfgridfile)


    files = glob.glob(inputfiles)

    nmonth = len(files)
    ncol = 2
    nrow= int(math.ceil(nmonth/ncol))

    fig, axes = plt.subplots(nrow, ncol)
    fig.suptitle(varname)
    for iplot in range(nmonth):
        i = iplot // ncol
        j = iplot % ncol
        ds_new = get_varproj(ds_grid=ds_grid, ds_clim=files[iplot], var=varname)
        axes[i, j].pcolormesh(ds_new[varname].isel(Time=0)) 
        month, year = get_monthyear(files[iplot])
        #axes[i, j].title(f'{year}-{month}')

    plt.show()

if __name__=='__main__':
    defopt.run(main)