import re
import os
import pickle
import glob
import xarray as xr


f = open('/nesi/nobackup/uoo03104/ymdsummer_all.pkl', 'rb') #open dict with keys year,month,day
ymd2files2 = pickle.load(f)

def pretime(ds):
    if 'XTIME' in ds:   
        return ds.reset_coords('XTIME', drop=True) 
    ds = ds.expand_dims('Time')
    ds = ds.drop_vars(['LU_INDEX', 'HGT', 'LANDMASK'])
    return ds
mf_ds = xr.Dataset()
#loop through the days in the dict
for ymd, files in ymd2files2.items(): 
    ds = xr.open_mfdataset(files, preprocess = pretime, concat_dim='Time', combine='nested')
    for v in ds.var():
        # for each var, calculate the avg, std, max, min, med, lower (0.25) and upper (0.75) quartile
        mf_ds['avg_' + v + ymd] = (("south_north", "west_east"), ds[v].mean(dim='Time').values)
        mf_ds['std_' + v + ymd] = (("south_north", "west_east"), ds[v].std(dim='Time').values)
        mf_ds['med_' + v + ymd] = (("south_north", "west_east"), ds[v].median(dim='Time').values)
        mf_ds['max_' + v + ymd] = (("south_north", "west_east"), ds[v].max(dim='Time').values)
        mf_ds['min_' + v + ymd] = (("south_north", "west_east"), ds[v].min(dim='Time').values)
        mf_ds['lowq_' + v + ymd] = (("south_north", "west_east"), ds[v].chunk({'Time':None}).quantile(0.25, dim="Time").values)
        mf_ds['upq_' + v + ymd] = (("south_north", "west_east"), ds[v].chunk({'Time':None}).quantile(0.75, dim="Time").values)
        mf_ds['upexq_' + v + ymd] = (("south_north", "west_east"), ds[v].chunk({'Time':None}).quantile(0.95, dim="Time").values)
        mf_ds['lowexq_' + v + ymd] = (("south_north", "west_east"), ds[v].chunk({'Time':None}).quantile(0.05, dim="Time").values)
        if v.endswith("NC"):
            mf_ds['sum_' + v + str(ymd)] = (("south_north", "west_east"), ds[v].sum(dim='Time').values)
    mf_ds.to_netcdf('/nesi/nobackup/uoo03104/dailyavg_summerd03/ds_clim_dailystats_' + ymd + '.nc')
    print(ymd)	
