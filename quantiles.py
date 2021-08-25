import matplotlib.pyplot as plt 
import xarray as xr
import glob

regridfiles = (glob.glob('/nesi/nobackup/uoo03104/clim_summerregridfinal/*.nc'))

postfiles = (glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_20171[1-2]??00_f01[3-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_20171[1-2]??00_f0[2-3][0-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_201[8-9]0[1-3]??00_f01[3-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_201[8-9]0[1-3]??00_f0[2-3][0-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_201[8-9]1[1-2]??00_f01[3-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_201[8-9]1[1-2]??00_f0[2-3][0-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_20200[1-3]??00_f01[3-9].nc'))
postfiles.extend(glob.glob('/nesi/nobackup/uoo03104/all_files/*d03_20200[1-3]??00_f0[2-3][0-9].nc'))

totalfiles = regridfiles + postfiles

def pretime(ds):
    if 'XTIME' in ds:   
        return ds.reset_coords('XTIME', drop=True) 
    ds = ds.expand_dims('Time') 
    return ds

## when no chunks for time the dask.array= should be total time
sevyr = xr.open_mfdataset(totalfiles, preprocess = pretime, concat_dim = 'Time', combine = 'nested', chunks={'Time':10, 'south_north':10, 'west_east':10})
sevyr.drop_vars('LU_INDEX')
sevyr_q = xr.Dataset()
dst_ds = xr.open_dataset('/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2018010100_f014.nc')
sevyr_q.coords["XLAT"] = (("south_north", "west_east"), dst_ds.XLAT.values)
sevyr_q.coords["XLONG"] = (("south_north", "west_east"), dst_ds.XLONG.values)
sevyr_q[v] = (("south_north", "west_east"), dst_ds.LU_INDEX.values)
for v in sevyr.var():
    da_v = sevyr[v]
    q = da_v.chunk({'Time':None}).quantile(0.95, dim="Time")
    sevyr_q[v] = (("south_north", "west_east"), q.values)
    #q.plot(x="west_east", y="south_north")
    #plt.show()
