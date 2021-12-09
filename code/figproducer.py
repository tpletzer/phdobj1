import defopt
import xarray as xr
import re
import glob
import math
import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file
import matplotlib.patches as patches
import cmocean

domains = {
    'NVL': (slice(0, 239+1), slice(871, 987)), # slice(imin, imax+1), slice(jmin, jmax+1)
    'MDV': (slice(100, 250+1), slice(553, 790)),
    'both': (slice(0, 250+1), slice(553, 987)),
    'NVL_new': (slice(84, 223+1), slice(745, 973+1)),
    'MDV_new': (slice(119, 247+1), slice(620, 722+1)),
}

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

def plotsubdoms(filename='sfc_wrfout_d03_2018021800_f023.nc', varname='HGT'):

    data = xr.open_dataset(filename)

    fig = plt.figure()
    ax = plt.axes()
    data[varname].plot(cmap='terrain', cbar_kwargs={"label": "Height (m)"}, add_labels=False)
    # ax.add_patch(patches.Rectangle((0, 871), 239, 116, alpha=0.2, color='red')) #old NVL
    # ax.add_patch(patches.Rectangle((100, 553), 150, 237, alpha=0.2, color='blue')) #old MDV
    ax.add_patch(patches.Rectangle((84, 745), 139, 228, alpha=0.2, color='red'))
    ax.add_patch(patches.Rectangle((119, 620), 128, 102, alpha=0.2, color='blue'))
    ax.add_patch(patches.Rectangle((0, 553), 250, 434, alpha=0.2, color='white'))
    plt.title('Locations of the subdomains')
    plt.show()

def onedomplot(domain = 'NVL_new', wrf_grid='sfc_wrfout_d03_2018021800_f023.nc', ds_clim='ds_clim_longtermsumrunoff.nc',
                varname='long_sum_SFROFF', t='Sum of surface runoff over seven summers (2013-2020)'):
         
     
    ds_grid = open_wrf_dataset(wrf_grid)
    ds_data = xr.open_dataset(ds_clim)
 
    ds_data = ds_data.expand_dims('Time')

    ds_grid = ds_grid.rename_dims({'time':'Time'})


    new = ds_grid.merge(ds_data[varname], combine_attrs="override")

    mask_land = new.HGT.values.reshape((1035, 675))
    mask_land = xr.where(mask_land>0.0, 1.0, 0.0)

    data = new[varname] * mask_land
    dom = domains[domain]
    sub = data[0, dom[1], dom[0]] # slice data over subdom, gives 2d array
 
 
    fig = plt.figure()
    proj = new.salem.cartopy()
    ax = plt.axes(projection=proj)
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    #ax.set_extent(new.salem.grid.extent, crs=proj) #activate to see full d03
    ax.set_title(t)

    sub.plot.pcolormesh(ax=ax, transform=proj, vmin=sub.min(), vmax=sub.max(), cmap=cmocean.cm.ice_r, 
        cbar_kwargs={"label": "surface runoff (mm)"}, add_labels=False) 
    plt.show()

def oneplot(wrf_grid='sfc_wrfout_d03_2018021800_f023.nc', ds_clim='ds_clim_longtermsumrunoff.nc',
            masked=True, v='long_sum_SFROFF', t='Sum of surface runoff over seven summers (2013-2020)'):
         
     
    ds_grid = open_wrf_dataset(wrf_grid)
    ds_data = xr.open_dataset(ds_clim)
 
    ds_data = ds_data.expand_dims('Time')

    ds_grid = ds_grid.rename_dims({'time':'Time'})


    new = ds_grid.merge(ds_data[v], combine_attrs="override")

    mask = new.HGT.values.reshape((1035, 675))
    mask = xr.where(mask>0.0, 1.0, 0.0)
 
 
    fig = plt.figure()
    proj = new.salem.cartopy()
    ax = plt.axes(projection=proj)
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.set_extent(new.salem.grid.extent, crs=proj)
    ax.set_title(t)

    if masked==True:
        t2 = (new[v].isel(Time=0))*mask
    else:
        t2 = new[v].isel(Time=0)

    t2.plot.pcolormesh(ax=ax, transform=proj, vmin=0.0, vmax=1500, cmap=cmocean.cm.ice_r, 
        cbar_kwargs={"label": "surface runoff (mm)"}, add_labels=False) 
    plt.show()

    #contourf for contourss instead


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


    #fig.suptitle(varname)
    fig = plt.figure(figsize=(8, 7))
    for iplot in range(nmonth):
        i = iplot // ncol
        j = iplot % ncol
        ds_new = get_varproj(ds_grid=ds_grid,
                             ds_clim=files[iplot],
                             var=varname)
        proj = ds_new.salem.cartopy()
        ax = plt.subplot(nrow, ncol, iplot + 1, projection=proj)
        ax.coastlines()
        ax.gridlines()
        #ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        #ax.set_extent(ds_new.salem.grid.extent, crs=proj)
        # ds_new[varname].isel(Time=0).plot.pcolormesh(ax=ax, 
        #                              transform=proj)
        ax.set_extent(ds_new.salem.grid.extent, crs=proj)
        ds_new[varname].isel(Time=0).plot(ax=ax, transform=proj)

        #month, year = get_monthyear(files[iplot])
        plt.title(f'{year}-{month}')

    plt.show()

if __name__=='__main__':
    defopt.run(main)