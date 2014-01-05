__author__ = 'Malhavok'


from Curves import CurveBase


class CurveParam(object):
    def __init__(self, paramName, curveClass, curveClassCtorParams = None):
        super(CurveParam, self).__init__()

        assert curveClass is not None and issubclass(curveClass, CurveBase.CurveBase)

        self.__paramName = paramName
        self.__curveClass = curveClass
        self.__curveClassCtorParams = curveClassCtorParams


    def get_param_name(self):
        return self.__paramName


    def create_curve_instance(self):
        if not self.__curveClassCtorParams:
            return self.__curveClass()
        else:
            return self.__curveClass(*self.__curveClassCtorParams)
