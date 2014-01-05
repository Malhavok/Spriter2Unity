__author__ = 'Malhavok'


class CurveParam(object):
    def __init__(self, paramName, curveClass, valueModLambda = None, curveClassCtorParams = None):
        super(CurveParam, self).__init__()

        self.__paramName = paramName
        self.__curveClass = curveClass
        self.__curveClassCtorParams = curveClassCtorParams
        self.__valueModLambda = valueModLambda


    def get_param_name(self):
        return self.__paramName


    def create_curve_instance(self):
        if not self.__curveClassCtorParams:
            return self.__curveClass()
        else:
            return self.__curveClass(*self.__curveClassCtorParams)


    def modify_value(self, oldValue):
        assert oldValue is not None

        if not self.__valueModLambda:
            retValue = oldValue
        else:
            retValue = self.__valueModLambda(oldValue)

        assert retValue is not None, 'Unable to modify value via lambda, maybe function doesnt return a value?'
        return retValue



class CurveHelper(object):
    def __init__(self, setCurveParamList, saverClass, savedObjectType, variableBaseName, path):
        super(CurveHelper, self).__init__()

        setNameOrder = [curveParam.get_param_name() for curveParam in setCurveParamList]

        self.__saver = saverClass(setNameOrder, savedObjectType, path, variableBaseName)
        self.__saverFilled = False

        self.__curves = {}
        self.__curveParams = {}

        self.__create_curve_and_curveParams_objects(setCurveParamList)


    def add_key_frame(self, time, keyName, value):
        assert keyName in self.__curves
        keyCurve = self.__curves[keyName]
        keyCurve.add_point(time, value)


    def fill_with_curve_time_lines(self, dataSet):
        tmpSet = set()

        for curve in self.__curves.values():
            timeListSet = set(curve.get_all_keys())
            tmpSet = tmpSet.union(timeListSet)

        return dataSet.union(tmpSet)


    def to_string(self, timeLine):
        self.__fill_saver(timeLine)
        return self.__saver.to_string()


    def to_editor_string(self, timeLine):
        self.__fill_saver(timeLine)
        return self.__saver.to_editor_string()


    def __fill_saver(self, timeLine):
        if self.__saverFilled:
            return

        self.__saver.set_timeline(timeLine)

        for keyName in self.__curves.keys():
            valueList = []
            curve = self.__curves[keyName]
            curveParam = self.__curveParams[keyName]

            for timeKey in timeLine:
                timeValue, inSlope, outSlope = curve.get_point_with_in_out_slopes(timeKey)
                modValue = curveParam.modify_value(timeValue)
                valueList.append((modValue, inSlope, outSlope))

            self.__saver.add_dataset(keyName, valueList)

        self.__saverFilled = True


    def __create_curve_and_curveParams_objects(self, setCurveParamList):
        for curveParam in setCurveParamList:
            newObj = curveParam.create_curve_instance()
            assert newObj is not None

            self.__curves[curveParam.get_param_name()] = newObj
            self.__curveParams[curveParam.get_param_name()] = curveParam



class CurveWorker(object):
    def __init__(self, setCurveParamList, curveSaverClass, savedObjectType, variableBaseName):
        super(CurveWorker, self).__init__()

        self.__setCurveParamList = setCurveParamList
        self.__variableBaseName = variableBaseName

        self.__curveSaverClass = curveSaverClass
        self.__savedObjectType = savedObjectType

        self.__data = {}

        self.__timeKeys = None


    def add_key_frame(self, time, path, key, value):
        helper = self.__get_helper_at(path)
        helper.add_key_frame(time, key, value)


    def to_string(self):
        self.__generate_time_keys()
        outList = []

        for helper in self.__data.values():
            outList.append(helper.to_string(self.__timeKeys))

        return '\n'.join(outList)


    def to_editor_string(self):
        self.__generate_time_keys()
        outList = []

        for helper in self.__data.values():
            outList.append(helper.to_editor_string(self.__timeKeys))

        return '\n'.join(outList)


    def __generate_time_keys(self):
        # this method assumes that no operations on time are made
        # so all time keys will be exactly the same no matter what
        # (like const floats). That's why check for equality for
        # floats seems like a good idea here
        if self.__timeKeys:
            return

        tmpSet = set()
        for helper in self.__data.values():
            tmpSet = helper.fill_with_curve_time_lines(tmpSet)

        self.__timeKeys = sorted(list(tmpSet))

        assert len(self.__timeKeys) > 0, 'Failed to fill temporary set with values'


    def __get_helper_at(self, path):
        if path not in self.__data:
            newHelper = CurveHelper(
                self.__setCurveParamList,
                self.__curveSaverClass,
                self.__savedObjectType,
                self.__variableBaseName,
                path
            )
            self.__data[path] = newHelper

        return self.__data[path]
