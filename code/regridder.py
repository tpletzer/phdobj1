#script to regrid sfc wrf files from AMPS from 2013 to 2017

import pickle
import os
import xarray as xr
import glob
import xesmf as xe
import defopt



def pkl_toregrid():

	


def regridder(*, start_index: int=0, end_index: int=-1): 
    """
    Regridding all files from 201311 to 201710
    @param start_index starting index of file list
    @param end_index ending index of file list
    """

    savedir = '/nesi/nobackup/uoo03104/clim_winterregrid/'

    f2 = open('/nesi/nobackup/uoo03104/climfiles_toregrid.pkl', 'rb')
    files = pickle.load(f2)
    #files = ['/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2013110100_f013.nc','/nesi/nobackup/uoo03104/all_files/sfc_wrfout_d03_2013110100_f033.nc' ]

    end_index=min(end_index, len(files))
    files = files[start_index:end_index]
    dst_ds = xr.open_dataset('/nesi/nobackup/uoo03104/clim_summerpost/ds_clim_d03201801.nc')

    dst = xr.Dataset({'lat': (['south_north', 'west_east'], dst_ds['XLAT'].values),
                      'lon': (['south_north', 'west_east'], dst_ds['XLONG'].values)})

    src_ds_0 = xr.open_dataset(files[0])
    src_ds_0 = src_ds_0.squeeze('Time')
    src_0 = xr.Dataset({'lat': (['south_north', 'west_east'], src_ds_0['XLAT'].values),
                        'lon': (['south_north', 'west_east'], src_ds_0['XLONG'].values)})
    regridder = xe.Regridder(src_0, dst, 'bilinear')

    for f in files:
        
        src_ds = xr.open_dataset(f)
        src_ds = src_ds.squeeze('Time')
        src = xr.Dataset({'lat': (['south_north', 'west_east'], src_ds['XLAT'].values),
                          'lon': (['south_north', 'west_east'], src_ds['XLONG'].values)})
        
        regrid_ds = xr.Dataset()
        for v in src_ds.var():
            regrid_ds[v] = (("south_north", "west_east"), regridder(src_ds[v]).values)
        
        regrid_ds.coords["XLAT"] = (("south_north", "west_east"), dst_ds.XLAT.values)
        regrid_ds.coords["XLONG"] = (("south_north", "west_east"), dst_ds.XLONG.values)
        regrid_ds.to_netcdf(savedir + 'regrid_' + str(f[-22:-3]) + '.nc')

        print('done with ' + str(f[-22:-3]))

if __name__ == "__main__":
    defopt.run(regridder)


    

