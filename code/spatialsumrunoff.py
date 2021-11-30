import defopt
import pandas as pd
import xarray as xr
import re
import glob
import numpy as np

domains = {
	'NVL': (slice(0, 239+1), slice(871, 987)), # slice(imin, imax+1), slice(jmin, jmax+1)

}



def spatialsumrunoff(*, dir: str='/nesi/nobackup/uoo03104/dailysumrunoff2_summerd03/', domain: str='NVL'):
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
	wrf_grid='/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2018021800_f023.nc'
	ds_wrf = xr.open_dataset(wrf_grid)
	#mask = ds_wrf.LANDMASK.values.reshape((1035, 675))
	mask = ds_wrf.HGT.values.reshape((1035, 675))
	mask = xr.where(mask>0, 1.0, 0.0)  # redo hotencoding for height
	
	for filename in files:
		
		m = re.search(r'(\d\d\d\d)(\d\d)(\d\d)\.nc$', filename)
		year = m.group(1)
		month = m.group(2)
		daystr = m.group(3)

		ds = xr.open_dataset(filename) 
		data = ds['sum_SFROFFd03' + year + month + daystr].values

		# get the slice of the data for that domain
		dom = domains[domain]

		# TO DO masking of coastline
		roff = np.sum(data[dom[1], dom[0]]*mask[dom[1], dom[0]]) # sum over domain

		days[ifile]=int(daystr) # store result
		months[ifile] = int(month)
		years[ifile] = int(year)
		sfcrunoffs[ifile] = roff
		
		ifile += 1
 
	# save df
	df = pd.DataFrame({'days': days, 'months': months, 'years': years, 'sfcrunoffs': sfcrunoffs})
	df.to_csv(domain + '.csv')

if __name__=='__main__':
	defopt.run(spatialsumrunoff)

#-------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def plotsumrunoff(csvfile='NVL.csv'):

	"""
	Plots timeseries subplot for summers of the spatial sum of sfc runoff

	@param csvfile directory of csv file 

	"""

	data = pd.read_csv(csvfile)

	# turn the year, month and day into datetime objects
	dt = pd.to_datetime({'year': data.years,
		                 'month': data.months,
		                 'day': data.days})
	data['date'] = dt

	# reorder data by datetime
	data.sort_values(by=['date'], inplace=True, ascending=True)

	# define summer as Nov-Mar
	#dtmin = datetime(year=2014, month=11, day=1)
	#dtmax = dtmin + timedelta(days=150)
	#summer = data[(data['date'] >= dtmin) & (data['date'] < dtmax)]
	#summer = data[data['date'].dt.month == 11]

	ncol=1
	nrow = 7
	fig, axes = plt.subplots(nrow, ncol, figsize=(15,10))

	for iplot in range(nrow):
		i = iplot // ncol
		dtmin = datetime(year=(i+2013), month=11, day=1)
		dtmax = dtmin + timedelta(days=150)
		summer = data[(data['date'] >= dtmin) & (data['date'] < dtmax)]
		axes[i].plot(summer.date, summer.sfcrunoffs)
		axes[i].set_ylim(bottom=0, top=1200000)

	
	plt.subplots_adjust(hspace=2.0)
	plt.show()

	

	# plot each summer timeseries on a seperate subplot
	plt.plot(summer.date, summer.sfcrunoffs)
	plt.show()




####----------- code to analyze NVL.csv script
import pandas as pd 

csvfile='NVL.csv'

data = pd.read_csv(csvfile)

dt = pd.to_datetime({'year': data.years,
		                 'month': data.months,
		                 'day': data.days})

data['date'] = dt

data.sort_values(by=['date'], inplace=True, ascending=True)

count=0
for i in data.itertuples():
	if i.sfcrunoffs < 0:
		print(i.date, i.sfcrunoffs)
		count+=1
print(count)  ## 103 files

#data.date.where(data.sfcrunoffs<0).count()
