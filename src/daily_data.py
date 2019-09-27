#!/usr/bin/env python
# coding: utf-8


# In[ ]:


import pandas as pd
import src.auxiliary_functions as aux
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


# In[ ]:


@dataclass
class DailyData:
    mid_price_list: list
    date: datetime.date
    name: str
    time: List[pd.Series] = field(default_factory=list)
    spread: List[pd.Series] = field(default_factory=list)
    change: List[pd.Series] = field(default_factory=list)
    duramp: List[pd.DataFrame] = field(default_factory=list)
    # duration: List[pd.Series] = field(default_factory=list)
    # amplitude: List[pd.Series] = field(default_factory=list)
    df: pd.DataFrame = field(default=pd.DataFrame)
        
    def spread_hesapla(self):
        for i in range(23):
            self.time.append(self.mid_price_list[i]['time'])
            self.spread.append(aux.find_spread((self.mid_price_list[i].iloc[:,1],self.mid_price_list[i].iloc[:,2]),a_PNLTICK=10,a_TICKSIZE=0.0001,b_PNLTICK=6.25,b_TICKSIZE=0.0001))
            self.change.append(aux.find_change(self.spread[i]))
            self.duramp.append(aux.find_duramp(self.change[i]))
        #    self.amplitude.append(aux.find_amplitude(self.change[i],self.duration[i]))
        
        
    def get_df(self,hour_slice):
        return pd.DataFrame(data=[self.spread[hour_slice],self.change[hour_slice],self.duramp[hour_slice].duration,self.duramp[hour_slice].amplitude]).transpose()


    


# In[ ]:


def to_match_days(infoList):
    """Aynı güne ait olan verileri tuple çiftleri olarak bulur ve listeye atar
    Parameters:
        infoList(list): Info örneklerinin bir listesi
    Returns:
        list: tuple çitlerinin bir listesi
    """
    same=[]
    size = len(infoList)
    for i in range(size-1):
        for k in range(i+1,size):
            if (infoList[i].date==infoList[k].date) and (infoList[i].product!=infoList[k].product):
                same.append((infoList[i],infoList[k]))
    return same


# In[ ]:


def to_match_hour(info1,info2):
    """make hourly matching belonging to different products
    Parameters:
        info1, info2 (Info) :
    Returns:
        list: mid_price içeren saatlik df listesi (23 df [time,mid_price,mid_price])
    """
    saatlik =[]
    for i in range(23):
        d = {'time': info1.hourly_data[i].time,
             info1.date.strftime('%m/%d/%Y_')+info1.product : info1.hourly_data[i].mid_price,
             info2.date.strftime('%m/%d/%Y_')+info2.product : info2.hourly_data[i].mid_price }        
        saatlik.append(pd.DataFrame(data=d).reset_index(drop=True))
    return saatlik



# In[ ]:
def get_all_data(full_data):
    """tüm duration df'lerini birleştirir. tüm amp. df'lerini birleştirir. sonra bu ikisini birleştirip döndürür.
    **part_** : **i**.saate ait spread,dur,amp.. verileri(*1.gün+2.gün+3.gün*..) birleştiriliyor <br>
    daha sonra *part_* ile başlayan listelerden **df** oluşturuluyor<br>
    oluşturulan **df**'ler **full_** prefix'e sahip listelere atılıyor.
    Parameters:
        full_data (list): DailyData orneklerinin bir listesi
    Returns:
        dataframe: 
    """
    full_duration = []
    full_amplitude = []
    hour_series = pd.date_range('2018-01-01-18', periods=23, freq='H')
    hour_series = hour_series.time
    
    for hour in range(23):
        part_duration = []
        part_amplitude = []
        
        for data in full_data:
            part_duration.extend(data.duramp[hour].duration)
            part_amplitude.extend(data.duramp[hour].amplitude)
        
        df_amp = pd.DataFrame(part_amplitude)
        df_amp = df_amp.reset_index(drop=True)        
        current_index = full_data[0].time[hour]
        full_amplitude.append(df_amp)
        
        df_dur = pd.DataFrame(part_duration).transpose()
        df_dur = df_dur.reset_index(drop=True)        
        current_index = full_data[0].time[hour]
        full_duration.append(df_dur.transpose())
    dur = pd.concat(objs=full_duration,keys=hour_series)
    amp = pd.concat(objs=full_amplitude,keys=hour_series)
    df = pd.concat([dur,amp],axis=1)
    df.columns=['duration','amplitude']
    df = df.dropna()
    return df


def divide(df):
    return {'pozitive':df[df['amplitude']>0].median(),'negative':df[df['amplitude']<0].median()}