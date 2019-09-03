#!/usr/bin/env python
# coding: utf-8

# In[30]:


def calc_density(df):
    df = df.groupby(df.columns.tolist()).size().reset_index().            rename(columns={0:'density'})
    return df


# In[71]:


# In[ ]:





# In[ ]:




