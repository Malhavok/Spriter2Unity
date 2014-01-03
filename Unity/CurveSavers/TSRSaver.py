__author__ = 'Malhavok'

from SaversBase import SaversBase


# assumes that all passed parameters are 3 element tuples
# (value, inSlope, outSlope)
#
class TSRSaver(SaversBase):
    def __init__(self, setNameOrder, typeId, path, varName):
        super(TSRSaver, self).__init__(setNameOrder, typeId, path, varName)


    def _to_string(self):
        outList = []

        outList.append('- curve:')
        outList.append('    serializedVersion: 2')
        outList.append('    m_Curve:')

        for idx in xrange(len(self._timeline)):
            outList.append('    - time: ' + str(self._timeline[idx]))
            outList.append('      value: ' + self.__make_idx_value(idx, 0))
            outList.append('      inSlope: ' + self.__make_idx_value(idx, 1))
            outList.append('      outSlope: ' + self.__make_idx_value(idx, 2))
            outList.append('      tangentMode: 0')

        outList.append('    m_PreInfinity: 2')
        outList.append('    m_PostInfinity: 2')
        outList.append('  path: ' + self._path)

        return '\n'.join(outList)


    def _to_editor_string(self):
        outList = []

        for marker in self._setNameOrder:
            outList.append('- curve:')
            outList.append('    serializedVersion: 2')
            outList.append('    m_Curve:')

            for idx in xrange(len(self._timeline)):
                valueList = self._data[marker]
                value = valueList[idx]

                outList.append('    - time: ' + str(self._timeline[idx]))
                outList.append('      value: ' + str(value[0]))
                outList.append('      inSlope: ' + str(value[1]))
                outList.append('      outSlope: ' + str(value[2]))
                outList.append('      tangentMode: 0')

            outList.append('    m_PreInfinity: 2')
            outList.append('    m_PostInfinity: 2')
            outList.append('  attribute: ' + self._saverVariableName + '.' + marker)
            outList.append('  path: ' + self._path)
            outList.append('  classID: ' + str(self._typeId))
            outList.append('  script: {fileID: 0}')

        return '\n'.join(outList)


    def __make_idx_value(self, dataIdx, tupleIdx):
        outList = []

        for marker in self._setNameOrder:
            valueList = self._data[marker]
            valueElem = valueList[dataIdx]
            value = valueElem[tupleIdx]

            outList.append(marker + ': ' + str(value))

        return '{' + ', '.join(outList) + '}'
