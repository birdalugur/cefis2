#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import glob
import datetime
import os


# In[ ]:


def get_path(dir_path):
    """
    @type dir_path: str
    @param dir_path: okunacak klasöre ait path
    @rtype: list
    @returns: Belirtilen klasördeki excel dosyalarına ait yolun bir listesini döndürür.
    """

    files = [f for f in glob.glob(dir_path + "**/*.xlsx", recursive=True)]
    return files


# In[ ]:


def get_date(file_path):
    """Tarih bilgisini dosya adından ayrıştırır ve döndürür
    Parameters:
        file_path (str) : .xlsx dosyasına ait path
    Returns:
        Timestamp: dataya ait tarih bilgisi
    """
    date_list = file_path.split('\\')[-1].split('.')[0].split('_')[0:3]
    date = str()
    for y in date_list:
        if date_list.index(y) != 2:
            date = date + str(y) + '.'
        else:
            date = date + str(y)
    return pd.Timestamp(date)


# In[ ]:


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
    """Ardışık veriler arasındaki değişim miktarını hesaplar.
    Parameters:
        data (pandas.Series): Hesaplanacak veri
    Returns:
        pandas.Series: Değişim miktarının sıralı bir listesi
    """
    size = len(data)
    change_list = size*[None]
    count=0
    while(count<=size):
        try:
            change = ((-1)*(data[count]))+data[count+1]
            change_list[count+1]=change
            count+=1
        except:
            break
    series = pd.Series(data=change_list,index=data.index,name='change')    
    return series


# In[4]:


def find_duration(data):
    """Değişimin süresini hesaplar
    Parameters:
        data (pandas.Series): (+),(-) yönde ya da sabit bir dalganın süresini hesaplar
    Returns:
        pd.Series: Her bir yönde gerçekleşen değişimin süresi
    """
    size = len(data)
    dur_list = size*[None]
    sign_negativ =0
    sign_positive=0
    sign_zero=0
    for i in range(1,size+1):
        try:
            change = data.iat[i]
            if change is None:
                change = 0
        except:
            if sign_positive>0:
                dur_list[i-1] = sign_positive
            else:
                if sign_negativ>0:
                    dur_list[i-1] = sign_negativ
                elif sign_zero>0:
                    dur_list[i-1] = sign_zero
        if change<0:
            if (sign_positive==0 and sign_negativ==0 and sign_zero==0) or (sign_positive==0 and sign_negativ>0):
                sign_negativ+=1
            if sign_positive>0:
                dur_list[i-1]=sign_positive
                sign_positive=0
                sign_negativ+=1
            if sign_zero>0:
                dur_list[i-1]=sign_zero
                sign_zero=0
                sign_negativ+=1
        if change>0:
            if (sign_negativ==0 and sign_positive==0 and sign_zero==0) or (sign_negativ==0 and sign_positive>0):
                sign_positive+=1
            if sign_negativ>0:
                dur_list[i-1]=sign_negativ
                sign_negativ=0
                sign_positive+=1
            if sign_zero>0:
                dur_list[i-1]=sign_zero
                sign_zero=0
                sign_positive+=1
        if change == 0:
            if sign_negativ>0:
                dur_list[i-1]=sign_negativ
                sign_negativ=0
                sign_zero+=1
            elif sign_positive>0:
                dur_list[i-1]=sign_positive
                sign_positive=0
                sign_zero+=1
            else:
                sign_zero+=1
    series = pd.Series(data=dur_list,name='duration',index=data.index)
    return series
        


# In[ ]:


def find_amplitude(change_data, duration_data):
    """
    Parameters:
        change_data (pd.Series): Spread değeri kullanılarak hesaplanmış change serisi
        duration_data (pd.Series): Change verisi kullanılarak hesaplanmış duration serisi
    Returns:
        pd.Series:
    """
    size = len(duration_data)
    amplitude_list = size*[None]
    amplitude = 0
    count = 1
    index = 0
    i = 0
    while(i<size):
        if not (pd.np.isnan(duration_data.iat[i])):
            index = duration_data.iat[i] + count
            for value in change_data[int(count):int(index)]:                
                try:
                    amplitude+=value
                except:
                    amplitude+=0
            amplitude_list[i]=amplitude
            amplitude=0
            count=index
        i+=1
    series = pd.Series(data=amplitude_list,name='amplitude',index=duration_data.index)
    return series


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


