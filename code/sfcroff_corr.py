import time
import re
import os
import pickle
import glob
import xarray as xr

def pretime(ds): 
    ds = ds.expand_dims('Time')
    ds['HGT'] = (("south_north", "west_east"), hgt.values)
    return ds


def sfcroff_corr(file_dir, var='mo_avg_T2'):

    # directory of files
    ds_hgt = xr.open_dataset('/nesi/project/uoo03104/amps_daily/dailyavg_summerd03/ds_clim_dailystats_d0320180205.nc')
    hgt = ds_hgt.avg_HGTd0320180205

    files_avg = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlyavg_summerd03/*')
    files_avg.sort()

    files_sfroff = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/*')
    files_sfroff.sort()

    ds_avg = xr.open_mfdataset(files_avg, concat_dim='Time', combine='nested', preprocess = pretime)
    ds_sfroff = xr.open_mfdataset(files_sfroff, concat_dim='Time', combine='nested', preprocess = pretime)

    mask_sfroff = ds_sfroff['mo_avgsum_SFROFF'].where(ds_sfroff.HGT>0.0)
    mask_avg = ds_avg[var].where(ds_sfroff.HGT>0.0)

    #compute corr
    cor = xr.corr(mask_sfroff, mask_avg, dim='Time')
