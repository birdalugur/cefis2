from dataclasses import dataclass
import numpy as np
import pandas as pd


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

    >>> data_of_range = range_creator.convert_range(data,100)

    >>> second_creator = Interval(range_method='width')

    >>> second_creator.convert_range(data,5)
    """

    def __init__(self, range_method):
       
        self.range_method = range_method

        self.__first_range = None
        self.__second_range = None                

    def __intervals(self,series,value):
        """Serinin, min ve max değeri arasında eşit aralıklı sayıları döndür.
        """
        min_s = series.min()-0.0000000001
        max_s = series.max()
        return np.linspace(min_s,max_s,value)

    def __width(self,series,value):
        min_s = series.min()-0.0000000000001
        max_s = series.max()
        return list(self.wrange(min_s,max_s,value))

    def wrange(self,start, stop, step):
        while True:
            yield start
            start = start + step
            if start == stop:
                break
            elif start > stop:
                yield stop
                break

    def __set_range(self,data,value):
        """range_method'a göre aralığın nasıl oluşturulacağını belirler.

        Parameters
        ----------        
        data : pandas.DataFrame        
        
        """
        if self.range_method == 'interval':
            self.__first_range = self.__intervals(data.duration,value)
            self.__second_range = self.__intervals(data.amplitude,value)

        elif self.range_method == 'width':
            self.__first_range = self.__width(data.duration,value)
            self.__second_range = self.__width(data.amplitude,value)

        else:
            raise ValueError('range_method: %s bulunamadı' %(self.range_method))

    def convert_range(self,data,value = None):
        """Bir DataFrame'e belirli aralık değerleri uygulayarak yeniden düzenler
        ve düzenlenmiş halini döndürür.

        Parameters
        ----------

        data: pandas.DataFrame
            Düzenlenecek veri seti

        value: int
            range_method 'interval' ise aralık sayısını belirtir.
            range_method 'width' ise her bir aralığın genişliğini belirtir.
        
        width: float, default: None
            Her bir aralığın genişlik miktarı. Bu parametre yalnızca range_method 'width' ise kullanılabilir.

        Returns
        -------
        pandas.DataFrame
        """
                   
        self.__set_range(data, value)
        
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
    def __init__(self, dataframe = None):
        self.data = dataframe
               

    #----------ALL PROPERTIES----------------------------
    @property
    def frequency(self):
        """ joint density ve frekansı içerir
        """
        return self.__get_frequency(self.data)

    @property
    def joint_density(self):
        return self.__create_joint(self.frequency)

    @property
    def horizontal_total_of_joint(self):
        return self.__horizontal_total(self.joint_density)

    @property
    def vertical_total_of_joint(self):
        return self.__vertical_total(self.joint_density)
    
    #---------------------------------------------------


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
    
    
    def __create_joint(self,df):
        """Bu method density, duration ve amplitude verileri içeren bir
            DataFrame'in pivot tablosunu oluşturur. Tablo, aynı zamanda
            density değerlerinin satır ve sütun toplamlarını da içerir.
        """
        
        pivot = pd.pivot_table(df, values='density', index=['duration'], columns='amplitude')
        return pivot

    def __horizontal_total(self, joint_dens):
        return joint_dens.agg('sum',axis=1)

    def __vertical_total(self, joint_dens):
        return joint_dens.agg('sum')


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
            con_density_table = self.joint_density/self.vertical_total_of_joint
            con_density = con_density_table.stack().to_frame('conditional_distribution').swaplevel(0,1).sort_index()          
            return Gosterim(con_density,con_density_table)

        #conditional density/x
        elif choice == 'duration':
            con_density_table = (self.joint_density.T/self.horizontal_total_of_joint).T
            con_density = con_density_table.stack().to_frame('conditional_distribution').sort_index()
            # con_density = con_density_table.stack().to_frame('conditional_distribution').swaplevel(0, 1, axis=0).sort_index()
            return Gosterim(con_density,con_density_table)

        else:
            raise Exception(
                "choice, 'duration' ya da 'amplitude' olarak ayarlanmalıdır'")



