import xarray as xr
import re
import glob
import math
import defopt


def degdayszn(*, szn1: str='2016', szn2: str='2017'):

    daily_dir = '/nesi/project/uoo03104/amps_daily/dailyavg_summerd03/'

    files = glob.glob(daily_dir + '/ds_clim_dailystats_d03' + szn1 + '1[1-2]??.nc')
    files.extend(glob.glob(daily_dir + '/ds_clim_dailystats_d03' + szn2 + '0[1-3]??.nc')) #list of files for 2016/2017 season

    daily_ds = xr.open_mfdataset(files)



    change_var = {} # make dict to remove day from variable name eg. keys: 'std_LHd03201902' items: 'std_LHd03201902[0-3][0-9]'
    for v in list(daily_ds.var()):
        if v.startswith('avg_T2'):
            change_var[v[:-11]]=change_var.get(v[:-11],[])
            change_var[v[:-11]].append(v)
        else:
            continue

    daily_ds = daily_ds.expand_dims('Time')

    change_var_keys = list(change_var)

    ds = xr.Dataset()

    ds[change_var_keys[0]] = xr.concat([daily_ds[v] for v in daily_ds.var() if v.startswith(change_var_keys[0])], dim = 'Time')

    mf_ds = xr.Dataset()

    mf_ds[szn1[2:] + szn2[2:] + 'degdays270'] = (("south_north", "west_east"), xr.where(ds['avg_T2']>=270.0, ds['avg_T2'] - 270.0, 0).sum(dim='Time').values)
    mf_ds[szn1[2:] + szn2[2:] + 'degdays273'] = (("south_north", "west_east"), xr.where(ds['avg_T2']>=273.0, ds['avg_T2'] - 273.0, 0).sum(dim='Time').values)


    mf_ds.to_netcdf('/nesi/project/uoo03104/amps_longterm/ds_clim_szndegdays' + szn1[2:] + szn2[2:] + '.nc')
    mf_ds.close()

if __name__ == "__main__":
    defopt.run(degdayszn)

