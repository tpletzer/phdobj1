import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file
import xarray as xr


def plot_dsclim(wrf_grid = '/Users/tamarapletzer/Desktop/wrfout_d03_2019021900_f015.nc',
		 ds_clim = '/Users/tamarapletzer/Desktop/ds_clim_monthlyavg_d03201802.nc', masked=True):
    ds_grid = open_wrf_dataset(wrf_grid)
    ds_data = xr.open_dataset(ds_clim)

    ds_data = ds_data.expand_dims('Time')

    ds_grid = ds_grid.rename_dims({'time':'Time'})
    ds_grid = ds_grid.drop_dims('soil_layers')
    ds_grid = ds_grid.drop_dims('bottom_top')

    new = ds_grid.merge(ds_data.monthly_avg_avg_T2d03201802, combine_attrs="override")

    mask = new['monthly_avg_avg_T2d03201802'].where(new['LANDMASK']==1)


    plt.figure()
    proj = new.salem.cartopy()
    ax = plt.axes(projection=proj)
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.set_extent(new.salem.grid.extent, crs=proj)

    if masked==True:
         t2 = mask.isel(Time=0)
    else:
        t2 = new.monthly_avg_avg_T2d03201802.isel(Time=0)

    t2.plot.pcolormesh(ax=ax, transform=proj)
    plt.show()
