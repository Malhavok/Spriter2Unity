__author__ = 'Malhavok'

import math

class CurveCalc(object):
    def __init__(self):
        self.info = {}
        self.markers = ['x', 'y', 'z', 'w']


    def add_info(self, path, time, values):
        if path not in self.info:
            self.info[path] = {}

        self.info[path][time] = values

    def get_data(self):
        outDict = {}

        for path in self.info:
            if path is None:
                continue

            outData = self.mangle_data(self.info[path])
            outDict[path] = outData

        return outDict

    def to_editor_string(self, typeId, varName):
        dataDict = self.get_data()

        outList = []

        for path in dataDict.keys():
            tmpVar = self.curve_to_editor_string(path, dataDict[path], typeId, varName)
            if tmpVar is None:
                continue
            outList.append(tmpVar)

        if len(outList) == 0:
            return None

        return '\n'.join(outList)

    def to_string(self):
        dataDict = self.get_data()

        outList = []

        for path in dataDict.keys():
            tmpVar = self.curve_to_string(path, dataDict[path])
            if tmpVar is None:
                continue
            outList.append(tmpVar)

        if len(outList) == 0:
            return None

        return '\n'.join(outList)

    def curve_to_editor_string(self, path, dataList, typeId, varName):
        if dataList is None:
            return None

        outList = []
        numElems = len(dataList[0]['value'])

        for idx in xrange(numElems):
            outList.append('- curve:')
            outList.append('    serializedVersion: 2')
            outList.append('    m_Curve:')

            for elem in dataList:
                outList.append('    - time: ' + str(elem['time']))
                outList.append('      value: ' + str(elem['value'][idx]))
                outList.append('      inSlope: ' + str(elem['inSlope'][idx]))
                outList.append('      outSlope: ' + str(elem['outSlope'][idx]))
                outList.append('      tangentMode: ' + str(elem['tangentMode']))

            outList.append('    m_PreInfinity: 2')
            outList.append('    m_PostInfinity: 2')
            outList.append('  attribute: ' + varName + '.' + self.markers[idx])
            outList.append('  path: ' + path)
            outList.append('  classID: ' + str(typeId))
            outList.append('  script: {fileID: 0}')

        return '\n'.join(outList)

    def curve_to_string(self, path, dataList):
        if dataList is None:
            return None

        outList = []

        outList.append('- curve:')
        outList.append('    serializedVersion: 2')
        outList.append('    m_Curve:')

        for elem in dataList:
            outList.append('    - time: ' + str(elem['time']))
            outList.append('      value: ' + self.make_value(elem['value']))
            outList.append('      inSlope: ' + self.make_value(elem['inSlope']))
            outList.append('      outSlope: ' + self.make_value(elem['outSlope']))
            outList.append('      tangentMode: ' + str(elem['tangentMode']))

        outList.append('    m_PreInfinity: 2')
        outList.append('    m_PostInfinity: 2')
        outList.append('  path: ' + path)

        return '\n'.join(outList)

    def make_value(self, keyGroup):
        outList = []
        for idx in xrange(len(keyGroup)):
            outList.append(self.markers[idx] + ': ' + str(keyGroup[idx]))

        return '{' + ', '.join(outList) + '}'

    def mangle_data(self, dataDict):
        timeKeys = sorted(dataDict.keys())

        outList = []

        numKeys = len(timeKeys)
        if numKeys < 2:
            return None

        for idx in xrange(numKeys):
            time = timeKeys[idx]
            time2 = timeKeys[(idx + 1) % numKeys]

            d1 = list(dataDict[time])
            d2 = list(dataDict[time2])

            if len(d1) != len(d2):
                print 'ERROR: bad data list'
                print d1, d2
                print 'base data'
                print dataDict
                exit(1)

            elem = self.calc_elems(time, time2, d1, d2)
            elem['time'] = time

            outList.append(elem)

        # fix slopes
        for idx in xrange(len(outList)):
            nextIdx = (idx + 1) % len(outList)

            outList[nextIdx]['inSlope'] = outList[idx]['outSlope']

        return outList

    def calc_elems(self, x1, x2, d1, d2):
        outDict = {}

        outDict['value'] = d1
        outDict['inSlope'] = []
        outDict['outSlope'] = []

        # this number is deeply magical, i'm currently setting it to any value...
        # read: http://answers.unity3d.com/questions/313276/undocumented-property-keyframetangentmode.html
        # if it won't work i'll set it to 0 and interpolate by hand
        outDict['tangentMode'] = 0

        for idx in xrange(len(d1)):
            v1 = d1[idx]
            v2 = d2[idx]

            if idx != 2:
                slopeTg = (v1 - v2) / (x1 - x2)

                if math.fabs(slopeTg) < 1e-4:
                    slopeTg = 0.0

                # i'm adding it to both in and out slopes, didn't see changes
                # in linear movements
                outDict['inSlope'].append(slopeTg)
                outDict['outSlope'].append(slopeTg)
            else:
                outDict['inSlope'].append('Infinity')
                outDict['outSlope'].append('Infinity')

        return outDict
