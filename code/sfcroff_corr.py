import time
import re
import os
import pickle
import glob
import xarray as xr

def pretime(ds):
    ds = ds.expand_dims('Time')
    return ds

def addfield_ds(file_avg, file_sfroff):
    ## create a ds merges two fields together that have the same timestep
    ds1 = xr.open_dataset(file_avg)
    ds2 = xr.open_dataset(file_sfroff)
    ds1['mo_avgsum_SFROFF'] = (("south_north", "west_east"), ds2['mo_avgsum_SFROFF'].values)
    mf_ds.to_netcdf('/nesi/nobackup/uoo03104/temp/file_avg')

    return ds1


def sfcroff_corr(file_dir, var):

    # directory of files
    files = glob.glob('/nesi/project/uoo03104/temp/*')
    files.sort()
    
    #dataset of the two vars for the same timesteps and sorted (need netcdfs for each time with both fields eg. append to avg)

    #land mask and ice shelf mask

    #compute corr

    #return corr

    ds = xr.open_mfdataset(files, concat_dim='Time', combine='nested', )

    cor = xr.corr(ds.mo_maxsum_SFROFF, ds.mo_avgsum_SFROFF, dim='Time')