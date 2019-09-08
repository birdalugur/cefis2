#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from datetime import time
import src.daily_data as dt

# In[ ]:


def find_sign(value):
    """değişimin hangi yönde olduğunu kontrol eder
    Parameters:
        value (float) : amplitude değeri
    Returns:
        int: pozitif ise 1, negatif ise -1 aksi durumda 0 döndürür.
    """
    if value>0:
        return 1
    elif value<0:
        return -1
    else:
        return 0


# In[ ]:


def get_conditon(df_line, min_duration=None, min_amplitude=None):
    """Satırdaki verilerin, verilen koşulu sağlayıp sağlamadığını kontol eder.
    Parameters:
        df_line (Series) : dataframe'e ait bir satır
        min_duration (float) : geçerli sayılabilecek dur. değeri
        min_amplitude (float) : geçerli sayılabilecek amp. boyutu
    Returns:
        boolean: koşul sağlanıyorsa True, sağlanmıyorsa False
    """
    if min_amplitude == None:
        if df_line['duration'] <= min_duration:
            return True
        else:
            return False
    else:
        if df_line['duration'] <= min_duration and abs(df_line['amplitude']) <= abs(min_amplitude):
            return True
        else:
            return False


# In[3]:


def _conditionally_scan(df,medyan):
    """Bir dataframe'i verilen koşullara göre yeniden düzenler.
    Parameters:
        df (dataframe): pd.Dataframe nesnesi
        min_dur (int): 
        min_amp (float):
    Returns:
        pd.Dataframe:
    Example:
        min_duratin=1, min_amplitude=30 olarak verildiğini varsayalım. 3sn'lik ve -40 amp. sahip
        negatif bir dalgayı takip eden, 1sn'lik ve amplitude değeri 25 olan pozitif bir dalga var ise,
        bu dalgayı önceki dalgaya dahil eder yeni değer dur=4sn amp=-15 olur ve bir sonraki dalganın
        koşulu sağlayıp sağlamadığını kontrol eder. Sağlanıyorsa aynı işlem devam eder. Sağlanmıyorsa veriler kaydedilerek
        bir sonraki dalga için işlemler tekrar yapılır ve diğer dalga hesaplanır.
    """
    min_dur = None
    min_amp=None
    df=df[['duration','amplitude']].dropna()
    index = 0
    cout = 1
    time_list  = []
    dur_list =[]
    amp_list = []     
    dlist = []
    alist=[]
    first = True
    second = True
    while(cout<len(df)):
        current_dur = df.iloc[index,:]['duration']        
        current_amp = df.iloc[index,:]['amplitude']
        current_sign = find_sign(current_amp)

        if current_sign==1:
            min_dur = medyan['pozitive'].duration
            min_amp = medyan['pozitive'].amplitude
        else:
            min_dur = medyan['negative'].duration
            min_amp = medyan['negative'].amplitude

        second = True
        while(second and cout<len(df)+1):
            try:
                next_sign = find_sign(df.iloc[cout,:]['amplitude'])

                if (next_sign == current_sign) or next_sign == 0 :
                    dur_list.append(df.iloc[cout,:]['duration'])
                    amp_list.append(df.iloc[cout,:]['amplitude'])
                    cout+=1
                    
                else:
                    if get_conditon(df.iloc[cout,:],min_dur,min_amp):
                        
                        dur_list.append(df.iloc[cout,:]['duration'])
                        amp_list.append(df.iloc[cout,:]['amplitude'])
                        cout+=1
                        
                    else:      
                        print("count: ", cout," -index: ",index)
                        print("d",min_dur,"a",min_amp)
                        dur_list.append(df.iloc[index,:]['duration'])
                        amp_list.append(df.iloc[index,:]['amplitude'])
                        index = cout
                        time_list.append(df.index[cout-1])
                        cout=cout+1
                        dlist.append(sum(dur_list))
                        alist.append(sum(amp_list))
                        dur_list.clear()
                        amp_list.clear()
                        second = False
            except:
                dur_list.append(df.iloc[index,:]['duration'])
                amp_list.append(df.iloc[index,:]['amplitude'])
                dlist.append(sum(dur_list))
                alist.append(sum(amp_list))
                time_list.append(df.index[cout-1])
                second = False
        
    new_df = pd.DataFrame({'duration':dlist,'amplitude':alist},index=time_list)
    return new_df


# In[7]:


def scan(df):
    """Medyana göre dalgaları yeniden düzenler
    Parameters:
        df(pd.Dataframe): alt dataframe'ler içeren bir dataframe
    Returns:
        pd.Dataframe: pd.concat([df,df..])
    """
    df_list = []
    main_index = df.index.levels[0].tolist()    
    for index in main_index:
        current_df = df.loc[index]
        current_medyan = dt.divide(current_df)
        df_list.append(_conditionally_scan(df=current_df,medyan=current_medyan))
        
    combin_df = pd.concat(df_list,keys=main_index)
    return combin_df

