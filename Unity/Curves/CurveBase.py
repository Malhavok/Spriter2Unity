__author__ = 'Malhavok'

import bisect


class KVPoint(object):
    def __init__(self, key = None, value = None):
        self.__key = key
        self.__value = value

    def get_key(self):
        return self.__key

    def get_value(self):
        return self.__value

    def set_key(self, newKey):
        self.__key = newKey

    def set_value(self, newValue):
        self.__value = newValue


# optimized operation:
# 1st - adding all points
# then - getting all values
#
class CurveBase(object):
    def __init__(self):
        super(CurveBase, self).__init__()

        self.__sortedKeys = None
        self.__pointMap = {}


    def add_point(self, key, value):
        assert key is not None

        self.__pointMap[key] = KVPoint(key, value)
        self.__sortedKeys = None


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


    def __get_kv_point_at(self, key):
        if key in self.__pointMap:
            return self.__pointMap[key]

        if not self.__sortedKeys:
            self.__sortedKeys = sorted(self.__pointMap.keys())

        prevKey = self.__get_previous_key(key)
        nextKey = self.__get_next_key(key)

        prevKV = self.__pointMap[prevKey] if prevKey else None
        nextKV = self.__pointMap[nextKey] if nextKey else None

        return self._interpolate(prevKV, nextKV, key), prevKV, nextKV


    def __get_previous_key(self, key):
        assert self.__sortedKeys and len(self.__sortedKeys)

        idx = bisect.bisect_left(self.__sortedKeys, key) - 1
        return self.__sortedKeys[idx] if idx >= 0 else None


    def __get_next_key(self, key):
        assert self.__sortedKeys and len(self.__sortedKeys)

        idx = bisect.bisect_right(self.__sortedKeys, key)
        return self.__sortedKeys[idx] if idx < len(self.__sortedKeys) else None


    def _interpolate(self, kvPointPrev, kvPointNext, desiredKey):
        # this method should use values of kvPointPrev and kvPointNext (that might be None)
        # to interpolate value for desiredKey (which cannot be None)
        assert False and "This is to be overridden by children"


    def _calc_in_out_slopes(self, kvPointPrev, kvPointCurrent, kvPointNext):
        # this method should use values of given points (where kvPointPrev and kvPointNext can be None)
        # to calculate in and out slopes for given curve
        # returns 2 element tuple with [0] - in slope and [1] - out slope value
        assert False and "This is to be overridden by children"
