class Condition_Types:

    def __init__(self,type,*arg):
        self.argumans=arg
        self.type = type

    def get(self):
        pass

    def median():
        pass

    def percentile(self):
        print(self.argumans[0])


class Condition:

    def __init__(self,condition_type=None, *arg ,data=None):
        self.condition_type = Condition_Types(condition_type,arg)


    def implement(self):
        pass