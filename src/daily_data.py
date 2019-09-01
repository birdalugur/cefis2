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
        list: mid_price içeren saatlik df listesi
    """
    saatlik =[]
    for i in range(23):
        d = {'time': info1.hourly_data[i].time,
             info1.date.strftime('%m/%d/%Y_')+info1.product : info1.hourly_data[i].mid_price,
             info2.date.strftime('%m/%d/%Y_')+info2.product : info2.hourly_data[i].mid_price }        
        saatlik.append(pd.DataFrame(data=d).reset_index(drop=True))
    return saatlik

