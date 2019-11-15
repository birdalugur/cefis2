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
    Parameters
    ----------
    data (pd.Series): Negatif,pozitif ve 0 içerebilen sayı dizisi
    Return
    ------
    signs (pd.Series): 1,1,1,2,2,3,3,3,4,5,6,6..vs gibi işaretlenmiş seri
    """
    # mask the zeros
    s = data.eq(0)
    # merge the zeros to the wave after them
    m = np.sign(data).mask(s).bfill()
    # result
    marked_data = m.diff().ne(0).cumsum()
    marked_data.name='sign'
    return marked_data

def to_series(df):
    """DataFrame'i pandas.Series'e dönüştürür.
       df 2 sütuna sahiptir. Biri 'date' diğeri 'pair_name'(6AU8_6BU8 gibi)
    """
    df=df.set_index('date')
    serie= df.squeeze()
    return serie


def clean_data(pair):
    """Bir serideki 0'ları ve nanları kaldırır
    Parameters
    ----------
    pair (pd.Series) : Temizlenecek veri
    Return
    ------
    cleared_data (pd.Series)
    """
    return pair[pair!=0].dropna()