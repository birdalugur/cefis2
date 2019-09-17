#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import src.auxiliary_functions as aux
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class Info:
    path: str
    date: datetime.date
    product: str
    df: pd.DataFrame
    hourly_data: list


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
    

def __calc_mp(hourly_data):
    i=0
    for data in hourly_data:
        mp = aux.find_arithmeticMean(data.bid_price, data.ask_price)
        hourly_data[i]['mid_price'] = mp
        i+=1
    return hourly_data


def __parse_path(path):
    return path.split('\\')[-1].split('.')[0].split('_')


def __findDate(date):
    #return pd.Timestamp(date).date()
    return pd.Timestamp(date)

def get_productName(path):
    split_text = __parse_path(path)
    return split_text[1] + split_text[2]


def get_productDate(path):
    split_text = __parse_path(path)
    return __findDate(split_text[0])


def get_mid_price(frame):
    return aux.find_arithmeticMean(frame.bid_price, frame.ask_price)
    
def create_name(name,date):
    return date.strftime('%m/%d/%Y_') + name


def match_products(infoList):
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



def split_df(df,hour):
    """Verileri 1er saatlik dilimlere böler(23 ayrı df).
    Parameters:
        df (dataframe):
        hour (int): varsayılan olarak 1. Gelecekte, asal olmayan saatlik veri için değiştirilebilir.
    Returns:
        list: Saatlik olarak bölünmüş df'lerin bir listesi."""
    return np.array_split(df.drop(df.index[len(df)-1]),hour)