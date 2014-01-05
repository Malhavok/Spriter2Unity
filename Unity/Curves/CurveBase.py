__author__ = 'Malhavok'

import bisect
import math


class KVPoint(object):
    def __init__(self, key, value, originalValue):
        self.__key = key
        self.__value = value
        self.__originalValue = originalValue


    def get_key(self):
        return self.__key


    def get_value(self):
        return self.__value


    def get_original_value(self):
        return self.__originalValue


    def set_key(self, newKey):
        assert newKey is not None
        self.__key = newKey


    def set_value(self, newValue):
        assert newValue is not None
        self.__value = newValue


    def set_original_value(self, newValue):
        assert newValue is not None
        self.__originalValue = newValue


    def __eq__(self, other):
        assert isinstance(other, self.__class__)

        if math.fabs(self.__key - other.__key) > 1e-4:
            return False
        if math.fabs(self.__value - other.__value) > 1e-4:
            return False
        if math.fabs(self.__originalValue - other.__originalValue) > 1e-4:
            return False
        return True


    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        return 'KVPoint(key=' + str(self.__key)\
               + '; value=' + str(self.__value)\
               + '; originalValue=' + str(self.__originalValue)\
               + ')'


# optimized operation:
# 1st - adding all points
# then - getting all values
#
class CurveBase(object):
    def __init__(self, valueModifierLambda = None):
        super(CurveBase, self).__init__()

        self.__lambdaModifier = valueModifierLambda
        if self.__lambdaModifier is None:
            self.__lambdaModifier = lambda x: x

        self.__sortedKeys = None
        self.__pointMap = {}


    def add_point(self, key, value):
        assert key is not None

        modValue = self._modify_kv_value(value)
        self.__pointMap[key] = KVPoint(key, modValue, value)
        self.__invalidate_sorted_keys()


    def get_point_at(self, key):
        assert key is not None
        # if key matches one known - return known value
        # otherwise - interpolate
        kvPointAtKey, _prevKV, _nextKV = self.__get_kv_point_at(key)
        return kvPointAtKey.get_value()


    def get_point_with_in_out_slopes(self, key):
        assert key is not None
        # returns 3 elements tuple with value, inSlope and outSlope
        kvPointAtKey, prevKV, nextKV = self.__get_kv_point_at(key)
        inSlope, outSlope = self._calc_in_out_slopes(prevKV, kvPointAtKey, nextKV)
        return kvPointAtKey.get_value(), inSlope, outSlope


    def get_all_keys(self):
        self.__generate_sorted_keys()
        return self.__sortedKeys


    def _modify_kv_value(self, value):
        # this is using defined function to modify value
        return self.__lambdaModifier(value)


    def __get_kv_point_at(self, key):
        self.__generate_sorted_keys()

        prevKey = self.__get_previous_key(key)
        nextKey = self.__get_next_key(key)

        prevKV = None
        nextKV = None

        if prevKey is not None:
            prevKV = self.__pointMap[prevKey]

        if nextKey is not None:
            nextKV = self.__pointMap[nextKey]

        if key in self.__pointMap:
            keyKV = self.__pointMap[key]
        else:
            keyKV = self._interpolate(prevKV, nextKV, key)

        assert keyKV is not None, str(self.__class__) + ': Failed to obtain value for ' + str(key) + ' with keymap of: ' + str(self.__sortedKeys)
        return keyKV, prevKV, nextKV


    def __get_previous_key(self, key):
        assert self.__sortedKeys is not None
        idx = bisect.bisect_left(self.__sortedKeys, key) - 1
        return self.__sortedKeys[idx] if idx >= 0 else None


    def __get_next_key(self, key):
        assert self.__sortedKeys is not None
        idx = bisect.bisect_right(self.__sortedKeys, key)
        return self.__sortedKeys[idx] if idx < len(self.__sortedKeys) else None


    def __generate_sorted_keys(self):
        if self.__sortedKeys:
            return
        self.__sortedKeys = sorted(self.__pointMap.keys())


    def __invalidate_sorted_keys(self):
        self.__sortedKeys = None


    def _interpolate(self, kvPointPrev, kvPointNext, desiredKey):
        # this method should use values of kvPointPrev and kvPointNext (that might be None)
        # to interpolate value for desiredKey (which cannot be None)
        assert False and "This is to be overridden by children"


    def _calc_in_out_slopes(self, kvPointPrev, kvPointCurrent, kvPointNext):
        # this method should use values of given points (where kvPointPrev and kvPointNext can be None)
        # to calculate in and out slopes for given curve
        # returns 2 element tuple with [0] - in slope and [1] - out slope value
        assert False and "This is to be overridden by children"
