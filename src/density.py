#!/usr/bin/env python
# coding: utf-8

# In[3]:


import plotly.graph_objects as go
import pandas as pd
import numpy as np


# In[30]:


def calc_density(df):
    df = df.groupby(df.columns.tolist()).size().reset_index().            rename(columns={0:'density'})
    return df


# In[ ]:





# In[40]:


def draw(x1,y1,z1):
    fig = go.Figure(data=[go.Mesh3d(x=x1,
                   y=y1,
                   z=z1,
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


# In[ ]:





# fig = go.Figure(data=[go.Mesh3d(x=[1,2,3,4,5],
#                    y=[2,323,4,5,6],
#                    z=[2,3,234,5,623],
#                    opacity=0.5,name="asd")])

# fig.update_layout(scene = dict(
#                     xaxis = dict(
#                          backgroundcolor="rgb(200, 200, 230)",
#                          gridcolor="white",
#                          showbackground=True,
#                          zerolinecolor="white",),
#                     yaxis = dict(
#                         backgroundcolor="rgb(230, 200,230)",
#                         gridcolor="white",
#                         showbackground=True,
#                         zerolinecolor="white"),
#                     zaxis = dict(
#                         backgroundcolor="rgb(230, 230,200)",
#                         gridcolor="white",
#                         showbackground=True,
#                         zerolinecolor="white",),),
#                     width=700,
#                     margin=dict(
#                     r=10, l=10,
#                     b=10, t=10)
#                   )

# In[ ]:




