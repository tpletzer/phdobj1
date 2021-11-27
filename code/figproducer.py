import defopt
import xarray as xr
import re
import glob
import math
import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file


def spatialsumrunoff(*, dir: str, domain: str='NVL', month:int=None, year:int=None):
	"""
	Computes daily cumulative surface runoff over a sub domain.

	@param dir directory of files
	@param domain name of the domain
	@param month month (str), if None then every month
	@param year year (str), if None then every year

	"""