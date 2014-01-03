__author__ = 'Malhavok'

import Curves
import CurveSavers

from Transform import Transform


class TSRCurveHelper(object):
    LINEAR = 0
    INSTANT = 1
    DUMMY_0 = 2
    DUMMY_1 = 3


    def __init__(self, setNameOrderType, variableBaseName, path):
        super(TSRCurveHelper, self).__init__()

        setNameOrder = [keyName for keyName, _keyType in setNameOrderType]

        self.__saver = CurveSavers.TSRSaver.TSRSaver(setNameOrder, Transform.type, path, variableBaseName)
        self.__saverFilled = False

        self.__curves = self.__create_curve_objects(setNameOrderType)


    def add_key_frame(self, time, keyName, value):
        keyCurve = self.__get_key_curve(keyName)
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

        for keyName in self.__curves:
            valueList = []
            curve = self.__get_key_curve(keyName)

            for timeKey in timeLine:
                timeValues = curve.get_point_with_in_out_slopes(timeKey)
                valueList.append(timeValues)

            self.__saver.add_dataset(keyName, valueList)

        self.__saverFilled = True


    def __get_key_curve(self, keyName):
        assert keyName in self.__curves
        return self.__curves[keyName]


    def __create_curve_objects(self, setNameOrderType):
        outDict = {}

        for keyName, keyType in setNameOrderType:
            newObj = None

            if keyType == TSRCurveHelper.LINEAR:
                newObj = Curves.CurveLinear.CurveLinear()
            elif keyType == TSRCurveHelper.INSTANT:
                newObj = Curves.CurveInstant.CurveInstant()
            elif keyType == TSRCurveHelper.DUMMY_0:
                newObj = Curves.CurveDummy.CurveDummy(0.0)
            elif keyType == TSRCurveHelper.DUMMY_1:
                newObj = Curves.CurveDummy.CurveDummy(1.0)

            assert newObj is not None

            outDict[keyName] = newObj

        return outDict



class TSRCurveWorker(object):
    LINEAR = 'linear'
    INSTANT = 'instant'
    DUMMY_0 = 'dummy_0'
    DUMMY_1 = 'dummy_1'


    def __init__(self, setNameOrderType, variableBaseName):
        super(TSRCurveWorker, self).__init__()

        self.__setNameOrderType = setNameOrderType
        self.__variableBaseName = variableBaseName

        self.__workerNameOrderType = self.__create_worker_name_order_type()

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
            newHelper = TSRCurveHelper(self.__workerNameOrderType, self.__variableBaseName, path)
            self.__data[path] = newHelper

        return self.__data[path]


    def __create_worker_name_order_type(self):
        outList = []

        for keyName, keyType in self.__setNameOrderType:
            newType = None

            if keyType == TSRCurveWorker.LINEAR:
                newType = TSRCurveHelper.LINEAR
            elif keyType == TSRCurveWorker.INSTANT:
                newType = TSRCurveHelper.INSTANT
            elif keyType == TSRCurveWorker.DUMMY_0:
                newType = TSRCurveHelper.DUMMY_0
            elif keyType == TSRCurveWorker.DUMMY_1:
                newType = TSRCurveHelper.DUMMY_1

            assert newType is not None, 'Failed to map curve worker type to curve helper type for: "' + str(keyType) + '"'

            outList.append((keyName, newType))

        return outList
