import defopt
import pandas as pd
import xarray as xr
import re
import glob


domains = {
	'NVL': (slice(0, 239+1), slice(871, 987)), # slice(imin, imax+1), slice(jmin, jmax+1)

}



def spatialsumrunoff(*, dir: str, domain: str='NVL', month:int=None, year:int=None):
	"""
	Computes daily cumulative surface runoff over a sub domain.

	@param dir directory of files
	@param domain name of the domain
	@param month month (str), if None then every month
	@param year year (str), if None then every year

	"""

	# mask sea
	wrf_grid='/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2018021800_f023.nc'
	ds_wrf = xr.open_dataset(wrf_grid)
	mask = ds_wrf.LANDMASK.values.reshape((1035, 675))

	# open netcdf files
	files = glob.glob(dir+'/ds_clim_dailysumrunoff_d03' + str(year) + str(month) + '*.nc')
	days = []
	months = []
	sfcrunoffs = []
	for file in files:
		daystr = re.match(r'(\d\d)\.nc$').group(1)
		ds = xr.open_dataset(file)
		data = ds['sum_SFROFFd03' + str(year) + str(month) + daystr].values

		# get the slice of the data for that domain
		dom = domains[domain]

		# masking of coastline
		#roff = data[dom[0], dom[1]].sum(data) # sum over domain
		roff = np.sum(data[dom[1], dom[0]]*mask[dom[1], dom[0]])

		days.append(int(daystr)) # store result
		months.append(month)
		years.append(year)
		sfcrunoffs.append(roff)
 
	# save df
	df = pd.DataFrame(days=days, months=months, years=years, sfcrunoffs=sfcrunoffs)
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
	dtmin = datetime(year=y, month=11, day=1)
	dtmax = dtmin + timedelta(days=160)
	summer = data[(data['date'] >= dtmin) & (data['date'] < dtmax)]
	#summer = data[data['date'].dt.month == 11]

	

	# plot each summer timeseries on a seperate subplot
	plt.plot(df, data.sfcrunoffs)
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
