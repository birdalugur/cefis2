# In[3]:
import pandas as pd
import glob
import datetime
import os
import numpy as np

#%%
def split_df(df,hour):
    """Verileri 1er saatlik dilimlere böler(23 ayrı df).
    Parameters:
        df (dataframe):
        hour (int): varsayılan olarak 1. Gelecekte, asal olmayan saatlik veri için değiştirilebilir.
    Returns:
        list: Saatlik olarak bölünmüş df'lerin bir listesi."""
    return np.array_split(df.drop(df.index[len(df)-1]),hour)

#%%
def get_mid_price(frame):
    return find_arithmeticMean(frame.bid_price, frame.ask_price)


#%%
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


# In[ ]:


def find_change(data):
    """Ardışık veriler arasındaki değişim miktarını hesaplar
       baştaki ve sondaki sıfırları ve Nan'ları kaldırır.
    Parameters:
        data (pandas.Series): Hesaplanacak veri
    Returns:
        pandas.Series: Değişim miktarının sıralı bir listesi
    """    
    df = pd.np.trim_zeros(data.diff().dropna())
    df.name="change"
    return df


# In[ ]:


def combine_df(frames,dates):
    """Farklı günlere ait veriler dataframe olarak birleştirir. Hiyerarşik index sağlar.
    Parameters:
        frames (list): Dataframe olarak tutulan verilerin listesi
        dates : Her bir df'e ait tarihlerin tutulduğu liste
    Returns:
        Dataframe: Birleştirilmiş veriler
    """
    
    return pd.concat(frames, keys=dates,axis=1,sort=False)


# In[1]:


def find_arithmeticMean(*args):
    """verilerin aritmetik ortalamasını hesaplar ve döndürür.
    Parameters:
        name(str): Hesaplama sonrası üretilecek seriye verilecek isim. örn: 'p_6A'
        args(tuple): Her bir elemanı, ortalaması hesaplanacak seriler
    Returns:
        pd.Series: örn. 6A'ya ait mid_price
    """
    
    number=len(args)
    seri = pd.Series(data=sum(args)/number) 
    seri=seri.reset_index(drop=True)
    return seri

# In[1]:


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



# In[ ]:
def find_duramp(data):
    """ (+),(-) yönde ya da sabit bir dalganın süresini hesaplar
    Parameters:
        data (pandas.Series): change
    Returns:
        pd.Series: Her bir yönde gerçekleşen değişimin süresi
    """
    data = data.dropna()
    size = len(data)
    dur_list = size*[None]
    amp_list = size*[None]
    sign_negativ =0
    sign_positive=0
    amplitude = 0
    #sign_zero=0
    for i in range(0,size+1):
        try:
            change = data.iat[i]            
        except:
            if sign_positive>0:
                dur_list[i-1] = sign_positive
                amp_list[i-1] = amplitude
            else:
                if sign_negativ>0:
                    dur_list[i-1] = sign_negativ
                else:
                    continue
                
        if change<0:
            if (sign_positive==0 and sign_negativ==0 ) or (sign_positive==0 and sign_negativ>0):
                sign_negativ+=1
                amplitude +=change
            if sign_positive>0:
                amp_list[i-1]=amplitude
                dur_list[i-1]=sign_positive
                sign_positive=0
                sign_negativ+=1
                amplitude=change

        elif change>0:
            if (sign_negativ==0 and sign_positive==0 ) or (sign_negativ==0 and sign_positive>0):
                amplitude+=change
                sign_positive+=1
            if sign_negativ>0:
                amp_list[i-1]=amplitude
                dur_list[i-1]=sign_negativ
                sign_negativ=0
                sign_positive+=1
                amplitude=change
        else:
            if sign_negativ>0:
                sign_negativ+=1
            elif sign_positive>0:
                sign_positive+=1
            else:
                continue
            
    series_dur = pd.Series(data=dur_list,name='duration',index=data.index).dropna()
    series_amp = pd.Series(data=amp_list,name='amplitude',index=data.index).dropna()
    return pd.DataFrame(data=[series_dur,series_amp]).transpose()
        