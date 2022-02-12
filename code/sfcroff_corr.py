import time
import re
import os
import pickle
import glob
import xarray as xr

# directory of files
files = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/*')
#dataset of the two vars for the same timesteps and sorted 

#land mask and ice shelf mask

#compute corr

#return corr

#plot fn
files = glob.glob('/nesi/project/uoo03104/amps_monthly/monthlysumrunoff2_summerd03/*')

files.sort()

ds = xr.open_mfdataset(files, concat_dim='Time', combine='nested')

cor = xr.corr(ds.mo_maxsum_SFROFF, ds.mo_avgsum_SFROFF, dim='Time')