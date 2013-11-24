__author__ = 'Malhavok'

from CurveCalc import CurveCalc

class CurveCalcInstant(CurveCalc):
    def __init__(self):
        super(self.__class__, self).__init__()

    def curve_to_editor_string(self, path, dataList, typeId, varName):
        outList = []

        outList.append('- curve:')
        outList.append('    serializedVersion: 2')
        outList.append('    m_Curve:')

        for elem in dataList:
            outList.append('    - time: ' + str(elem['time']))
            outList.append('      value: ' + str(elem['value']))
            outList.append('      inSlope: Infinity')
            outList.append('      outSlope: Infinity')
            outList.append('      tangentMode: 31') # i found it like that in a test animation

        outList.append('    m_PreInfinity: 2')
        outList.append('    m_PostInfinity: 2')
        outList.append('  attribute: ' + varName)
        outList.append('  path: ' + path)
        outList.append('  classID: ' + str(typeId))
        outList.append('  script: {fileID: 0}')

        return '\n'.join(outList)

    def make_value(self, keyGroup):
        return str(keyGroup)

    def mangle_data(self, dataDict):
        timeKeys = sorted(dataDict.keys())

        outList = []
        numKeys = len(timeKeys)

        for idx in xrange(numKeys):
            time = timeKeys[idx]
            d1 = dataDict[time]

            elem = {'time': time, 'value': d1}
            outList.append(elem)

        return outList
