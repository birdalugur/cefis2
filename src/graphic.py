#Bu bölümde grafik ile ilgili işlemler yapıldı
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
    return data.loc[state].plot.bar()