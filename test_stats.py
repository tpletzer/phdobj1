import time
import re
import os
import pickle
import glob
import xarray as xr

t0 = time.time()
#daily averages
f = open('/nesi/nobackup/uoo03104/ymdsummer_all.pkl', 'rb') #open dict with keys year,month,day
ymd2files2 = pickle.load(f)

def pretime(ds):
    if 'XTIME' in ds:   
        return ds.reset_coords('XTIME', drop=True) 
    ds = ds.expand_dims('Time')
    ds = ds.drop_vars(['LU_INDEX', 'HGT', 'LANDMASK'])
    return ds


#loop through the days in the dict
keys_list = list(ymd2files2)
i=1
ymd = keys_list[i]
files = ymd2files2[keys_list[i]] # list of the files
mf_ds = xr.Dataset() # create empty dataset
ds = xr.open_mfdataset(files, preprocess = pretime, concat_dim='Time', combine='nested')

for v in ds.var():
    print(v)

t1 = time.time()
v = 'T2'
# for each var, calculate the avg, std, max, min, med, lower (0.25) and upper (0.75) quartile
mf_ds['avg_' + v + ymd] = (("south_north", "west_east"), ds[v].mean(dim='Time').values)
mf_ds['std_' + v + ymd] = (("south_north", "west_east"), ds[v].std(dim='Time').values)
mf_ds['med_' + v + ymd] = (("south_north", "west_east"), ds[v].median(dim='Time').values)
mf_ds['max_' + v + ymd] = (("south_north", "west_east"), ds[v].max(dim='Time').values)
mf_ds['min_' + v + ymd] = (("south_north", "west_east"), ds[v].min(dim='Time').values)
q = ds[v].chunk({'Time':None}).quantile([0.05, 0.25, 0.50, 0.75, 0.95], dim="Time") 
mf_ds['q0.05_' + v + ymd] = (("south_north", "west_east"), q[0].values)
mf_ds['q0.25_' + v + ymd] = (("south_north", "west_east"), q[1].values)
mf_ds['q0.50_' + v + ymd] = (("south_north", "west_east"), q[2].values)
mf_ds['q0.75_' + v + ymd] = (("south_north", "west_east"), q[3].values)
mf_ds['q0.95_' + v + ymd] = (("south_north", "west_east"), q[4].values)

t2 = time.time()

mf_ds.to_netcdf('/nesi/nobackup/uoo03104/dailyavg_summerd03/ds_clim_dailystats_' + ymd + '.nc')

t3 = time.time()

print(t3 - t0)
print(t1 - t0)
print(t2 - t1)
print(t3 - t2)
