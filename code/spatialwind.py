import defopt
import pandas as pd
import xarray as xr
import re
import glob
import numpy as np

domains = {
	'NVL': (slice(0, 239+1), slice(871, 987)), # slice(imin, imax+1), slice(jmin, jmax+1)
	'MDV': (slice(100, 250+1), slice(553, 790)),
	'both': (slice(0, 250+1), slice(553, 987)),
}

def spatialwind(*, dir: str='/nesi/nobackup/uoo03104/dailyavg_summerd03/', domain: str='NVL'):
	"""
	Computes daily cumulative surface runoff over a sub domain.

	@param dir directory of files
	@param domain name of the domain

	"""

	# open netcdf files
	files = glob.glob(dir + '*.nc')
	n = len(files)
	days = np.zeros(n, dtype=np.int32)
	months = np.zeros(n, dtype=np.int32)
	years = np.zeros(n, dtype=np.int32)
	u_avg = np.zeros(n, dtype=np.float64)
	v_avg = np.zeros(n, dtype=np.float64)
	ifile = 0
	
	# mask sea
	wrf_grid='/nesi/nobackup/uc03160/AMPS_data/AMPS_surface/all_files/sfc_wrfout_d03_2018021800_f023.nc'
	ds_wrf = xr.open_dataset(wrf_grid)

	mask_land = ds_wrf.HGT.values.reshape((1035, 675)) #mask
	mask_land = xr.where(mask_land>0, 1.0, 0.0)  # redo hotencoding for height
	
	for filename in files:
		
		m = re.search(r'(\d\d\d\d)(\d\d)(\d\d)\.nc$', filename)  #return date info
		year = m.group(1)
		month = m.group(2)
		day = m.group(3)

		ds = xr.open_dataset(filename) 
		data_u = ds['avg_U10d03' + year + month + day].values #take the average daily temp 
		data_v = ds['avg_V10d03' + year + month + day].values

		# get the slice of the data for that domain
		dom = domains[domain]

		# masking of coastline
		u10_mean = np.mean(data_u[dom[1], dom[0]]*mask_land[dom[1], dom[0]]) # sum over domain return scalar

		v10_mean = np.mean(data_v[dom[1], dom[0]]*mask_land[dom[1], dom[0]]) #returns # of pixels >0C


		days[ifile]=int(day) # store result
		months[ifile] = int(month)
		years[ifile] = int(year)
		u_avg[ifile] = u10_mean
		v_avg[ifile] = v10_mean
		
		ifile += 1
 
	# save df
	df = pd.DataFrame({'days': days, 'months': months, 'years': years, 'u_avg': u_avg, 'v_avg': v_avg})
	df.to_csv(domain + 'wind.csv')

if __name__=='__main__':
	defopt.run(spatialwind)