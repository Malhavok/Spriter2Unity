__author__ = 'Malhavok'


class SaversBase(object):
    def __init__(self, setNameOrder, typeId, path, varName):
        super(SaversBase, self).__init__()

        self._setNameOrder = setNameOrder
        self._typeId = typeId
        self._path = path
        self._saverVariableName = varName

        self._timeline = None
        self._data = {}


    def set_timeline(self, newTimeline):
        assert type(newTimeline) is list, 'Passed timeline is not a list: ' + str(type(newTimeline))
        assert len(newTimeline) > 0, 'Timeline have length less or equal 0: ' + str(len(newTimeline))

        self._timeline = newTimeline


    def add_dataset(self, setName, dataList):
        # note: dataList may contain values or tuple with values
        # depending on particular type of saver
        assert type(dataList) is list
        assert len(dataList) > 0

        self._data[setName] = dataList


    def __check_data(self):
        # all data and timeline have to have the same length
        assert self._timeline
        assert len(self._data) > 0

        for marker in self._setNameOrder:
            assert marker in self._data

        for valList in self._data.values():
            assert len(valList) == len(self._timeline)


    def to_string(self):
        self.__check_data()
        return self._to_string()


    def to_editor_string(self):
        self.__check_data()
        return self._to_editor_string()


    def _to_string(self):
        assert False and "This is to be inherited"


    def _to_editor_string(self):
        assert False and "This is to be inherited"
