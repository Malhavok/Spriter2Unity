__author__ = 'Malhavok'

from CurveCalc import CurveCalc

class CurveCalcSprite(CurveCalc):
    def __init__(self):
        super(self.__class__, self).__init__()

    def curve_to_editor_string(self, path, dataList, typeId, varName):
        outList = []

        outList.append('- curve:')

        for elem in dataList:
            outList.append('  - time: ' + str(elem['time']))
            outList.append('    value: {fileID: 21300000, guid: %s, type: 3}' % (str(elem['value']),))

        outList.append('  attribute: ' + varName)
        outList.append('  path: ' + path)
        outList.append('  classID: ' + str(typeId))
        outList.append('  script: {fileID: 0}')

        return '\n'.join(outList)

    def mangle_data(self, dataDict):
        timeKeys = sorted(dataDict.keys())
        numKeys = len(timeKeys)

        outList = []

        for idx in xrange(numKeys):
            time = timeKeys[idx]

            d1 = list(dataDict[time])

            elem = {'time': time, 'value': d1[0]}
            outList.append(elem)

        return outList
