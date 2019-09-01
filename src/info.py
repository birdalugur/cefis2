#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import src.auxiliary_functions as aux
from dataclasses import dataclass
from datetime import datetime


# In[ ]:


@dataclass
class Info:
    path: str
    date: datetime.date
    product: str
    df: pd.DataFrame
    hourly_data: list


# In[ ]:


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


def __calc_mp(hourly_data):
    i=0
    for data in hourly_data:
        mp = aux.find_arithmeticMean("self.product",data.bid_price, data.ask_price)
        hourly_data[i]['mid_price'] = mp
        i+=1
    return hourly_data


# In[ ]:


def __parse_path(path):
    return path.split('\\')[-1].split('.')[0].split('_')


# In[ ]:


def __findDate(date):
    return pd.Timestamp(date).date()

