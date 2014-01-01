__author__ = 'Malhavok'

import math
from CurveCalc import CurveCalc

class CurveCalcRot(CurveCalc):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.numSamples = 60


    def add_angle_info(self, path, time, angle):
        if path not in self.info:
            self.info[path] = {}

        if angle is None:
            self.info[path][time] = None
            return

        clampedAngle = math.fmod(angle, 2.0 * math.pi)
        assert(0.0 <= clampedAngle < 2.0 * math.pi)
        self.info[path][time] = clampedAngle


    def mangle_data(self, dataDict):
        self.fix_holes(dataDict)
        newDataDict = self.interpolate(dataDict)

        timeKeys = sorted(newDataDict.keys())

        outList = []

        numKeys = len(timeKeys)
        if numKeys < 2:
            return None

        for idx in xrange(numKeys):
            time = timeKeys[idx]
            time2 = timeKeys[(idx + 1) % numKeys]

            angle1 = newDataDict[time]
            angle2 = newDataDict[time2]

            elem = self.calc_elems(time, time2, angle1, angle2)
            elem['time'] = time

            outList.append(elem)

        return outList

    def calc_elems(self, x1, x2, angle1, angle2):
        outDict = {}

        outDict['value'] = [0.0, 0.0, math.sin(angle1 / 2.0), math.cos(angle1 / 2.0)]
        outDict['angle'] = angle1
        outDict['inSlope'] = []
        outDict['outSlope'] = []

        d1 = outDict['value']
        d2 = [0.0, 0.0, math.sin(angle2 / 2.0), math.cos(angle2 / 2.0)]

        # this number is deeply magical, i'm currently setting it to any value...
        # read: http://answers.unity3d.com/questions/313276/undocumented-property-keyframetangentmode.html
        outDict['tangentMode'] = 0

        for idx in xrange(len(d1)):
            v1 = d1[idx]
            v2 = d2[idx]

            slopeTg = (v1 - v2) / (x1 - x2)

            if math.fabs(slopeTg) < 1e-4:
                slopeTg = 0.0

            # i'm adding it to both in and out slopes, didn't see changes
            # in linear movements
            outDict['inSlope'].append(slopeTg)
            outDict['outSlope'].append(slopeTg)

        return outDict


    def interpolate(self, angleDict):
        availableKeys = sorted(angleDict.keys())

        # generate needed keys
        minKey = 0.0
        maxKey = availableKeys[-1]
        step = 1.0 / float(self.numSamples)
        neededKeys = []

        for t in self.kahan_range(minKey, maxKey, step):
            neededKeys.append(t)

        neededKeys.append(maxKey)

        outDict = {}
        if len(availableKeys) < 2:
            return outDict

        for idx in xrange(len(availableKeys)):
            # if looped
            idxNext = (idx + 1) % len(availableKeys)
            # else
            # idxNext = math.min(idx + 1, len(availableKeys))

            tStart = availableKeys[idx]
            tEnd = availableKeys[idxNext]

            aStart = angleDict[tStart]
            aEnd = self.closest_angle(aStart, angleDict[tEnd])
            # update, for the dict to be "smooth", this is kinda hacky and should be changed probably
            angleDict[tEnd] = aEnd

            slope = (aEnd - aStart) / (tEnd - tStart)
            offset = aEnd - slope * tEnd

            for time in neededKeys:
                if time < tStart or time >= tEnd:
                    continue

                angleVal = slope * time + offset
                outDict[time] = angleVal

        return outDict


    def closest_angle(self, a1, a2):
        # this checks what is the distance between angles
        normalDiff = math.fabs(a2 - a1)

        a2T1 = a2 + 2.0 * math.pi
        a2T2 = a2 - 2.0 * math.pi

        newDiff1 = math.fabs(a2T1 - a1)
        newDiff2 = math.fabs(a2T2 - a1)

        if normalDiff < newDiff1 and normalDiff < newDiff2:
            return a2
        elif newDiff1 < newDiff2:
            return a2T1
        return a2T2

    def kahan_range(self, start, stop, step):
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

    def fix_holes(self, inDict):
        # what does it do:
        # it finds None values as 1st and 2nd element and interpolates them
        # it's an error if such values appear at the start of the dict
        # !!! whenever it'll be fixed i should start again by redoing most
        # !!! of this ugly code into something more manageable
        timeKeys = sorted(inDict.keys())

        startTimeIdx = 0
        seekingEnd = False

        # this is terrible and hacky...
        assert(inDict[timeKeys[0]] is not None)

        for timeIdx in xrange(1, len(timeKeys)):
            currVal = inDict[timeKeys[timeIdx]]

            if seekingEnd:
                if currVal is not None:
                # yupi!
                #                    print 'Found end of this path at idx:', timeIdx, timeKeys[timeIdx]
                    seekingEnd = False
                    self.fix_dict_holes(inDict, startTimeIdx, timeIdx)
            else:
                if currVal is None:
                #                    print 'Found start of this path at idx:', startTimeIdx, timeKeys[startTimeIdx]
                    seekingEnd = True
                else:
                    startTimeIdx = timeIdx

        if seekingEnd:
            baseVal = inDict[timeKeys[startTimeIdx]]
            for idx in xrange(startTimeIdx, len(timeKeys)):
                inDict[timeKeys[idx]] = baseVal

    def fix_dict_holes(self, inDict, startIdx, endIdx):
    #        print '  Fixing from', startIdx, endIdx
        timeKeys = sorted(inDict.keys())

        startTime = timeKeys[startIdx]
        endTime = timeKeys[endIdx]
        timeDiff = endTime - startTime

        startVal = inDict[startTime]
        endVal = self.closest_angle(startVal, inDict[endTime])
        inDict[endTime] = endVal

        # linear interpolation
        slope = (endVal - startVal) / timeDiff
        offset = endVal - slope * endTime

        for idx in xrange(startIdx + 1, endIdx):
        #            print '    Working on idx', idx
            timeVal = timeKeys[idx]

            newAngle = slope * timeVal + offset

            inDict[timeVal] = newAngle
