#script to produce timeseries plot of atmospheric variables from AMPS using mean daily 

import xarray as xr
import re
import glob
import math
import defopt
from datetime import datetime, timedelta
import pickle


def create_df(dayfile_list):
    # file list of hourly files in one day

    #open files in  df
    df = open_mfdataset(dayfile_list)

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


def calc_daily(df, vars):
    # open files and calculate the mean and std daily for a given variables and regions

    return df

def calc_dailyspatial(dir: str='/nesi/project/uoo03104/amps_daily/dailysumrunoff2_summerd03/', domain: str='fulldom'):
    """
    Computes daily cumulative surface runoff over a sub domain.

    @param dir directory of files
    @param domain name of the domain

    """

    # open netcdf files
    files = glob.glob(dir+'/ds_clim_dailysumrunoff_d03*.nc')
    n = len(files)
    days = np.zeros(n, dtype=np.int32)
    months = np.zeros(n, dtype=np.int32)
    years = np.zeros(n, dtype=np.int32)
    sfcrunoffs = np.zeros(n, dtype=np.float64)
    ifile = 0
    
    # mask sea
    wrf_grid='/nesi/nobackup/uc03160/AMPS_data/AMPS_surface/all_files/sfc_wrfout_d03_2018021800_f023.nc'
    ds_wrf = xr.open_dataset(wrf_grid)
    mask = ds_wrf.HGT.values.reshape((1035, 675))
    mask = xr.where(mask>0.0, 1.0, 0.0)

    
    
    for filename in files:
        
        m = re.search(r'(\d\d\d\d)(\d\d)(\d\d)\.nc$', filename)
        year = m.group(1)
        month = m.group(2)
        daystr = m.group(3)

        ds = xr.open_dataset(filename) 
        data = ds['sum_SFROFFd03' + year + month + daystr].values

        # get the slice of the data for that domain
        dom = domains[domain]

        # masking of coastline
        roff = np.sum(data[dom[1], dom[0]]*mask[dom[1], dom[0]]) # sum over domain

        days[ifile]=int(daystr) # store result
        months[ifile] = int(month)
        years[ifile] = int(year)
        sfcrunoffs[ifile] = roff
        
        ifile += 1
 
    # save df
    df = pd.DataFrame({'days': days, 'months': months, 'years': years, 'sfcrunoffs': sfcrunoffs})
    df.to_csv(domain + '.csv')

    return avg,std, d_max, d_min

def calc_monthly(vars=['T2', 'SWDOWN'], domains=['MDV', 'RSR']):
    # open files and calculate the mean and std daily for a given variables and regions





def clim_time():
    #plot timeseries of mean daily var for 7 years

def clim_table():
    # pandas df with all avg info 

    # 

def main(post_dir, regrid_dir, 
    clim_vars, ['T2', 'Q2', 'U10', 'V10', 'SWDOWN', 'GLW', 'PSFC', 'RAINNC', 'SFROFF', 'UDROFF'],
    domains = {
    'RSR': (slice(0, 239+1), slice(871, 987)), # slice(imin, imax+1), slice(jmin, jmax+1)
    'MDV': (slice(100, 250+1), slice(553, 790)),
    'Soil': (slice(0, 250+1), slice(553, 987)),  #double check these also soil needs LU_index mask
    }):

    files =glob.glob(post_dir)
    files.extend(glob.glob(regrid_dir))

    ftime_shift = {} # keys are datetime and item is the file with forecast hour corresponding
    for file in files:  
        date_new = time_shift(file)
        ftime_shift[date_new] = file

    fday_shift = {} #keys: yyyymmdd #items: files with time shifted to fhour
    for key in ftime_shift.keys():
        fday_shift[key[:-2]]=fday_shift.get(key[:-2], [])
        fday_shift[key[:-2]].append(ftime_shift[key])

    #loop through each day and open df

    for day in fday_shift.keys():

        mf_ds = xr.open_Dataset() #empty df to save daily avg info


        df = create_df(fday_shift[day])

        daily_df = calc_daily(df, vars=clim_vars) #calculate avg, max, min per pixel
        #update mf_ds
        #save mf_ds

        #calculate spatial avg, std, max, min over the domains
        daily_stats_rsr = calc_dailyspatial(domain='RSR')
        daily_stats_mdv = calc_dailyspatial(domain='MDV')
        daily_stats_soil = calc_dailyspatial(domain='Soil')

        #update pd df with data


        #save df
















