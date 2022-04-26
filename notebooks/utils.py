import descarteslabs as dl
import numpy as np
from datetime import datetime, timedelta
from scipy.interpolate import interp1d

def get_ndvi_tseries(
    geom, 
    start_date="2019-04-01", 
    end_date="2019-10-01"
):
    scenes, ctx = dl.scenes.search(
        geom,
        products="esa:sentinel-2:l2a:v1",
        start_datetime=start_date,
        end_datetime=end_date,
        limit=None
    )
    print(f"Found {len(scenes)} scenes for specified geometry")
    
    print(f"Pulling raster data from DL Catalog")
    stack = scenes.stack(
        ["red", "nir", "cloud_mask"],
        ctx,
        flatten=lambda x: x.properties.date.strftime("%Y-%m-%d"),
        scaling="physical",
        progress=False,
    )
    
    print(f"Masking out clouds")
    cmask = np.repeat(
        (stack[:,-1].data==1)[:, np.newaxis],
        stack.shape[1],
        axis=1
    )
    
    stack.mask = (stack.mask) | cmask
    
    print(f"Computing NDVI")
    ndvi = (stack[:,1] - stack[:,0])/(stack[:,1] + stack[:,0])

    ndvi_ts = np.ma.median(ndvi, axis=[1,2])
    dates = list(scenes.groupby("properties.date.day"))
    
    dates = [
        key for key, scene in scenes.groupby(
            lambda x: x.properties.date.strftime("%Y-%m-%d")
        )
    ]
    
    dates_ts = [
        datetime.strptime(date, "%Y-%m-%d").timestamp() for date in dates
    ]
    
    new_dates = np.arange(
        datetime.strptime(start_date, "%Y-%m-%d"),
        datetime.strptime(end_date, "%Y-%m-%d"),
        timedelta(days=6)
    ).astype(datetime)
    
    new_dates_ts = [t.timestamp() for t in new_dates]
    
    tseries_masked = ndvi_ts.data[~ndvi_ts.mask]
    dates_masked = np.array(dates_ts)[~ndvi_ts.mask]
    
    print(f"Interpolating time series from dates: {dates} to new dates: {new_dates.tolist()}")
    
    f_interp = interp1d(
        dates_masked,
        tseries_masked,
        bounds_error=False,
        copy=False,
        fill_value="extrapolate",
    )
    
    return f_interp(new_dates_ts)[1:], new_dates[1:]

def get_cdl(
    geom,
    year=2019
):
    scenes, ctx = dl.scenes.search(
        geom,
        products="usda:cdl:v1",
        start_datetime=f"{year}-12-30",
        end_datetime=f"{year+1}-01-01",
        limit=None
    )
    
    cdl = scenes.mosaic(
        ["class"],
        ctx
    )
    
    return mode(cdl.data[~cdl.mask].flat, axis=None).mode[0]