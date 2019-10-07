import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dataclasses import dataclass


class Density:
    def __init__(self, dataframe):
        self.data = dataframe
        self.__data_range = None

        self.frequency = self.get_frequency(self.data)
        self.density_data = self._calc_density()
        self.joint_density = self.density_data.pivot(index='duration',columns='amplitude',values='density')

    @staticmethod
    def get_frequency(df):
        """Bir veri setindeki sayıların hangi sıklıkla yer aldığını döndürür.
        """
        df = df.groupby(df.columns.tolist()).size()\
            .reset_index().rename(columns={0: 'frequency'})
        return df        

    def _calc_density(self):
        df = self.frequency
        df['density'] = df['frequency']/df['frequency'].sum()
        return df
    
    # Aralık Uygulama İşlemleri----------------------------------------------------------------------

    def __create_range(self,series):
        """Serinin, min ve max değeri arasında eşit aralıklı sayıları döndür.
        """
        min_s = series.min()-0.0000000001
        max_s = series.max()
        return np.linspace(min_s,max_s,100)

    
    def get_current_range(self):
        """Nesnenin varsayılan aralığını döndürür.
        """
        return self.__data_range


    def set_range(self, incoming_range=None):
        """Mevcut nesneye bir aralık ataması yapmak için kullanılır.
        
        Parameters
        ----------
        incoming_range : numpy.ndarray, default None
            Nesneye atanacak aralık        
        """
        if incoming_range == None:
            self.data_range = self.__create_range(self.data)

        else:
            self.data_range = incoming_range
        
    def convert_range(self,dataframe):
        """Bir DataFrame'e belirli aralık değerleri uygulayarak yeniden düzenler.
        """
        range_dur = pd.cut(x=dataframe.duration, bins= self.__create_range(dataframe.duration))
        range_amp = pd.cut(x=dataframe.amplitude, bins= self.__create_range(dataframe.amplitude))
        return pd.concat([range_dur,range_amp],axis=1)

    #-------------------------------------------------------------------------------------------------

    @property
    def marginal_density(self):
        """Marjinal dağılımı döndürür."""
        return self.create_pivot(self.density_data)
        

    @staticmethod
    def create_pivot(df):
        """Bu method density, duration ve amplitude verileri içeren bir
            DataFrame'in pivot tablosunu oluşturur. Tablo, aynı zamanda
            density değerlerinin satır ve sütun toplamlarını da içerir.
        """
        pivot = pd.pivot_table(df, values='density', index=['duration'], columns='amplitude')        
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
