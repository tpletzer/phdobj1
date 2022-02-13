import time
import re
import os
import pickle
import glob
import xarray as xr

def pretime(ds): 
    ds_hgt = xr.open_dataset('/nesi/project/uoo03104/amps_daily/dailyavg_summerd03/ds_clim_dailystats_d0320180205.nc')
    hgt = ds_hgt.avg_HGTd0320180205
    ds = ds.expand_dims('Time')
    ds['HGT'] = (("south_north", "west_east"), hgt.values)
    return ds


def sfcroff_corr(file_dir='/nesi/project/uoo03104/amps_monthly/'):

    # directory of files
    ds_hgt = xr.open_dataset('/nesi/project/uoo03104/amps_daily/dailyavg_summerd03/ds_clim_dailystats_d0320180205.nc')
    hgt = ds_hgt.avg_HGTd0320180205

    files_avg = glob.glob(file_dir + 'monthlyavg_summerd03/*.nc')
    files_avg.sort()

    files_sfroff = glob.glob(file_dir + 'monthlysumrunoff2_summerd03/*.nc')
    files_sfroff.sort()

    ds_avg = xr.open_mfdataset(files_avg, concat_dim='Time', combine='nested', preprocess = pretime)
    ds_sfroff = xr.open_mfdataset(files_sfroff, concat_dim='Time', combine='nested', preprocess = pretime)

    mf_ds = xr.Dataset()

    for v in ds_avg.var():
        if v.startswith("mo_avg_"):
            print(v)
            mask_sfroff = ds_sfroff['mo_avgsum_SFROFF'].where(ds_sfroff.HGT>0.0)
            mask_avg = ds_avg[v].where(ds_sfroff.HGT>0.0)

            #compute corr
            cor = xr.corr(mask_sfroff, mask_avg, dim='Time')
            mf_ds['cor_' + v] = (("south_north", "west_east"), cor.values)
        else:
            continue


    mf_ds.to_netcdf(file_dir + 'sfroffcor_' + '.nc')
    mf_ds.close()


sfcroff_corr()


