__author__ = 'Malhavok'


from CurveBase import CurveBase, KVPoint

# always returns the same, dummy, value
#
class CurveDummy(CurveBase):
    def __init__(self, dummyValue):
        super(CurveDummy, self).__init__()

        self.dummyValue = dummyValue


    def _interpolate(self, _kvPointPrev, _kvPointNext, desiredKey):
        return KVPoint(desiredKey, self.dummyValue)


    def _calc_in_out_slopes(self, _kvPointPrev, _kvPointCurrent, _kvPointNext):
        return 0.0, 0.0



## some basic tests


import unittest

class TestCurveDummy(unittest.TestCase):
    def test_dummy_test(self):
        dummyVal = 42.0
        dummy = CurveDummy(dummyVal)

        self.assertAlmostEqual(dummy.get_point_at(0.0), dummyVal, 5)
        self.assertAlmostEqual(dummy.get_point_at(-1.0), dummyVal, 5)
        self.assertAlmostEqual(dummy.get_point_at(50.0), dummyVal, 5)
        self.assertAlmostEqual(dummy.get_point_at('lol, this should work too'), dummyVal, 5)



if __name__ == '__main__':
    unittest.main()