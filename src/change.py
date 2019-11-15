import pandas as pd
import numpy as np
import src.base as base

def get_change(data):
    """Ardışık veriler arasındaki değişim miktarını hesaplar
       baştaki ve sondaki sıfırları ve Nan'ları kaldırır.
    Parameters:
        data (pandas.DataFrame): Hesaplanacak veri
    Returns:
        df_change: Değişim miktarı
    """
    data=data.set_index(data.date)
    data=data.drop('date',axis=1)
    change = data.diff().dropna()
    change=change.apply(np.trim_zeros)
    return change


def sign(pair):
    """Change'i işaretlemek için kullanılır.
    Parameters
    ----------
    pair (pd.Series): change of pair
    Returns
    -------
    signed_data (pd.DataFrame)
    """
    sign=base.mark_data(pair)
    return pd.concat([pair,sign],axis=1)

def last_time(x):
    """DatetimeIndex'deki son zamanı döndürür
    """
    x=x.reset_index()
    return x.iloc[-1].date

def get_amplitude(change_of_pair):
    """Bir change serisi alır. Amplitude ve duration'ı hesaplayarak döndürür.
    Example
    -------
    >>> x=get_amplitude(change_of_6AU8_6BU8)    
    >>> x.dtypes
    Out[]:
        6AU8_6BU8            float64   #amplitude
        duration     timedelta64[ns]
        date          datetime64[ns]
        dtype: object
    """
    name=change_of_pair.name
    temizle=base.clean_data(change_of_pair)
    isaretle=sign(temizle)
    r=isaretle.reset_index()
    r['duration']=r.date.diff()
    return r.groupby('sign').agg({name:'sum','duration':'sum','date':last_time})