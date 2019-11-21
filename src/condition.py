#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import src.change as change


class Sign:
    def __init__(self,data,pn=True):
        #__pn True ise pozitif ve negatif veriler ile ayrı çalışır.
        self.__pn = pn       
        
        
        #df'in sütunları alınıyor
        try:
            self.duration  = data['duration'].dt.seconds
        except:
            data.duration=pd.to_timedelta(data.duration.astype(str))
            self.duration  = data['duration'].dt.seconds
        
        self.amplitude = data.iloc[:,-1]
        self.date      = data['date']       
        
        #kullanılacak fonksiyonlar
        self._median     = None
        self._percentile = None
        self._is_provide = None
        
        #fonksiyona göre atanacak koşul değerleri
        self.duration_val    = None
        self.amplitude_val   = None
        self.duration_bools  = None
        self.amplitude_bools = None
        self.bools = None
        
        #pozitif-negatif durumuna göre atanacak fonksiyonlar
        if self.__pn==False:
            self._median     = self._direct_median
            self._percentile = self._direct_percentile
            self._is_provide = self._direct_is_provide
        elif self.__pn == True:            
            self._median     = self._pn_median
            self._percentile = self._pn_percentile 
            self._is_provide = self._pn_is_provide
            
                
    def medyan(self):
        """Medyan değerine göre verileri işaretler ve döndürür
        """
        self.duration_val  = self._median(self.duration)
        self.amplitude_val = self._median(self.amplitude)
        self.assign_bools()
        print('duration= '+str(self.duration_val))
        print('amplitude= '+str(self.amplitude_val))
        return self.sign_data(self.amplitude,self.bools)
        
        
    def percentile(self,percen_val):
        """Percentile değerine göre veriyi işaretler ve döndürür
        """
        self.duration_val=self._percentile(self.duration,percen_val)
        self.amplitude_val=self._percentile(self.amplitude,percen_val)
        self.assign_bools()
        print('duration= '+str(self.duration_val))
        print('amplitude= '+str(self.amplitude_val))
        return self.sign_data(self.amplitude,self.bools)
        
    def assign_bools(self):
        self.duration_bools= self._get_bools(data=self.duration,val=self.duration_val)       
        self.amplitude_bools= self._get_bools(self.amplitude,self.amplitude_val)
        self.bools = self.duration_bools & self.amplitude_bools
        
    def _get_bools(self,data,val) -> pd.Series:
        bools=data.apply(lambda x : self._is_provide(x,val))
        bools[0]=False
        return bools
    
    def _direct_is_provide(self,x,val):
        return abs(x)<=val
    
    def _pn_is_provide(self,x,val):
        if x <0:
            return abs(x)<=val['negatif']
        if x >0:
            return abs(x)<=val['pozitif']
    
    #>>>>>>>>>>>>>>>medyan ve percentile fonksiyonları>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def _pn_median(self,data) -> dict:
        """Pozitif ve negatif'i ayrı hesaplar
        """
        return {'pozitif': data[data>0].median(),'negatif': data[data<0].median()}
        
        
    def _direct_median(self,data):
        return data.median()
    
    def _direct_percentile(self,data,percent_val):
        return data.quantile(percent_val)
        
        
    def _pn_percentile(self,data, percent_val) -> dict:
        """Pozitif ve negatif'i ayrı hesaplar
        """
        return {'pozitif':
            data[data>0].quantile(percent_val),\
                'negatif':data[data<0].quantile(percent_val)}
    #<<<<<<<<<<<<<<<<medyan ve percentile fonksiyonları<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    def sign_data(self,data : pd.Series, bools : pd.Series) -> pd.Series:
        a=data.mask(bools).fillna(method='ffill')
        return np.sign(a).diff().ne(0).cumsum()


def apply(data, sign):
    """computes and returns the new wave according to the given signs.
    """
    name = data.iloc[:,-1].name
    print(name)
    new_data=data.groupby(sign).agg({'date':change.last_time,'duration':'sum',name:'sum'})    
    return new_data.reset_index(drop=True)

