#!/usr/bin/env python
# coding: utf-8

# from importlib import reload
# reload(aux)

# In[3]:


import pandas as pd
import src.auxiliary_functions as aux
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


# In[5]:


@dataclass
class Info:
    path: str
    date: datetime.date
    product: str
    df: pd.DataFrame
    hourly_data: list


# In[19]:


@dataclass
class GunlukVeri:    
    #eslesmis_info: tuple
    saatik_data: list
    tarih: datetime.date
    name: str
    time: List[pd.Series] = field(default_factory=list)    
    spread: List[pd.Series] = field(default_factory=list)
    change: List[pd.Series] = field(default_factory=list)
    duration: List[pd.Series] = field(default_factory=list)
    amplitude: List[pd.Series] = field(default_factory=list)
    df: pd.DataFrame = field(default=pd.DataFrame)
        
    def spread_hesapla(self):
        for i in range(23):
            self.time.append(self.saatik_data[i]['time'])
            self.spread.append(aux.find_spread((self.saatik_data[i].iloc[:,1],self.saatik_data[i].iloc[:,2]),a_PNLTICK=10,a_TICKSIZE=0.0001,b_PNLTICK=6.25,b_TICKSIZE=0.0001))
            self.change.append(aux.find_change(self.spread[i]))
            self.duration.append(aux.find_duration(self.change[i]))
            self.amplitude.append(aux.find_amplitude(self.change[i],self.duration[i]))
        
        
    def get_df(self,hour_slice):
        return pd.DataFrame(data=[self.spread[hour_slice],self.change[hour_slice],self.duration[hour_slice],self.amplitude[hour_slice]])


# In[32]:


def get_info(path):
    __cols= ["Time","BID price","ASK price"]
    split_text = __parse_path(path)
    date=__findDate(split_text[0])
    product=split_text[1] + split_text[2]
    df = pd.read_excel(path,usecols=__cols)
    df.columns=['time','bid_price','ask_price']
    hourly_data = aux.split_df(df)
    hourly_data=__calc_mp(hourly_data)
    return Info(path,date,product,df=df,hourly_data=hourly_data)


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


# In[36]:


def to_match_hour(info1,info2):
    """make hourly matching belonging to different products
    """
    saatlik =[]
    for i in range(23):
        d = {'time': info1.hourly_data[i].time,
             info1.date.strftime('%m/%d/%Y_')+info1.product : info1.hourly_data[i].mid_price,
             info2.date.strftime('%m/%d/%Y_')+info2.product : info2.hourly_data[i].mid_price }        
        saatlik.append(pd.DataFrame(data=d).reset_index(drop=True))
    return saatlik


# In[33]:


def __calc_mp(hourly_data):
        i=0
        for data in hourly_data:
            mp = aux.find_arithmeticMean("self.product",data.bid_price, data.ask_price)
            hourly_data[i]['mid_price'] = mp
            i+=1
        return hourly_data


# In[24]:


def __parse_path(path):
    return path.split('\\')[-1].split('.')[0].split('_')


# In[25]:


def __findDate(date):
    return pd.Timestamp(date).date()


# @dataclass
# class HourlyData:
#     mid_price : pd.Series
#     time_slice : int
#     data_date: datetime.date
#     timeseries: pd.Series

# def ikile(info1,info2):
#     saatlik =[]
#     for i in range(23):
#         saatlik.append((info1.hourly_data[i],info2.hourly_data[i]))
#     return saatlik
