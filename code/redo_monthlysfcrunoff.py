import time
import re
import os
import pickle
import glob
import xarray as xr
import defopt


def monthly_stats(*, start_index: int=0, end_index: int=-1):
    #open ym with d03201803 and daily avg files (including sumrunoff)

    #daily averages
    f = open('/nesi/project/uoo03104/pkl_data/ym2sumrofffiles.pkl', 'rb') #open dict with keys dom, year,month 35 total and files from daily stats and sum
    ym2files2 = pickle.load(f)


    #loop through the months in the dict
    keys_list = list(ym2files2)
    end_index = min(len(keys_list), end_index) 

    for i in range(start_index, end_index):  # for each month
        mf_ds = xr.Dataset() # create empty dataset
        ym = keys_list[i] #dom yr mo eg. d03202003
        print(ym)
        

        sum_ds = xr.open_mfdataset(ym2files2[ym])

        change_var = {} # make dict to remove day from variable name eg. keys: 'std_LHd03201902' items: 'std_LHd03201902[0-3][0-9]'
        for v in list(sum_ds.var()):
            change_var[v[:-2]]=change_var.get(v[:-2],[])
            change_var[v[:-2]].append(v)

        sum_ds = sum_ds.expand_dims('Time')

        change_var_keys = list(change_var)

        ds = xr.Dataset()

        for i3 in range(0, len(list(change_var))):
            ds[change_var_keys[i3][:-9]] = xr.concat([sum_ds[v] for v in sum_ds.var() if v.startswith(change_var_keys[i3])], dim = 'Time')
        
        for v2 in ds.var():
            mf_ds['mo_' + 'sum' + v2[3:]] = (("south_north", "west_east"), ds[v2].sum(dim='Time').values)
            mf_ds['mo_' + 'avgsum' + v2[3:]] = (("south_north", "west_east"), ds[v2].mean(dim='Time').values)
            mf_ds['mo_' + 'maxsum' + v2[3:]] = (("south_north", "west_east"), ds[v2].max(dim='Time').values)
            mf_ds['mo_' + 'minsum' + v2[3:]] = (("south_north", "west_east"), ds[v2].min(dim='Time').values)
            mf_ds['mo_' + 'stdsum' + v2[3:]] = (("south_north", "west_east"), ds[v2].std(dim='Time').values)
            continue

        mf_ds.to_netcdf('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/ds_clim_monthlysfcrunoff_' + ym + '.nc')
        mf_ds.close()

if __name__ == "__main__":
    defopt.run(monthly_stats)