__author__ = 'Malhavok'

from CurveLinear import CurveLinear
from CurveBase import KVPoint

import math

# angles passed to this instance have to be in radians
#
class CurveLinearAngle(CurveLinear):
    def __init__(self):
        super(CurveLinearAngle, self).__init__()


    def add_point(self, key, value):
        addVal = self.__wrap_angle(value)
        super(CurveLinearAngle, self).add_point(key, addVal)


    def _interpolate(self, kvPointPrev, kvPointNext, desiredKey):
        if kvPointPrev is None:
            return kvPointNext

        if kvPointNext is None:
            return kvPointPrev

        startKey = kvPointPrev.get_key()
        endKey = kvPointNext.get_key()

        assert startKey < endKey
        assert desiredKey > startKey
        assert desiredKey < endKey

        percent = (desiredKey - startKey) / (endKey - startKey)
        angleDiff = self.__calc_angle_diff(kvPointPrev.get_value(), kvPointNext.get_value())
        value = self.__wrap_angle(kvPointPrev.get_value() + percent * angleDiff)

        return KVPoint(desiredKey, value)


    def __wrap_angle(self, angle):
        # whoa, best answer i ever saw
        # http://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        #
        # (cosA, sinA) is a point that represents difference in angles
        # and atan2 converts point coordinates into an angle!
        return math.atan2(math.sin(angle), math.cos(angle))


    def __calc_angle_diff(self, startAngle, targetAngle):
        angleDiff = targetAngle - startAngle
        return self.__wrap_angle(angleDiff)



## some basic tests

import unittest


class TestCurveLinearAngle(unittest.TestCase):
    def test_angle_pairs(self):
        pi2 = math.pi * 2.0

        testCases = [
            (1.0, 0.0, 2.0, pi2, 1.5, 0.0),
            (1.0, 0.0, 2.0, math.pi, 1.5, math.pi / 2.0),
            (1.0, 0.0, 2.0, -math.pi, 1.5, -math.pi / 2.0),
            (0.0, 0.0, 1.0, 4.0 * pi2, 1.5, 0.0),
            (0.0, 0.0, 1.0, 3.0 * math.pi / 2.0, 1.5, -math.pi / 2.0)
        ]

        for k1, a1, k2, a2, kRes, aRes in testCases:
            self.single_pair_test(k1, a1, k2, a2, kRes, aRes)


    def single_pair_test(self, k1, angle1, k2, angle2, kResult, angleResult):
        curve = CurveLinearAngle()

        curve.add_point(k1, angle1)
        curve.add_point(k2, angle2)

        outAngle = curve.get_point_at(kResult)
#        print k1, angle1, k2, angle2, kResult, angleResult, outAngle

        self.assertAlmostEqual(outAngle, angleResult, 5)



if __name__ == '__main__':
    unittest.main()
