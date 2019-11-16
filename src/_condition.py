class Condition_Types:

    def __init__(self, data : pd.DataFrame = None) -> None :
        self._data=data
    
    def median(self) -> dict:
        pass

    def percentile(self, percentile_value : float) -> dict:
        pass

    def other_method(self):
        pass

class Condition():
    """Veriyi çeşitli koşulları baz alarak yeniden düzenlemek isteyebilirsiniz.
    """

    def __init__(self, data : pd.DataFrame = None) :
        self._data = data
        self.types = Condition_Types(data)
        self.values = None
        
     
    def implement(self) -> pd.DataFrame:
        """ _condition_value'e göre dalgaları yeniden düzenler
        """
        pass





condition = Condition('data')
condition.values=condition.types.median()
condition.implement()