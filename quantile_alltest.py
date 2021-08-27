import numpy as np
import xarray as xr
import glob
import defopt
import time


def pretime(ds):
    if 'XTIME' in ds:   
        return ds.reset_coords('XTIME', drop=True) 
    ds = ds.expand_dims('Time')
    ds = ds.drop_vars(['LU_INDEX', 'HGT', 'LANDMASK'])
    return ds

## when no chunks for time the dask.array= should be total time

def quantile_all(*, start_index: int=0, end_index: int=1, qfrac: float=0.95, v: str='T2'):

    """
    Calculates the quantiles of all AMPS d03 files from 201311 to 202003
    @param j represents each of the south_north values in range(0, 1034)
    """
    t0 = time.time()
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
    t1 = time.time()
    sevyr = xr.open_mfdataset(totalfiles[:100], parallel = False, preprocess = pretime, concat_dim = 'Time', combine = 'nested')
    t2 = time.time()
    savedir = '/nesi/nobackup/uoo03104/quantile_j/'

    q = np.zeros((1035, 675), np.float32)
    # iterate pixel by pixel
    for j in range(start_index, end_index):
        print(j)
        data = sevyr[v][:, j, :]
        sevyr.close() 
        q[j, :] = np.quantile(data, q=qfrac, axis=0)
    t3 = time.time()
    np.save(f'{savedir}{v}_{j:04d}.npy', q)
    t4 = time.time() 
    print(f' timings glob = {t1-t0:.3f} xarray open_mf = {t2-t1:.3f} q = {t3-t2:.3f} save = {t4-t3:.3f} total = {t4-t0:.3f}')

if __name__ == "__main__":
    defopt.run(quantile_all)
