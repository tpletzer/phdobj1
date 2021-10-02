import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file
import xarray as xr


def plot_dsclim(wrf_grid = '/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2019021900_f015.nc',
		 ds_clim = '/nesi/nobackup/uoo03104/dailyq_summerd03/ds_clim_dailyq_d0320161118.nc', masked=True):
    ds_grid = open_wrf_dataset(wrf_grid)
    ds_data = xr.open_dataset(ds_clim)

    ds_data = ds_data.expand_dims('Time')

    ds_grid = ds_grid.rename_dims({'time':'Time'})
    #ds_grid = ds_grid.drop_dims('soil_layers')
    #ds_grid = ds_grid.drop_dims('bottom_top')

    new = ds_grid.merge(ds_data['q0.950_T2_d0320161118'], combine_attrs="override")

    mask = new['q0.950_T2_d0320161118'].where(new['LANDMASK']==1)


    plt.figure()
    proj = new.salem.cartopy()
    ax = plt.axes(projection=proj)
    ax.coastlines()
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    ax.set_extent(new.salem.grid.extent, crs=proj)

    if masked==True:
         t2 = mask.isel(Time=0)
    else:
        t2 = new['q0.950_T2_d0320161118'].isel(Time=0)

    t2.plot.pcolormesh(ax=ax, transform=proj)
    plt.show()

plot_dsclim()
