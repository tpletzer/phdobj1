import defopt
import xarray as xr
import re
import glob
import math
import matplotlib.pyplot as plt
import cartopy
import salem
from salem import open_wrf_dataset, get_demo_file


def main(*, varname: str, wrfgridfile: str, inputfiles: str, outputfile: str):
	"""
	Plotting subplots

	@param varname (str) variable name
	@param wrfgridfile (str) wrf file with grid info
	@param inputfiles (str) input files
	@param outputfile (str) name of output file

	"""


if __name__=='__main__':
	defopt.run(main)