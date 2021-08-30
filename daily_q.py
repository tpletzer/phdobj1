import time
import re
import os
import pickle
import glob
import xarray as xr
import defopt


def pretime(ds):
    if 'XTIME' in ds:   
        return ds.reset_coords('XTIME', drop=True) 
    ds = ds.expand_dims('Time')
    ds = ds.drop_vars(['LU_INDEX', 'HGT', 'LANDMASK'])
    return ds

def daily_quantiles(*, start_index: int=0, end_index: int=-1):
    q_frac = [0.05, 0.25, 0.50, 0.75, 0.95]
    dst_ds = xr.open_dataset('/nesi/nobackup/uoo03104/clim_summerpost/ds_clim_d03201801.nc')
    #daily averages
    f = open('/nesi/nobackup/uoo03104/ymdsummer_all.pkl', 'rb') #open dict with keys year,month,day
    ymd2files2 = pickle.load(f)

    #loop through the days in the dict
    keys_list = list(ymd2files2)
    end_index = min(len(keys_list), end_index)
    
    for i in range(start_index, end_index):  # for each day
        mf_ds = xr.Dataset() # create empty dataset
        ymd = keys_list[i]
        print(ymd)
        files = ymd2files2[keys_list[i]] # list of the files
        ds = xr.open_mfdataset(files, preprocess = pretime, concat_dim='Time', combine='nested')
        for v in ds.var():
            print(v)
            # for each var, calculate the quantiles
            q = ds[v].chunk({'Time':None}).quantile(q_frac, dim="Time")
            for j in range(len(q_frac)):
                vname = f'q{q_frac[j]:.3f}_{v}_{ymd}' 
            	mf_ds[vname] = (("south_north", "west_east"), q[j].values)

        mf_ds.coords["XLAT"] = (("south_north", "west_east"), dst_ds.XLAT.values)
        mf_ds.coords["XLONG"] = (("south_north", "west_east"), dst_ds.XLONG.values)
        mf_ds.to_netcdf('/nesi/nobackup/uoo03104/dailyq_summerd03/ds_clim_dailyq_' + ymd + '.nc')
        mf_ds.close()
        print(ymd)

if __name__ == "__main__":
    defopt.run(daily_quantiles)
