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

def daily_stats(*, start_index: int=0, end_index: int=-1):
    #daily averages
    f = open('/nesi/nobackup/uoo03104/ymdsummer_all.pkl', 'rb') #open dict with keys year,month,day #check dir path
    ymd2files2 = pickle.load(f)

    #f = open('/nesi/nobackup/uoo03104/ymdsummer_tbd.pkl', 'rb') #open dict with files_done removed
    #ymd2files2 = pickle.load(f)

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
            # for sfcroff and udroff calculate the sum
            if v.endswith("ROFF"):
               mf_ds['sum_' + v + str(ymd)] = (("south_north", "west_east"), xr.where(ds[v]<0, 0, ds[v]).sum(dim='Time').values)
               # mf_ds['sum_' + v + str(ymd)] = (("south_north", "west_east"), ds[v].sum(dim='Time').values)
            else:
                continue
        mf_ds.to_netcdf('/nesi/nobackup/uoo03104/dailysumrunoff2_summerd03/ds_clim_dailysumrunoff_' + ymd + '.nc')
        mf_ds.close()
        print(ymd)

if __name__ == "__main__":
    defopt.run(daily_stats)