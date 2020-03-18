# -*- coding: utf-8 -*-
# utils.py
"""
utils.py
========

A collection of helpful utilities
"""
from __future__ import print_function, division

import json
import re

import h5py

from ..core import _decode

UNIQUE_ID = 1


def get_path(D, path):
    """Get a path from a dictionary

    :param dict D: a dictionary
    :param list path: an iterable of hashables
    :return: the item at the path from the dictionary
    """
    assert isinstance(D, dict)
    try:
        assert map(hash, path)
    except TypeError:
        raise TypeError(u'path should be an iterable of hashables')

    item = D
    for p in path:
        try:
            item = item[p]
        except KeyError:
            item = None
            break
    return item


def rgba_to_hex(rgba, channels=3):
    """Convert RGB(A) iterable to a hex string (e.g. #aabbcc(dd)

    :param rgba: an iterable with normalised (values in the closed interval ``[0-1]``) colour channel values
    :type rgba: list or tuple
    :param int channels: the number of channels (3 or 4); default 3
    :return: a hex string
    :rtype: str
    """
    try:
        assert channels in [3, 4]  # you can only return 3 or 4 channels
    except AssertionError:
        raise ValueError(u"keyword 'channels' can only be 3 or 4")
    min_channel_value = 0.0
    max_channel_value = 1.0
    if len(rgba) == 4:
        r, g, b, a = rgba
    elif len(rgba) == 3:
        r, g, b = rgba
        a = 1
    if r < min_channel_value or r > max_channel_value or \
            g < min_channel_value or g > max_channel_value or \
            b < min_channel_value or b > max_channel_value or \
            a < min_channel_value or a > max_channel_value:
        raise ValueError(
            u'values of rgba should be [{}-{}] (inclusive)'.format(
                min_channel_value,
                max_channel_value
            )
        )
    import math

    def dd_hex(val):
        _, hex_val = hex(int(math.floor(val * 255))).split(u'x')
        if len(hex_val) == 1:
            hex_val = u'0' + hex_val
        return hex_val

    if channels == 3:
        hex_colour = u'#' + dd_hex(r) + dd_hex(g) + dd_hex(b)
    elif channels == 4:
        hex_colour = u'#' + dd_hex(r) + dd_hex(g) + dd_hex(b) + dd_hex(a)
    return hex_colour


def get_version(fn):
    """
    Gets the version from the EMDB-SFF file

    :param fn: name of EMDB-SFF file
    :type fn: bytes or unicode
    :return: the version
    :rtype: unicode
    """
    if re.match(r".*\.(sff|xml)$", fn, re.IGNORECASE):
        from xml.etree import ElementTree as ET
        root = ET.parse(fn).getroot()
        version = root.findall('./version')[0].text
    elif re.match(r".*\.(hff|h5|hdf5)$", fn, re.IGNORECASE):
        with h5py.File(fn, 'r') as h:
            version = h[u'/version'][()]
    elif re.match(r".*\.json$", fn, re.IGNORECASE):
        with open(fn, 'r') as j:
            version = json.load(j)[u'version']
    else:
        raise ValueError(u"invalid filetype: {}".format(fn))
    return _decode(version, 'utf-8')


def get_unique_id():
    """Return an ID that will be unique over the current segmentation

    :return: unique_id
    :rtype: int
    """
    global UNIQUE_ID
    UNIQUE_ID = UNIQUE_ID + 1
    return UNIQUE_ID
