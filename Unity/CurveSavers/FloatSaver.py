__author__ = 'Malhavok'

from SaversBase import SaversBase


# assumes that all passed parameters are 3 element tuple
# (value, inSlope, outSlope)
#
# to_string and to_editor_string are the same for float params
#
class FloatSaver(SaversBase):
    def __init__(self, setNameOrder, typeId, path, varName):
        super(FloatSaver, self).__init__(setNameOrder, typeId, path, varName)


    def _to_string(self):
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

            if marker is None:
                outList.append('  attribute: ' + self._saverVariableName)
            else:
                outList.append('  attribute: ' + self._saverVariableName + '.' + marker)

            pathStr = '  path:'
            if self._path is not None:
                pathStr = pathStr + ' ' + self._path

            outList.append(pathStr)

            outList.append('  classID: ' + str(self._typeId))
            outList.append('  script: {fileID: 0}')

        return '\n'.join(outList)


    def _to_editor_string(self):
        return self._to_string()
