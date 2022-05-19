import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import pytz
from pandas.plotting import register_matplotlib_converters
import glob

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


def main_chanobs(file_dir='/nesi/nobackup/output_files/', obs_csv):

    chanobs_baseline = xr.open_mfdataset('*CHANOBS*',
                            combine='by_coords')



def main_ldasout(file_dir):

def main_wrfin(file_dir):

def main_chrtoutgrid(file_dir):


