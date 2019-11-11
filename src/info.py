import pandas as pd
import src.auxiliary_functions as aux
from platform import system

def __parse_path(path):
    if system() == 'Windows':
        return path.split('\\')[-1].split('.')[0].split('_')
    else:
        return path.split('/')[-1].split('.')[0].split('_')

def __findDate(date):
    return pd.Timestamp(date)

def get_productName(path):
    split_text = __parse_path(path)
    return split_text[1] + split_text[2]

def get_productDate(path):
    split_text = __parse_path(path)
    return __findDate(split_text[0])  
        

def get_detail(df):
    """DataFrame'e ait istatistiksel bilgi döndürür """
    detail_list = []
    time_list= df.index.levels[0].tolist()
    for t in time_list:
        detail_list.append(df.loc[t].describe())
    return pd.concat(detail_list,keys=time_list)

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

