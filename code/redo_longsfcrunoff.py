# script to redo longterm avg sfc runoff 

import time
import re
import os
import pickle
import glob
import xarray as xr


#longterm surface runoff

def pretime(ds):
    ds = ds.expand_dims('Time')
    return ds

#summermo = ['11', '12', '01', '02', '03']

#for mo in range(0, len(summermo)):
    # files = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/*' + summermo[mo] + '.nc') ###check this
    files = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/*')
    print(files)
    mf_ds = xr.Dataset()
    ds = xr.open_mfdataset(files, preprocess = pretime, concat_dim='Time', combine='nested')
    for v2 in ds.var():
        if v2.startswith("mo_sum"):
            mf_ds['long_' + v2[3:]] = (("south_north", "west_east"), ds[v2].sum(dim='Time').values)
            mf_ds['long_' + 'avg' + v2[3:]] = (("south_north", "west_east"), ds[v2].mean(dim='Time').values)
            mf_ds['long_' + 'std' + v2[3:]] = (("south_north", "west_east"), ds[v2].std(dim='Time').values)
            mf_ds['long_' + 'max' + v2[3:]] = (("south_north", "west_east"), ds[v2].max(dim='Time').values)
            mf_ds['long_' + 'min' + v2[3:]] = (("south_north", "west_east"), ds[v2].min(dim='Time').values)
        elif v2.startswith("mo_avgsum"):
            mf_ds['long_' + 'avg' + v2[3:]] = (("south_north", "west_east"), ds[v2].mean(dim='Time').values)
            mf_ds['long_' + 'std' + v2[3:]] = (("south_north", "west_east"), ds[v2].std(dim='Time').values)
        elif v2.startswith("mo_maxsum"):
            mf_ds['long_' + v2[3:]] = (("south_north", "west_east"), ds[v2].max(dim='Time').values)
        elif v2.startswith("mo_minsum"):
            mf_ds['long_' + v2[3:]] = (("south_north", "west_east"), ds[v2].min(dim='Time').values)

        else:
            continue


mf_ds.to_netcdf('/nesi/project/uoo03104/amps_longterm/longtermsumrunoff_summerd03/ds_clim_longterm_redosfrunoff' + '.nc')

