#!/usr/bin/env python
# coding: utf-8

import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Density:
    def __init__(self,dataframe):
        self.data = dataframe
        self.density_data = self._calc_density()
        
    def _calc_density(self):
        df = self.data.groupby(self.data.columns.tolist()).size().reset_index().rename(columns={0:'density'})
        df['density'] = df['density']/df['density'].sum()
        return df
    
    @property
    def marginal_distribution(self):
        """Marjinal dağılımı döndürür."""
        return self.create_pivot(self.density_data)

    @staticmethod
    def create_pivot(df):
        """Bu method density, duration ve amplitude verileri içeren bir
            DataFrame'in pivot tablosunu oluşturur. Tablo, aynı zamanda
            density değerlerinin satır ve sütun toplamlarını da içerir.
        """
        return pd.pivot_table(df, values='density', index=['duration'],columns='amplitude',margins=True)
    
    def dagilim_hesapla(self):
        df_piv_d = self.marginal_distribution.drop('All',axis=1)
        distribution_of_duration = (df_piv_d.iloc[:-1]/ df_piv_d.iloc[-1]).stack().to_frame('marginal_distribution')
        return distribution_of_duration

    
    def draw(self):
        df = self.density_data
        fig = go.Figure(data=[go.Mesh3d(x=df.duration,
                       y=df.amplitude,
                       z=df.density,
                       opacity=0.5,name="asd")])
        fig.update_layout(scene = dict(
                        xaxis = dict(
                             backgroundcolor="rgb(200, 200, 230)",
                             gridcolor="white",
                             showbackground=True,
                             zerolinecolor="white",),
                        yaxis = dict(
                            backgroundcolor="rgb(230, 200,230)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white"),
                        zaxis = dict(
                            backgroundcolor="rgb(230, 230,200)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",),),
                        width=700,
                        margin=dict(
                        r=10, l=10,
                        b=10, t=10)
                      )
        return fig

    


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