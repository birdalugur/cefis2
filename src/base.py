def groupby_date_and_time(df):
    """DataFrame'i tarih ve saate göre gruplar
    """
    df=df.reset_index()
    df_group=df.groupby([df.date.dt.floor('d'),df.date.dt.hour])
    return df_group