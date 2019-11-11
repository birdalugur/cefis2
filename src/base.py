import pandas as pd

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