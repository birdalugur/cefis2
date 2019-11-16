import pandas as pd


# # Taslak
class Condition_Types:

    def __init__(self, data : pd.DataFrame = None) -> None :
        self.data=data

    
    def median(self) -> dict:
        """pozitif medyan ve negatif medyanı döndürür.
        """
        pass

    def percentile(self, percentile_value : float) -> dict:
        pass

    def other_method(self):
        pass


class Condition():
    """Veriyi çeşitli koşulları baz alarak yeniden düzenlemek isteyebilirsiniz.
    """

    def __init__(self, data : pd.DataFrame = None) :
        self.condition_type = Condition_Types(data) 
        self._condition_value = None
        
    def set_type(self, method=None, params=None) -> None:
        if method == 'median':
            self._condition_value = self.condition_type.median()
        elif method == 'percentile':
            self._condition_value= self.condition_type.percentile(percentile_value = params)
        else:
            pass
    
    def implement(self) -> pd.DataFrame:
        """ _condition_value'e göre dalgaları yeniden düzenler
        """
        pass


# # Class'ın Uygulanması


kosul = Condition('data')

kosul.set_type(method='median')

result = kosul.implement()