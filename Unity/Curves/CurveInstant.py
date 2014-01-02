__author__ = 'Malhavok'

from CurveBase import CurveBase

# this shows instant change
#
class CurveInstant(CurveBase):
    def __init__(self):
        super(CurveInstant, self).__init__()


    def _interpolate(self, kvPointPrev, kvPointNext, _desiredKey):
        return kvPointPrev if kvPointPrev else kvPointNext


    def _calc_in_out_slopes(self, _kvPointPrev, _kvPointCurrent, _kvPointNext):
        return 'Infinity', 'Infinity'



## some basic tests

import unittest

class TestCurveInstant(unittest.TestCase):
    testPoints = {1.1: 15.0, 3.4: 3.0}
    minPoint = 1.1
    maxPoint = 3.4

    def setUp(self):
        self.curveInstant = CurveInstant()

        for k in TestCurveInstant.testPoints:
            self.curveInstant.add_point(k, TestCurveInstant.testPoints[k])


    def tearDown(self):
        self.curveInstant = None


    def test_point_prev(self):
        preVal = self.curveInstant.get_point_at(TestCurveInstant.minPoint - 1.0)
        self.assertAlmostEqual(preVal, TestCurveInstant.testPoints[TestCurveInstant.minPoint], 5)


    def test_point_post(self):
        postVal = self.curveInstant.get_point_at(TestCurveInstant.maxPoint + 1.0)
        self.assertAlmostEqual(postVal, TestCurveInstant.testPoints[TestCurveInstant.maxPoint], 5)


    def test_point_middle(self):
        midKey = (TestCurveInstant.maxPoint + TestCurveInstant.minPoint) / 2.0
        midVal = self.curveInstant.get_point_at(midKey)
        self.assertAlmostEqual(midVal, TestCurveInstant.testPoints[TestCurveInstant.minPoint], 5)


    def test_basic_slopes(self):
        _val, inSlope, outSlope = self.curveInstant.get_point_with_in_out_slopes(5)
        self.assertEqual(inSlope, 'Infinity')
        self.assertEqual(outSlope, 'Infinity')



if __name__ == '__main__':
    unittest.main()
