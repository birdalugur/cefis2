#Bu bölümde grafik ile ilgili işlemler yapıldı
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def draw_3d(df):
    """ 3 eksenli grafik çizer
        Parametre olarak verilen DataFrame, duration, amplitude ve conditional_distribution adında 3 sütun içermelidir.
        Sütun veriler yalnıca numeric olmalıdır
    """
    min_value = df.amplitude.min()
    max_value = df.amplitude.max()
    
    fig = go.Figure(data=[go.Mesh3d(x=df.duration,
                                    y=df.amplitude,
                                    z=df.conditional_distribution,
                                    opacity=0.5)])
    fig.update_layout(scene=dict(
        xaxis=dict(
            backgroundcolor="rgb(200, 200, 230)",
            # title="duration",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",),
        yaxis=dict(
            backgroundcolor="rgb(230, 200,230)",
            # title="amplitude",
            gridcolor="white",
            showbackground=True,
            range=[min_value,max_value],
            zerolinecolor="white"),
        zaxis=dict(
            backgroundcolor="rgb(230, 230,200)",
            # title = "conditional density",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",),),
        width=700,
        margin=dict(
        r=10, l=10,
        b=10, t=10)
    )
    return fig


def draw_2d(df,axis='y'):
    if axis == 'y':
        all_amplitude = df.index.get_level_values(0).unique()
        for amp in all_amplitude:
            current = df.loc[amp]
            fig = px.line(current.reset_index(), x='duration', y='conditional_distribution',\
                         title= "amplitude: " + str(amp))
            fig.show()
            
    elif axis == 'x':
        all_duration = df.index.get_level_values(0).unique()
        for dur in all_duration:
            current = df.loc[dur]
            fig = px.line(current.reset_index(), x='amplitude', y='conditional_distribution',title= "duration: " + str(dur))
            fig.show()
    
    else:
        raise ValueError('Geçersiz eksen değeri')




def conditional_drawing(data, state):
    """ Interval tipinde veriler içeren bir dataframe'den grafik oluşturmak için kullanılır.

    Parameters
    ----------
    data: pandas.DataFrame
        Aralıklar ile ifade edilmiş df veri yapısı
    state:
        Condition durumu
    Returns
    -------
    matplotlib.axes.Axes
    """
    return data.loc[state].plot.bar().show()

def _split_product(df):
    """MultiIndex dataframi ürün bazında ayırır ve tüm günleri birleştirir
    """
    idx = pd.IndexSlice
    df = df.set_index('time')
    products = list(df.columns.get_level_values(1).unique())
    product_list = {}
    for product in products:
        urun =df.loc[:,idx[:,product]]
        urun = urun.stack(level=0).reset_index().drop('level_1',axis=1)
        product_list[product] = urun        
    return product_list  

def spread_scatter(hourly_spread):
    """
    Parameters
    ----------
    hourly_spread (dict) : Belirli bir saate ait, tüm ürünleri içeren spread verisi
    """
    hourly_spread = _split_product(hourly_spread)
    while hourly_spread:
        item = hourly_spread.popitem()[1]
        px.scatter(item, x="time", y=item.columns[1]).show()


def scatter_all_days(df):
    fig = go.Figure()
    size = df.columns.size
    for i in range(size):
        data = df.iloc[:,i]
        name = df.columns.values.item(i).strftime("%m. %d. %Y")
        fig.add_trace(
            go.Scatter(
                x = df.index,
                y = data,
                name = name            
            )
        )
    return fig


def draw_spread(prod_name, hour_indice, spread, amplitude):
    fig = go.Figure()
    specific_spread = aux.extract_product(spread[hour_indice],prod_name)
    time_serie = aux.get_time(hour_indice,prod_name)
    count = time_serie.index.max()+1
    for i in range(count):
        data = AB.iloc[:,i].loc[x.loc[0].level_1]
        fig.add_trace(go.Scatter(
                x=data.index,
                y=data,
                name=str(i),
                opacity=0.8))
    return fig