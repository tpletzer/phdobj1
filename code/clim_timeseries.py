#script to produce timeseries plot of atmospheric variables from AMPS using mean daily 

import xarray as xr
import re
import glob
import math
import defopt
from datetime import datetime, timedelta
import pickle


def create_df(file_dir):
    # file list of hourly files in one day

    #open files in  df

    return df

def time_shift(file):
    #convert from forecast time to UTC
    #file name: sfc
    date = file.split('/')[-1].split('_')[-2] #split the file name if regrid #'regrid_d03_2015011000_f027.nc' or #sfc
    date_and_time= datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]), hour=int(date[8:10]))

    f_hour = re.match(r'^(\w\w)(\w\w).*$', file.split('/')[-1].split('_')[-1].split('.')[0])
    f_hour = int(f_hour.group(2))

    time_change = timedelta(hours=f_hour)
    new_time = date_and_time + time_change

    new_timestr = new_time.strftime("%Y%m%d%H")

    # file_parts = file.split('.')[0].split('_') #['regrid', 'd03', '2015011000', 'f027']

    # file_new = file_parts[0] + '_' + file_parts[1] + '_' + new_timestr[0:-2] + '00_' + new_timestr[-2:] + '.nc'

    return new_timestr


def calc_daily(vars=['T2', 'Q2', 'U10', 'V10', 'SWDOWN', 'GLW', 'PSFC', 'RAINNC', 'SFROFF', 'UDROFF'],
                domains=['MDV', 'RSR', 'Soil']):
    # open files and calculate the mean and std daily for a given variables and regions



def calc_monthly(vars=['T2', 'SWDOWN'], domains=['MDV', 'RSR']):
    # open files and calculate the mean and std daily for a given variables and regions





def clim_time():
    #plot timeseries of mean daily var for 7 years

def clim_table():
    # pandas df with all avg info 

    # 

def main():

    ftime_shift = {} # keys are datetime and item is the file with forecast hour corresponding
    for file in files:  
        date_new = time_shift(file)
        ftime_shift[date_new] = file

    fday_shift = {} #keys: yyyymmdd #items: files with time shifted to fhour
    for key in ftime_shift.keys():
        fday_shift[key[:-2]]=fday_shift.get(key[:-2], [])
        fday_shift[key[:-2]].append(ftime_shift[key])



    df = create_df()








