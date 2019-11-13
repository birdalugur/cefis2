import pandas as pd
import numpy as np

def groupby_date_time(df):
    """DataFrame'i tarih ve saate göre gruplar
    """
    df=df.reset_index()
    df_group=df.groupby([df.date.dt.floor('d'),df.date.dt.hour])
    return df_group


def average_of_series(*args):
    """verilerin aritmetik ortalamasını hesaplar ve döndürür.
    Parameters:        
        args: Her biri pd.Series olan değişken sayıda argüman alabilir
    Returns:
        pd.Series: argümanların aritmetik ortalaması
    """
    
    number=len(args)
    seri = pd.Series(data=sum(args)/number) 
    seri=seri.reset_index(drop=True)
    return seri

def mark_data(data):
    """Dalgaları bulmak için verileri işaretler
    """
    # mask the zeros
    s = data.eq(0)
    # merge the zeros to the wave after them
    m = np.sign(data).mask(s).bfill()
    # result
    marked_data = m.diff().ne(0).cumsum()
    marked_data.name='sign'
    return marked_data