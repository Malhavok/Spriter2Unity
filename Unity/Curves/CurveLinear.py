__author__ = 'Malhavok'

from CurveBase import CurveBase, KVPoint


# linear interpolation
#
class CurveLinear(CurveBase):
    def __init__(self):
        super(CurveLinear, self).__init__()


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
        value = kvPointPrev.get_value() * (1.0 - percent) + kvPointNext.get_value() * percent

        return KVPoint(desiredKey, value)


    def _calc_in_out_slopes(self, kvPointPrev, kvPointCurrent, kvPointNext):
        inSlope = 0.0
        outSlope = 0.0

        if kvPointPrev and kvPointPrev != kvPointCurrent:
            inSlope = self.__calc_slope(kvPointPrev, kvPointCurrent)

        if kvPointNext and kvPointNext != kvPointCurrent:
            outSlope = self.__calc_slope(kvPointCurrent, kvPointNext)

        return inSlope, outSlope


    def __calc_slope(self, point1, point2):
        assert point1.get_key() < point2.get_key()
        return (point2.get_value() - point1.get_value()) / (point2.get_key() - point1.get_key())




## some basic tests

import unittest


class TestCurveLinear(unittest.TestCase):
    testPoints = {1.0: 1.0, 2.0: 2.0}
    minPoint = 1.0
    maxPoint = 2.0

    def setUp(self):
        self.curveLinear = CurveLinear()

        for k in TestCurveLinear.testPoints.keys():
            self.curveLinear.add_point(k, TestCurveLinear.testPoints[k])


    def tearDown(self):
        self.curveLinear = None


    def test_point_prev(self):
        val, inSlope, outSlope = self.curveLinear.get_point_with_in_out_slopes(TestCurveLinear.minPoint - 1.0)
        self.assertAlmostEqual(val, TestCurveLinear.testPoints[TestCurveLinear.minPoint], 5)
        self.assertAlmostEqual(inSlope, 0.0, 5)
        self.assertAlmostEqual(outSlope, 0.0, 5)


    def test_point_post(self):
        val, inSlope, outSlope = self.curveLinear.get_point_with_in_out_slopes(TestCurveLinear.maxPoint + 1.0)
        self.assertAlmostEqual(val, TestCurveLinear.testPoints[TestCurveLinear.maxPoint], 5)
        self.assertAlmostEqual(inSlope, 0.0, 5)
        self.assertAlmostEqual(outSlope, 0.0, 5)


    def test_point_middle(self):
        midKey = (TestCurveLinear.maxPoint + TestCurveLinear.minPoint) / 2.0
        midVal = (TestCurveLinear.testPoints[TestCurveLinear.maxPoint] + TestCurveLinear.testPoints[TestCurveLinear.minPoint]) / 2.0
        slope = (TestCurveLinear.testPoints[TestCurveLinear.maxPoint] - TestCurveLinear.testPoints[TestCurveLinear.minPoint])\
                / (TestCurveLinear.maxPoint - TestCurveLinear.minPoint)

        val, inSlope, outSlope = self.curveLinear.get_point_with_in_out_slopes(midKey)
        self.assertAlmostEqual(val, midVal, 5)
        self.assertAlmostEqual(inSlope, slope, 5)
        self.assertAlmostEqual(outSlope, slope, 5)


    def test_point_exact(self):
        slope = (TestCurveLinear.testPoints[TestCurveLinear.maxPoint] - TestCurveLinear.testPoints[TestCurveLinear.minPoint])\
                / (TestCurveLinear.maxPoint - TestCurveLinear.minPoint)

        val1, inSlope1, outSlope1 = self.curveLinear.get_point_with_in_out_slopes(TestCurveLinear.minPoint)
        self.assertAlmostEqual(val1, TestCurveLinear.testPoints[TestCurveLinear.minPoint], 5)
        self.assertAlmostEqual(inSlope1, 0.0, 5)
        self.assertAlmostEqual(outSlope1, slope, 5)

        val2, inSlope2, outSlope2 = self.curveLinear.get_point_with_in_out_slopes(TestCurveLinear.maxPoint)
        self.assertAlmostEqual(val2, TestCurveLinear.testPoints[TestCurveLinear.maxPoint], 5)
        self.assertAlmostEqual(inSlope2, slope, 5)
        self.assertAlmostEqual(outSlope2, 0.0, 5)



if __name__ == '__main__':
    unittest.main()