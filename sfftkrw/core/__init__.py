# -*- coding: utf-8 -*-
"""

Convenience utilities

"""
import sys

# redefinitions used globally
if sys.version_info[0] > 2:
    import builtins

    # xrange
    _xrange = builtins.range
    # iter* methods on dictionaries
    _dict_iter_keys = builtins.dict.keys
    _dict_iter_values = builtins.dict.values
    _dict_iter_items = builtins.dict.items
    # dictionaries preserve order in Python3
    if sys.version_info[1] >= 7:
        _dict = builtins.dict
    else:
        from collections import OrderedDict

        _dict = OrderedDict
    # UserList
    from collections import UserList

    _UserList = UserList
    # pseudo unicode function (does not exist in Python3)
    _bytes = builtins.bytes
    _str = builtins.str


    def _unicode(data):
        return data


    # urlencode
    from urllib.parse import urlencode

    _urlencode = urlencode
    # string base is str
    _basestring = (builtins.bytes, builtins.str)


    # decode is meaningless for str in Python3
    def _decode(data, encoding):
        if isinstance(data, builtins.str):
            return data
        elif isinstance(data, builtins.bytes):
            return data.decode(encoding)
        return data


    # encoding
    def _encode(data, encoding):
        if isinstance(data, builtins.str):
            return data.encode(encoding)
        elif isinstance(data, builtins.bytes):
            return data
        return data


    # input
    _input = builtins.input

    # file
    import io

    _file = io.IOBase

    # clear list
    def _clear(_list):
        _list.clear()
else:
    import __builtin__

    # xrange
    _xrange = __builtin__.xrange

    # iter* methods on dictionaries
    _dict_iter_keys = __builtin__.dict.iterkeys
    _dict_iter_values = __builtin__.dict.itervalues
    _dict_iter_items = __builtin__.dict.iteritems

    # for order preservation in dicts user OrderedDict
    from collections import OrderedDict

    _dict = OrderedDict

    from UserList import UserList

    _UserList = UserList
    # unicode
    _bytes = __builtin__.str
    _str = __builtin__.unicode


    def _unicode(data):
        return __builtin__.unicode(data)


    # urlencode
    from urllib import urlencode

    _urlencode = urlencode
    # string base is basestring
    _basestring = __builtin__.basestring


    # decode Python2 str object
    def _decode(data, encoding):
        if isinstance(data, __builtin__.str):
            return data.decode(encoding)
        elif isinstance(data, __builtin__.unicode):
            return data
        return data


    # encoding
    def _encode(data, encoding):
        if isinstance(data, __builtin__.str):
            return data
        elif isinstance(data, __builtin__.unicode):
            return data.encode(encoding)
        return data


    # input
    _input = __builtin__.raw_input

    # file
    _file = __builtin__.file

    # clear list
    def _clear(_list):
        del _list[:]
