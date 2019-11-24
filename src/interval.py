from operator import attrgetter
import pandas as pd
from operator import attrgetter

def __define_Timerange(duration,value,method):
    if method == 'width':
        return pd.timedelta_range(start=duration.min(),end=duration.max(),freq=pd.Timedelta(pd.offsets.Second(value)))
    elif method == 'size':
        return pd.timedelta_range(start=duration.min(),end=duration.max(),periods=value)
    else:
        raise ValueError('method argümanı width ya da size olmalı')

def __define_range(data,value,method):
    if method == 'width':
        return pd.interval_range(start=data.min(),freq=value,end=data.max())
    elif method == 'size':
        return np.linspace(data.min(), data.max(), value)
    else:
        raise ValueError('method argümanı width ya da size olmalı')

def set_range(data,value,method):
    """method = 'width' -> her bir aralığın genişliği @value kadardır.
       method = 'size'  -> her bir aralık eşit büyüklükte @value adettir.
    """
    interval = __define_range(data=data,value=value,method=method)
    return pd.cut(data,interval)

def set_timeRange(data,value,method):
    """method = 'width' -> her bir aralığın genişliği @value kadardır.
       method = 'size'  -> her bir aralık eşit büyüklükte @value adettir.
    """
    interval = __define_Timerange(duration=data,value=value,method=method)
    return pd.cut(data,interval)

def get_right(x):
    """Aralığın sağ değerini döndürür
    """
    return x.map(attrgetter('right'))