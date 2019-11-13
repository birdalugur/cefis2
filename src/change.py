import pandas as pd
import numpy as np
from src.base import (mark_data)

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
    sign=mark_data(pair)
    return pd.concat([pair,sign],axis=1)

def last_time(x):
    """DatetimeIndex'deki son zamanı döndürür
    """
    x=x.reset_index()
    return x.iloc[-1].date