from dataclasses import dataclass
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Interval:
    """
    Bu sınıf, verileri belirli aralıklara yerleştirmek için tasarlanmıştır.
    Aralıklar oluşturulurken 2 ayrı yöntem kullanılır.

    Parameters
    ----------

    range_method  : str 
    aralık oluşturma yöntemi. 'interval' veya 'width' olabilir.            

    Example
    -------

    >>> data = pd.read_excel("data.csv")

    >>> range_creator = Interval(range_method='interval')

    >>> data_of_range = range_creator.convert_range(data)
    """

    def __init__(self, range_method):
       
        self.range_method = range_method

        self.__first_range = None
        self.__second_range = None

        self.__width = None        

    def __intervals(self,series):
        """Serinin, min ve max değeri arasında eşit aralıklı sayıları döndür.
        """
        min_s = series.min()-0.0000000001
        max_s = series.max()
        return np.linspace(min_s,max_s,100)

    def __width(self):
        pass

    def __set_range(self,data):
        """range_method'a göre aralık değerlerini belirler.

        Parameters
        ----------        
        data : pandas.DataFrame        
        
        """
        if self.range_method == 'interval':
            self.__first_range = self.__intervals(data.duration)
            self.__second_range = self.__intervals(data.amplitude)

        elif self.range_method == 'width':
            pass

        else:
            raise ValueError('range_method: %s bulunamadı' %(self.range_method))

    def convert_range(self,data,width = None):
        """Bir DataFrame'e belirli aralık değerleri uygulayarak yeniden düzenler
        ve düzenlenmiş halini döndürür.

        Parameters
        ----------

        data: pandas.DataFrame
            Düzenlenecek veri seti
        
        width: float, default: None
            Her bir aralığın genişlik miktarı. Bu parametre yalnızca range_method 'width' ise kullanılabilir.

        Returns
        -------
        pandas.DataFrame
        """
        if width != None:
            self.__width = width            
        self.__set_range(data)
        
        range_dur = pd.cut(x=data.duration, bins= self.__first_range)
        range_amp = pd.cut(x=data.amplitude, bins= self.__second_range)
        return pd.concat([range_dur,range_amp],axis=1)

    def _get_current_range(self):
        """Nesnenin, eksenlere göre varsayılan aralığını döndürür.

        Notes
        -----
        Bu method ile ilgili gelecekte düzenleme yapılması gerekmektedir.

        >>> obj = Density(data_of_6A_6B_U8)
        >>> obj.get_current_range()
        
        | 0 | 1       | 2          | 3          | 4          | ... | 87  |
        |---|---------|------------|------------|------------|-----|-----|
        | 0 | 1.000   | 5.191919   | 9.383838   | 13.575758  | ... | 326 |
        | 1 | -13.125 | -12.784091 | -12.443182 | -12.102273 | ... | 29  |
        
        """
        return pd.DataFrame([self.__first_range,self.__second_range]).T



class Density:
    def __init__(self, dataframe):
        self.data = dataframe
               

    @property
    def frequency(self):
        """ joint density ve frekansı içerir
        """
        return self.__get_frequency(self.data)

    @property
    def marginal_density(self):
        """Marjinal dağılımı döndürür."""
        return self.__create_marginal(self.frequency)  


    def __get_frequency(self,data):
        """Bir veri setindeki sayıların hangi sıklıkla yer aldığını döndürür.
        """
        df = data.groupby(data.columns.tolist()).size()\
            .reset_index().rename(columns={0: 'frequency'})

        df = self.__calculate_density(df)
        return df

    def __calculate_density(self, df):
        """Marjinal density hesaplar ve yeni bir sütun olarak ekler.
        """        
        df['density'] = df['frequency']/df['frequency'].sum()
        return df
    
    
    def __create_marginal(self,df):
        """Bu method density, duration ve amplitude verileri içeren bir
            DataFrame'in pivot tablosunu oluşturur. Tablo, aynı zamanda
            density değerlerinin satır ve sütun toplamlarını da içerir.
        """
        #TypeError alındığından pivot_table yerine pivot metodu kullanıldı
        #Fakat, Görsel olarak pivot_table daha uygun
        #pivot = pd.pivot_table(df, values='density', index=['duration'], columns='amplitude')
        #pivot = df.pivot(values='density', index='duration', columns='amplitude')        
        horizontal_total = pivot.agg('sum',axis=1)        
        pivot['sum'] = horizontal_total
        vertical_total=pivot.agg('sum')
        vertical_total.name = 'sum'
        pivot = pivot.append(vertical_total)
        return pivot


    def conditional_density(self, choice):
        """Koşullu dağılımı döndürür
        """

        #dataclass yalnızca, veriyi farklı şekillerde göstermek için kullanıldı.
        #sözlükde kullanılabilirdi
        @dataclass
        class Gosterim:
            normal:pd.DataFrame #grafikte bu kullanılacak
            pivot:pd.DataFrame

        #conditional density/y
        if choice == 'amplitude':
            df_piv_d = self.marginal_density.drop('sum', axis=1)
            #distribution_of_duration = (
             #   df_piv_d.iloc[:-1] / df_piv_d.iloc[-1]).stack().to_frame('conditional_distribution')
            distribution_of_pivot = df_piv_d.iloc[:-1] / df_piv_d.iloc[-1]
            distribution_of_amplitude = distribution_of_pivot.stack().to_frame('conditional_distribution').swaplevel(0,1).sort_index()

            #Her bir sütundaki değerler toplanıp son satıra yazdırılıyor.
            sutun_toplami=distribution_of_pivot.agg('sum')
            sutun_toplami.name = 'sum'
            distribution_of_pivot = distribution_of_pivot.append(sutun_toplami)

            return Gosterim(distribution_of_amplitude,distribution_of_pivot)
            #return distribution_of_duration

        #conditional density/x
        elif choice == 'duration':
            df_piv_a = self.marginal_density.transpose().drop('sum', axis=1)
            # distribution_of_amplitude = (
            #     df_piv_a.iloc[:-1] / df_piv_a.iloc[-1]).stack().to_frame('conditional_distribution')
            distribution_of_pivot = df_piv_a.iloc[:-1] / df_piv_a.iloc[-1]
            distribution_of_duration = distribution_of_pivot.stack().to_frame('conditional_distribution').swaplevel(0, 1, axis=0).sort_index()

            distribution_of_pivot = distribution_of_pivot.transpose()
            satir_toplami = distribution_of_pivot.agg('sum',axis=1)            
            distribution_of_pivot['sum'] = satir_toplami
            return Gosterim(distribution_of_duration,distribution_of_pivot)
            #return distribution_of_amplitude.swaplevel(0, 1, axis=0).sort_index()

        else:
            raise Exception(
                "choice, 'duration' ya da 'amplitude' olarak ayarlanmalıdır'")


#Bu bölümde grafik ile ilgili işlemler yapıldı
def draw_3d(df):
    """ 3 eksenli grafik çizer
        Parametre olarak verilen DataFrame, duration, amplitude ve conditional_distribution adında 3 sütun içermelidir.
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

# ## Usage

# ```python
# x = np.random.randn(5)
# y = np.random.randn(5)
# z = np.random.randn(5)
# df = pd.DataFrame(data=[x,y]).transpose()
# df.columns = ['duration','amplitude']
# density = Density(df)
# density.draw()
# ```
