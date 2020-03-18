# -*- coding: utf-8 -*-
"""

Convenience utilities

"""
from __future__ import print_function

import sys
from functools import partial

_print = partial(print, file=sys.stderr)

# redefinitions used globally
if sys.version_info[0] > 2:
    import builtins

    # xrange
    _xrange = builtins.range
    # dictionaries preserve order in Python3.7+
    if sys.version_info[1] >= 7:
        _dict = builtins.dict
        _classic_dict = builtins.dict
    else:
        from collections import OrderedDict

        _dict = OrderedDict
        _classic_dict = builtins.dict

    # iter* methods on dictionaries
    _dict_iter_keys = _dict.keys
    _dict_iter_values = _dict.values
    _dict_iter_items = _dict.items

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


    import inspect

    _getattr_static = inspect.getattr_static

    # exceptions
    _FileNotFoundError = FileNotFoundError
else:
    import __builtin__

    # xrange
    _xrange = __builtin__.xrange

    # for order preservation in dicts user OrderedDict
    from collections import OrderedDict

    _dict = OrderedDict
    _classic_dict = __builtin__.dict

    # iter* methods on dictionaries
    _dict_iter_keys = _dict.iterkeys
    _dict_iter_values = _dict.itervalues
    _dict_iter_items = _dict.iteritems

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


    # borrowed from Python 3.8's inspect.py
    # ------------------------------------------------ static version of getattr
    import types

    _sentinel = object()


    def _static_getmro(klass):
        return type.__dict__['__mro__'].__get__(klass)


    def _check_instance(obj, attr):
        instance_dict = {}
        try:
            instance_dict = object.__getattribute__(obj, "__dict__")
        except AttributeError:
            pass
        return dict.get(instance_dict, attr, _sentinel)


    def _check_class(klass, attr):
        for entry in _static_getmro(klass):
            if _shadowed_dict(type(entry)) is _sentinel:
                try:
                    return entry.__dict__[attr]
                except KeyError:
                    pass
        return _sentinel


    def _is_type(obj):
        try:
            _static_getmro(obj)
        except TypeError:
            return False
        return True


    def _shadowed_dict(klass):
        dict_attr = type.__dict__["__dict__"]
        for entry in _static_getmro(klass):
            try:
                class_dict = dict_attr.__get__(entry)["__dict__"]
            except KeyError:
                pass
            else:
                if not (type(class_dict) is types.GetSetDescriptorType and
                        class_dict.__name__ == "__dict__" and
                        class_dict.__objclass__ is entry):
                    return class_dict
        return _sentinel


    def getattr_static(obj, attr, default=_sentinel):
        """Retrieve attributes without triggering dynamic lookup via the
           descriptor protocol,  __getattr__ or __getattribute__.
           Note: this function may not be able to retrieve all attributes
           that getattr can fetch (like dynamically created attributes)
           and may find attributes that getattr can't (like descriptors
           that raise AttributeError). It can also return descriptor objects
           instead of instance members in some cases. See the
           documentation for details.
        """
        instance_result = _sentinel
        if not _is_type(obj):
            klass = type(obj)
            dict_attr = _shadowed_dict(klass)
            if (dict_attr is _sentinel or
                    type(dict_attr) is types.MemberDescriptorType):
                instance_result = _check_instance(obj, attr)
        else:
            klass = obj

        klass_result = _check_class(klass, attr)

        if instance_result is not _sentinel and klass_result is not _sentinel:
            if (_check_class(type(klass_result), '__get__') is not _sentinel and
                    _check_class(type(klass_result), '__set__') is not _sentinel):
                return klass_result

        if instance_result is not _sentinel:
            return instance_result
        if klass_result is not _sentinel:
            return klass_result

        if obj is klass:
            # for types we check the metaclass too
            for entry in _static_getmro(type(klass)):
                if _shadowed_dict(type(entry)) is _sentinel:
                    try:
                        return entry.__dict__[attr]
                    except KeyError:
                        pass
        if default is not _sentinel:
            return default
        raise AttributeError(attr)


    _getattr_static = getattr_static

    # exceptions
    _FileNotFoundError = OSError
