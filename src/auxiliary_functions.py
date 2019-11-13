# In[3]:
import pandas as pd
import glob
import datetime
import os
import numpy as np


def split_df(df,hour):
    """Verileri 1er saatlik dilimlere böler(23 ayrı df).
    Parameters:
        df (dataframe):
        hour (int): varsayılan olarak 1. Gelecekte, asal olmayan saatlik veri için değiştirilebilir.
    Returns:
        list: Saatlik olarak bölünmüş df'lerin bir listesi."""
    return np.array_split(df.drop(df.index[len(df)-1]),hour)


def combine_date(time_series,date):
    """tarih ve saat bilgisini birleştirip series olarak döndürür.
    Parameters:
        time_series (pandas.Series):TIME sütunundan okunan datetime.time serisi
        date(Timestamp) : Seriye eklenecek tarih
    Returns:
        pandas.Series: birleştirilmiş Timestamp serisi    
    """
    date_list = list()
    list_time = list(time_series)
    for time in list_time:
        date_list.append(pd.Timestamp.combine(date,time))
    return pd.Series(data=date_list)     




def combine_df(frames,dates):
    """Farklı günlere ait veriler dataframe olarak birleştirir. Hiyerarşik index sağlar.
    Parameters:
        frames (list): Dataframe olarak tutulan verilerin listesi
        dates : Her bir df'e ait tarihlerin tutulduğu liste
    Returns:
        Dataframe: Birleştirilmiş veriler
    """
    
    return pd.concat(frames, keys=dates,axis=1,sort=False)



def find_spread(a_series,b_series,values):
    """6A ve 6B verisinden SPREAD verisini üretir.
    Parameters:
        mid_price(tuple):
        values(dict): ticksize değerleri
    Returns:
        pd.Series: Hesaplanmış spread verisi
    """
    atick = values['a_PNLTICK']/values['a_TICKSIZE']
    btick = values['b_PNLTICK']/values['b_TICKSIZE']
    size = len(a_series)
    spread = size*[0]
    for i in range(size): 
        try:
            spread[i+1] = (((a_series.iat[i+1] - a_series.iat[i])*atick) - ((b_series.iat[i+1] - b_series.iat[i])*btick)) +spread[i] 
        except:            
            pass        
    return pd.Series(data=spread,index=a_series.index,name='spread')


def extract_product(df, product_name):
    """Belirli bir ürüne ait spread verisini ayıklar
    """
    idx = pd.IndexSlice
    df = df.set_index('time')
    return df.loc[:,idx[:,product_name]].droplevel(level=1,axis=1)    


def get_time(hour_indice,prod_name,duramp):
    """Time bilgisini amplitude verisinden alarak döndürür.
    Parameters
    ----------
    hour_indice (int): time_series indisi. Örnek : 18:00:00-19:00:00 için 0, 19:00:00-20:00:00 için 1
    prod_name (str): ürün adı
    Return
    ------
    pandas.DataFrame : n güne ait time series içerir
    """
    return duramp[hour_indice]['6AU8_6BU8'].reset_index().drop(['duration','amplitude'],axis=1).set_index('level_0')


