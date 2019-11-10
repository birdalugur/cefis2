import pandas as pd

def group_by_spread(df_mp,values):
    """df_mp'ı tarih ve saate göre gruplar ve her bir gruba get_spread fonksiyonunu uygular
    Parameters
    ----------
    df_mp (pandas.DataFrame) : mid price 
    values (dict): ticksize değerleri
    Returns
    pd.DataFrame : pair'in spread değeri
    """
    df_mp=df_mp.reset_index()
    mp_group=df_mp.groupby([df_mp.date.dt.floor('d'),df_mp.date.dt.hour])
    spread_series=mp_group.apply(lambda x : get_spread(x,values))
    df_spread=pd.DataFrame(spread_series).droplevel([0,1])
    return df_spread

def get_spread(pair,values):
    """6A ve 6B gibi mid_price verisinden SPREAD verisini üretir.
    Parameters:
        pair(pandas.DataFrame):
        values(dict): ticksize değerleri
    Returns:
        pd.Series: Hesaplanmış spread verisi
    """
    a_series=pair.iloc[:,1]
    b_series=pair.iloc[:,2]
    atick = values['a_PNLTICK']/values['a_TICKSIZE']
    btick = values['b_PNLTICK']/values['b_TICKSIZE']
    size = len(a_series)
    spread = size*[0]
    for i in range(size): 
        try:
            spread[i+1] = (((a_series.iat[i+1] - a_series.iat[i])*atick) - ((b_series.iat[i+1] - b_series.iat[i])*btick)) +spread[i] 
        except:            
            pass
    return pd.Series(data=spread,index=pair.date,name=a_series.name+'_'+b_series.name)