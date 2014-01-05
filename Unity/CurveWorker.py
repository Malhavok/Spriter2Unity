__author__ = 'Malhavok'


def kahan_range(start, stop, step):
    # yields from start (including) to stop (excluding)

    # taken from:
    # http://stackoverflow.com/questions/4189766/python-range-with-step-of-type-float
    # remember kids: kahan sumation is good, google it and use it wisely
    assert step > 0.0
    total = start
    compo = 0.0
    while total < stop:
        yield total
        y = step - compo
        temp = total + y
        compo = (temp - total) - y
        total = temp



class _CurveWorkerHelper(object):
    def __init__(self, setCurveParamList, saverClass, savedObjectType, variableBaseName, path):
        super(_CurveWorkerHelper, self).__init__()

        setNameOrder = [curveParam.get_param_name() for curveParam in setCurveParamList]

        self.__saver = saverClass(setNameOrder, savedObjectType, path, variableBaseName)
        self.__saverFilled = False

        self.__curves = {}
        self.__create_curve_objects(setCurveParamList)


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

            for timeKey in timeLine:
                timeValue, inSlope, outSlope = curve.get_point_with_in_out_slopes(timeKey)
                valueList.append((timeValue, inSlope, outSlope))

            self.__saver.add_dataset(keyName, valueList)

        self.__saverFilled = True


    def __create_curve_objects(self, setCurveParamList):
        for curveParam in setCurveParamList:
            newObj = curveParam.create_curve_instance()
            assert newObj is not None

            self.__curves[curveParam.get_param_name()] = newObj



class CurveWorker(object):
    FPS = 60.0

    def __init__(self, setCurveParamList, curveSaverClass, savedObjectType, variableBaseName, continuousTimeLine = False):
        super(CurveWorker, self).__init__()

        self.__setCurveParamList = setCurveParamList
        self.__variableBaseName = variableBaseName

        self.__curveSaverClass = curveSaverClass
        self.__savedObjectType = savedObjectType

        self.__data = {}

        self.__timeKeys = None
        self.__continuousTimeLine = continuousTimeLine


    def add_key_frame(self, time, path, key, value):
        if path is None:
            return

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

        if self.__continuousTimeLine:
            self.__make_timeline_continuous()

        assert len(self.__timeKeys) > 0, 'Failed to fill temporary set with values'


    def __make_timeline_continuous(self):
        # this here assumes that a timeKeys are generated and just waiting
        # to be modified
        step = 1.0 / CurveWorker.FPS
        start = self.__timeKeys[0]
        end = self.__timeKeys[-1]

        newList = []
        for elem in kahan_range(start, end, step):
            newList.append(elem)
        newList.append(end)

        self.__timeKeys = newList


    def __get_helper_at(self, path):
        if path not in self.__data:
            newHelper = _CurveWorkerHelper(
                self.__setCurveParamList,
                self.__curveSaverClass,
                self.__savedObjectType,
                self.__variableBaseName,
                path
            )
            self.__data[path] = newHelper

        return self.__data[path]
