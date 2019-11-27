from dataclasses import dataclass
import numpy as np
import pandas as pd


def get_frequency(df):
    """frekansı hesaplar ve sıralı şekilde döndürür.
    """
    df = df.set_index('date')
    return df.groupby(df.columns.tolist()).size()\
            .reset_index().rename(columns={0: 'frequency'}).sort_values('frequency',ascending =False)\
                .reset_index(drop=True)


def joint_density(df):
    new_df= get_frequency(df)
    new_df['density'] = new_df['frequency']/new_df['frequency'].sum()
    pivot = pd.pivot_table(new_df, values='density', index=['duration'], columns=new_df.iloc[:,1].name)
    return pivot
    

def frequency(df,freq):
    if freq == 'default':
        return get_frequency(df)
    else:
        return df.groupby(pd.Grouper(key='date',freq=freq)).apply(get_frequency).droplevel(1)


def __density(df):
    new_df= get_frequency(df)
    new_df['density'] = new_df['frequency']/new_df['frequency'].sum()
    return new_df.drop('frequency',axis=1)


def density(df,freq):
    if freq == 'default':
        return __density(df)
    elif (freq == 'd')or(freq=='h'):
        return df.groupby(pd.Grouper(key='date',freq=freq)).apply(__density).droplevel(1)
    pass


def _vertical_total(df):
    pivot = pd.pivot_table(df, values='density', index=['duration'], columns=df.iloc[:,1].name)
    v_total = pivot.agg('sum')
    return pivot/v_total

def _horizontal_total(df):
    pivot = pd.pivot_table(df, values='density', index=['duration'], columns=df.iloc[:,1].name)
    h_total = pivot.agg('sum',axis=1)
    return pivot.T/h_total

def conditional_density(df,axis):
    name = df.iloc[:,1].name
    if axis =='y':
        piv = _vertical_total(df)
        return pd.melt(piv.reset_index(),id_vars='duration',value_vars=list(piv.columns[1:]))
    elif axis == 'x':
        piv = _horizontal_total(df)
        return pd.melt(piv.reset_index(),id_vars=name,value_vars=list(piv.columns[1:]))
    else:
        pass