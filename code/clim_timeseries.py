#script to produce timeseries plot of atmospheric variables from AMPS using mean daily 

import xarray as xr
import re
import glob
import math
import defopt
from datetime import datetime, timedelta

def create_df(file_dir):
    #open files in  df

def time_shift(file):
    #convert from forecast time to UTC
    #file name: sfc
    date = file.split('/')[-1].split('_')[-2] #split the file name if regrid #'regrid_d03_2015011000_f027.nc' or #sfc
    date_and_time= datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]), hour=int(date[8:10]))

    f_hour = re.match(r'^(\w\w)(\w\w).*$', file.split('/')[-1].split('_')[-1].split('.')[0])
    f_hour = int(f_hour.group(2))

    time_change = timedelta(hours=f_hour)
    new_time = date_and_time + time_change

    return date_and_time


def calc_meandaily(var='T2', domain='RSR'):
    # open files and calculate the mean daily for a given variable and region




def clim_time():







