from dataclasses import dataclass
import numpy as np
import pandas as pd


def get_frequency(df):
    """frekansı hesaplar ve sıralı şekilde döndürür.
    """
    return df.groupby(df.columns.tolist()).size()\
            .reset_index().rename(columns={0: 'frequency'}).sort_values('frequency',ascending =False)\
                .reset_index(drop=True)


def joint_density(df):
    new_df= get_frequency(df)
    new_df['density'] = new_df['frequency']/new_df['frequency'].sum()
    pivot = pd.pivot_table(new_df, values='density', index=['duration'], columns=new_df.iloc[:,1].name)
    return pivot

    


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



