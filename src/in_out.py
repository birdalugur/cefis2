#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import glob


# In[ ]:


def get_path(dir_path):
    """
    @type dir_path: str
    @param dir_path: okunacak klasöre ait path
    @rtype: list
    @returns: Belirtilen klasördeki excel dosyalarına ait yolun bir listesini döndürür.
    """

    files = [f for f in glob.glob(dir_path + "**/*.xlsx", recursive=True)]
    return files


# In[ ]:


def write_excel(path,df,file_name,prod_name):
    directory_path = path+'\\'+prod_name + '\\'
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        if not os.path.exists(directory_path+'detail\\'):
            os.mkdir(directory_path+'detail\\')
    writer = pd.ExcelWriter(directory_path+ file_name+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


# In[ ]:


def write(name,full):
    """Excel'e yazar
    Parameters:
        name (str): """
    
    path = 'C:\\Users\\ugur.eren\\Python Codes\\cefis2\\out\\'
    hour_series = pd.date_range('2018-01-01-18', periods=23, freq='H')
    hour_series = hour_series.time
    for i in range(23):
        fn = hour_series[i].strftime("%H-%M-%S")        
        write_excel(path=path,df=full.loc[hour_series[i]].dropna(),file_name=fn,prod_name=name)
        write_excel(path=path,df=full.loc[hour_series[i]].describe(),file_name=fn+'_detail', prod_name=name+'\\detail')     

