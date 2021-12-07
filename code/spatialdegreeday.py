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

def spatialdegreeday(*, dir: str='/nesi/nobackup/uoo03104/dailyavg_summerd03/', domain: str='NVL'):
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
	degreedays_sum = np.zeros(n, dtype=np.float64)
	degreedays_count = np.zeros(n, dtype=np.float64)
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
		data = ds['avg_T2d03' + year + month + day].values #take the average daily temp

		mask_deg = data.reshape((1035, 675)) #mask values less than or equal to 273.15K
		mask_deg = xr.where(mask_deg>273.15, 1.0, 0.0) 

		mask = (mask_land*mask_deg)

		# get the slice of the data for that domain
		dom = domains[domain]

		# masking of coastline
		degday_sum = np.sum(data[dom[1], dom[0]]*mask[dom[1], dom[0]]) # sum over domain return scalar

		degday_count = np.sum(mask_deg[dom[1], dom[0]]*mask_land[dom[1], dom[0]]) #returns # of pixels >0C


		days[ifile]=int(day) # store result
		months[ifile] = int(month)
		years[ifile] = int(year)
		degreedays_sum[ifile] = degday_sum
		degreedays_count[ifile] = degday_count
		
		ifile += 1
 
	# save df
	df = pd.DataFrame({'days': days, 'months': months, 'years': years, 'degreedays_sum': degreedays_sum, 'degreedays_count': degreedays_count})
	df.to_csv(domain + 'degday.csv')

if __name__=='__main__':
	defopt.run(spatialdegreeday)