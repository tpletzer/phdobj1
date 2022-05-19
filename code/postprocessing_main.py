import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import pytz
from pandas.plotting import register_matplotlib_converters
import glob
from datetime import datetime
import defopt


'''
WORKFLOW

1. open all output files (CHANOBS, LDASOUT, wrf input, etc.) - this can be in parallel

2. open csv with validation data 

3. plot hourly timeseries for observation locations

4. plot scatterplots for observations (equal x and y, diag line)

5. Run validation metrics: RMSE, NSE, NSElog, bias, metric for timing/activation?

6. avg activation metrics across all obs 

7. latex doc with all figures and table of metrics

* for some, timeseries of spatial data eg. streamflow

'''


def main_chanobs(*, file_dir: str='/nesi/nobackup/output_files/', 
                ob_dir: str='/nesi/nobackup/uoo03104/validation_data/streamgagedata/', 
                ob_csv: str='stream_conc.csv'):  #need csv where each station is a col and rows are time and hourly
    """
    Postprocessing workflow of channel observations

    @param file_dir directory of model output netcdfs
    @param  ob_dir directory of observation csv
    @param ob_csv name of csv file for observations


    """

    chanobs_baseline = xr.open_mfdataset('*CHANOBS*', combine='by_coords') #open model output netcdfs

    #extract time from the first and last file in sim (in UTC)
    files = glob.glob(file_dir + '*CHANOBS*')
    files = sorted(files) 
    t0_str = files[0].split('/')[-1].split('.')[0] #extract first time stamp of simulation
    t0_utc = pd.Timestamp(t0_str,tz='UTC') # convert to time
    t0_mcm = t0_utc.tz_convert('Antarctica/Mcmurdo') #convert to mcm timezone
    t0 = str(t0_mcm)[0:-6] #id for observation csv

    tf_str = files[-1].split('/')[-1].split('.')[0] #extract last time stamp of simulation
    tf_utc = pd.Timestamp(tf_str,tz='UTC') # convert to time
    tf_mcm = tf_utc.tz_convert('Antarctica/Mcmurdo') #convert to mcm timezone
    tf = str(tf_mcm)[0:-6] #id for observation csv '2018-12-13 14:00:00'

    #open observational data
    obs = pd.read_csv(ob_dir + ob_csv, dtype=str)
    obs['DATE_TIME'] = pd.to_datetime(obs['DATE_TIME']) #convert DATE_TIME to date time obj

    obs = obs.loc[obs.DATE_TIME >= t0, :] # extract same times as the simulation
    obs = obs.loc[obs.DATE_TIME <= tf, :] 
    obs = obs.set_index('DATE_TIME') #use DATE_TIME as index
    obs.index = obs.index.tz_localize('Antarctica/Mcmurdo').tz_convert('UTC') #convert to UTC to match model output
    # obs['DISCHARGE RATE']=pd.to_numeric(obs['DISCHARGE RATE']) 

    # def to_m3(x):
    #     return x/1000

    # obs['DISCHARGE RATE']=obs['DISCHARGE RATE'].apply(to_m3)



if __name__ == "__main__":
    defopt.run(main_chanobs)

def main_ldasout(file_dir):

def main_wrfin(file_dir):

def main_chrtoutgrid(file_dir):


