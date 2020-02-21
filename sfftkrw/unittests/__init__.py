# -*- coding: utf-8 -*-
import json
import os
import random
import sys
from unittest import TestCase

from .. import BASE_DIR
from ..core import _xrange, _print, _FileNotFoundError

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-15'
__updated__ = '2018-02-14'

# path to test data
TEST_DATA_PATH = os.path.join(BASE_DIR, 'test_data')


# helper functions
def _random_integer(start=1, stop=1000):
    try:
        assert stop > start
    except AssertionError:
        raise ValueError("`stop` should be greater than `start`")
    return random.randint(start, stop)


def _random_float(multiplier=1):
    try:
        assert multiplier != 0
    except AssertionError:
        raise ValueError("`multiplier` should never be 0")
    return random.random() * multiplier


def _random_integers(count=10, start=1, stop=1000, as_string=False, sep=' '):
    try:
        assert stop > start
    except AssertionError:
        raise ValueError("`stop` should be greater than `start`")
    try:
        assert count > 0
    except AssertionError:
        raise ValueError("`count` should be greater than 0")
    if as_string:
        return sep.join(map(str, [_random_integer(start=start, stop=stop) for _ in _xrange(count)]))
    else:
        return [_random_integer(start=start, stop=stop) for _ in _xrange(count)]


def _random_floats(count=10, multiplier=1):
    try:
        assert multiplier != 0
    except AssertionError:
        raise ValueError("`multiplier` should never be 0")
    try:
        assert count > 0
    except AssertionError:
        raise ValueError("`count` should be greater than 0")
    return [_random_float(multiplier=multiplier) for _ in _xrange(count)]


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Py23Fix(object):
    def __init__(self, *args, **kwargs):
        if sys.version_info[0] > 2:
            pass
        else:
            # new names for assert methods
            self.assertCountEqual = self.assertItemsEqual
            self.assertRegex = self.assertRegexpMatches
            self.assertRaisesRegex = self.assertRaisesRegexp
        super(Py23Fix, self).__init__(*args, **kwargs)


class Py23FixTestCase(Py23Fix, TestCase):
    """Mixin to fix method changes in TestCase class"""

    @classmethod
    def setUpClass(cls):
        cls.test_hdf5_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'test.hdf5')

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.test_hdf5_fn)
        except _FileNotFoundError:
            pass

    @staticmethod
    def stderr(*args, **kwargs):
        _print(*args, **kwargs)

    @staticmethod
    def stderrj(*args, **kwargs):
        _print(json.dumps(*args, indent=2, **kwargs))

    @staticmethod
    def stderrh(group):
        def _print_keys(group, indent=0):
            if hasattr(group, 'keys'):
                for key in group.keys():
                    try:
                        _print('{indent}{key} => {value}'.format(
                            indent='\t' * indent,
                            key=key,
                            value=group[key][()]
                        ))
                    except AttributeError:
                        _print('{indent}{key} => {value}'.format(
                            indent='\t' * indent,
                            key=key,
                            value=group[key].name
                        ))
                    if hasattr(group[key], 'keys'):
                        if group[key].keys():
                            indent += 1
                            _print_keys(group[key], indent=indent)
                        indent -= 1
            else:
                _print(group)

        _print_keys(group)