def find_arithmeticMean(name, *args):
    """verilerin aritmetik ortalamasını hesaplar ve döndürür.
    Parameters:
        name(str): Hesaplama sonrası üretilecek seriye verilecek isim. örn: 'p_6A'
        args(tuple): Her bir elemanı, ortalaması hesaplanacak seriler
    Returns:
        pd.Series: örn. 6A'ya ait mid_price
    """
    
    number=len(args)
    return pd.Series(data=sum(args)/number,name=name,index=args[0].index) 


# In[1]:


def find_spread(mid_price,a_PNLTICK,a_TICKSIZE, b_PNLTICK,b_TICKSIZE):
    """6A ve 6B verisinden SPREAD verisini üretir.
    Parameters:
        mid_price(tuple):
        a_series(pd.Series): 6A sütunundaki veriler
        b_series(pd.Series): 6B sütunundaki veriler
        a_PNLTICK(float): 6A'ya ait PNLTICK değeri
        a_TICKSIZE(float): 6A'ya ait TICKSIZE değeri
        b_PNLTICK(float): 6B'ye ait PNLTICK değeri
        b_TICKSIZE(float): BA'ya ait TICKSIZE değeri
    Returns:
        pd.Series: Hesaplanmış spread verisi
    """
    a_series=mid_price[0]
    b_series=mid_price[1]
    atick = a_PNLTICK/a_TICKSIZE
    btick = b_PNLTICK/b_TICKSIZE
    size = len(a_series)
    spread = size*[0]
    for i in range(size):        
        try:
            spread[i+1] = (((a_series[i+1] - a_series[i])*atick) - ((b_series[i+1] - b_series[i])*btick)) +spread[i]    
        except:
            pass
    return pd.Series(data=spread,index=a_series.index,name='spread')


# In[ ]:


def element_counts(series,first=None,last=None):
    """hangi değerden kaç adet olduğunu döndürür.
    Parameters:
        series(pd.Series): incelenecek seri
        first(int):bakılacak aralığın başlangıç değeri
        last(int):bakılacak aralığın bitiş değeri
    """
    if (first==None) and (last==None):
        return pd.DataFrame(series.value_counts())
    else:
        return series[first:last].value_counts()


# In[ ]:


def write_excel(path,df,file_name,prod_name):
    directory_path = path+'\\'+prod_name + '\\'
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        if not os.path.exists(directory_path+'detail\\'):
            os.mkdir(directory_path+'detail\\')
    writer = pd.ExcelWriter(directory_path+ file_name+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


# In[2]:


def combin_date_and_time(time_series,date):
    """Bu fonksiyon, pd.Series.apply() metodundan çağrılmalı.
    Parameters
        time_series (pd.Series):
        date (datetime.date):
    Returns
        datetime.datetime
    """
    return datetime.datetime.combine(date,time_series)


# In[1]:


def split_df(df,hour=1):
    """Verileri 1er saatlik dilimlere böler(23 ayrı df).
    Parameters:
        df (dataframe):
        hour (int): varsayılan olarak 1. Gelecekte, asal olmayan saatlik veri için değiştirilebilir.
    Returns:
        list: Saatlik olarak bölünmüş df'lerin bir listesi."""
    start=0
#     stop=hour
    stop = 3600
    loop=int(23/hour)
    df_list=[pd.DataFrame()]*loop
    count=0    
    while count<loop:
#         df_list[count]= df_list[count].append(df[datetime.time(start):datetime.time(stop)])
        df_list[count]= df_list[count].append(df[start:stop])
        start=stop
        stop+=3600
        count+=1
    #df_list[count]= df_list[count].append(df[start:82801])
    return df_list  

