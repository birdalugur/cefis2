import pandas as pd


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
    atick = values.iloc[:,0].pnltick/values.iloc[:,0].ticksize
    btick = values.iloc[:,1].pnltick/values.iloc[:,1].ticksize
    size = len(a_series)
    spread = size*[0]
    for i in range(size): 
        try:
            spread[i+1] = (((a_series.iat[i+1] - a_series.iat[i])*atick) - ((b_series.iat[i+1] - b_series.iat[i])*btick)) +spread[i] 
        except:            
            pass
    return pd.Series(data=spread,index=pair.date,name=a_series.name+'_'+b_series.name)


