# -*- coding: utf-8 -*-
# base.py
from __future__ import division, print_function

import importlib
import inspect
import io
import json
import numbers
import os
import re

import h5py

from .. import VALID_EXTENSIONS, EMDB_SFF_VERSION
from ..core import _dict, _str, _encode, _decode, _bytes, _clear, _basestring, _getattr_static
from ..core.print_tools import print_date

# from ..schema import emdb_sff as sff

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
sff = importlib.import_module(emdb_sff_name)

_match_var_stop = re.compile(r"(?P<var>\w+)\[\:(?P<stop>\d*)\]")


class SFFTypeError(Exception):
    """Raised whenever incorrect types are used"""

    def __init__(self, instance, klass, message=None):
        self.instance = instance
        self.klass = klass
        self.message = message

    def __str__(self):
        if self.message is None:
            return repr(u"'{}' is not object of type {}".format(self.instance, self.klass))
        else:
            return repr(u"'{}' is not object of type {}: {}".format(self.instance, self.klass, self.message))


class SFFValueError(Exception):
    """Raised whenever invalid/missing values are found"""


# fixme: correct documentation
class SFFType(object):
    """Base class for all EMDB-SFF adapter classes

    This class reads and configures any subclass using the subclass's definition.

    Subclasses of :py:class:`SFFType` should define class attributes from the following list depending on whether
    the subclass defines a container or not. Containers typically have *List* in the class name signifying that they
    are a *list* of objects of some type. For example, the :py:class:`SFFSegmentList` objects are a *list of*
    :py:class:`SFFSegment` objects.
    """
    gds_type = None
    u"""The ``generateDS`` class adapted by this `SFFType` subclass"""
    gds_tag_name = None
    u"""The literal tag name in XML output. Should only changed in cases where several types are an extension of
        a single type in which case all types appear in the XML with the name of their parent. Most classes
        will not need this set."""
    repr_string = ""
    u"""A *string representation* for objects of the subclass that can be formatted. This string will be produced
        for calls to the :py:func:`print` function. Formatting is accomplished by included empty format delimiters
        (``{}``) which will be populated with values from the :py:attr:`repr_args` specified below otherwise
        literal braces will be displayed.
    """
    repr_args = ()
    u"""The *arguments of the string representation*, if any.
    
    A tuple of strings each of which is an attribute that can be 
    referenced for a value to put into the `repr_string`
    
    For example to have the representational string "SFFSegment(id=33)"
    we set `repr_string="SFFSegment(id={})` and `repr_args=('id', )`
    
    Some special `repr_args` values are:
    
    -   ``len()`` fills the ``{}`` with the length;
    -   ``list()`` fills the ``{}`` with a list of contained objects.
    -   ``data[:100]`` applied to the :py:class:`sfftkrw.SFFLattice` class where only the first 100 bytes are displayed
    """
    eq_attrs = list()
    u"""A list of attributes used to test equality"""

    def __new__(cls, new_obj=True, *args, **kwargs):
        """Matching constructor signature for subclasses"""
        return super(SFFType, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        if self.gds_type:
            # restructure kwargs of type SFF* to their gds_type equivalents
            _kwargs = _dict()
            # remove `new_obj` from kwargs
            if u'new_obj' in kwargs:
                del kwargs[u'new_obj']
            for k in kwargs:
                if isinstance(kwargs[k], SFFType):
                    _kwargs[k] = kwargs[k]._local
                else:
                    _kwargs[k] = kwargs[k]
            self._local = self.gds_type(*args, **_kwargs)
            # ensure that the version is copied without requiring user intervention
            if isinstance(self._local, sff.segmentation):
                self.version = self._local.schema_version
        else:
            raise ValueError(u"attribute 'gds_type' cannot be 'None'")
        # if we have a name for the XML output tag we set it here
        self._local.original_tagname_ = self.gds_tag_name

    @classmethod
    def from_gds_type(cls, inst=None):
        """Create an :py:class:`.SFFType` subclass directly from a `gds_type` object

        Notice that we ignore do not pass `*args, **kwargs` as we assume the `inst` is complete.
        """
        if isinstance(inst, cls.gds_type):
            obj = cls(new_obj=False)
            obj._local = inst
        elif inst is None:
            obj = None
        else:
            raise SFFTypeError(inst, cls.gds_type)
        return obj

    def __str__(self):
        return repr(self)

    def __repr__(self):
        """Return a representation of the object

        In most cases can be used to instantiate the object.
        """
        if self.repr_string:
            if self.repr_args:
                assert isinstance(self.repr_args, tuple)
                if len(self.repr_args) == self.repr_string.count(u'{}'):
                    _repr_args = list()
                    for arg in self.repr_args:
                        if arg == u'len()':
                            _repr_args.append(len(self))
                        elif arg == u'list()':
                            _repr_args.append(list(self))
                        elif _match_var_stop.match(arg):
                            mo = _match_var_stop.match(arg)
                            var = mo.group('var')
                            stop = int(mo.group('stop'))
                            sub_str = getattr(self, var)
                            if sub_str:  # there is something
                                if len(sub_str) < stop:
                                    _repr_args.append(sub_str)
                                else:
                                    if isinstance(sub_str, _bytes):
                                        _repr_args.append(sub_str[:stop] + b"...")
                                    elif isinstance(sub_str, _str):
                                        _repr_args.append(sub_str[:stop] + u"...")
                            else:
                                _repr_args.append(sub_str)
                        else:
                            _repr_args.append(getattr(self, arg, None))
                    # quote strings
                    repr_args = list()
                    for r in _repr_args:
                        if isinstance(r, _str):  # or isinstance(r, _bytes):
                            repr_args.append(u"\"{}\"".format(r))
                        elif isinstance(r, _bytes):
                            repr_args.append(u"\"{}\"".format(_decode(r, u'utf-8')))
                        else:
                            repr_args.append(r)
                    # repr_args = list(map(lambda r: "\"{}\"".format(r) if isinstance(r, _str) else r, _repr_args))
                    return self.repr_string.format(*repr_args)
                else:
                    raise ValueError(u"Unmatched number of '{}' and args in repr_args")
            else:
                return self.repr_string
        else:
            return _str(type(self))

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        if self.eq_attrs:
            return all(list(map(lambda a: getattr(self, a) == getattr(other, a), self.eq_attrs)))
        return False

    def export(self, fn, args=None, *_args, **_kwargs):
        """Export to a file on disc

        :param fn: filename to export to; the output format is determined by the extension:
        :type fn: str or io.TextIOWrapper or io.RawIOBase or io.BufferedIOBase or file
        :return int status: exit code from :py:mod:`os` library

        - ``.sff`` - XML
        - ``.hff`` - HDF5
        - ``.json`` - JSON
        """
        if self._is_valid():
            if isinstance(fn, _basestring):
                fn_ext = fn.split('.')[-1].lower()
                try:
                    assert fn_ext in VALID_EXTENSIONS
                except AssertionError:
                    print_date(_encode(u"Invalid filename: extension should be one of {}: {}".format(
                        ", ".join(VALID_EXTENSIONS),
                        fn,
                    ), u'utf-8'))
                    return os.EX_DATAERR
                if re.match(r"^(sff|xml)$", fn_ext, re.IGNORECASE):
                    with open(fn, u'w') as f:
                        # write version and encoding
                        version = _kwargs.get(u'version') if u'version' in _kwargs else u"1.0"
                        encoding = _kwargs.get(u'encoding') if u'encoding' in _kwargs else u"UTF-8"
                        f.write(u'<?xml version="{}" encoding="{}"?>\n'.format(version, encoding))
                        # always export from the root
                        self._local.export(f, 0, *_args, **_kwargs)
                elif re.match(r"^(hff|h5|hdf5)$", fn_ext, re.IGNORECASE):
                    with h5py.File(fn, u'w') as f:
                        self.as_hff(f, args=args)
                elif re.match(r"^json$", fn_ext, re.IGNORECASE):
                    with open(fn, u'w') as f:
                        if self.version == u'0.7.0.dev0':
                            self.as_json(f, args=args, *_args, **_kwargs)
                        elif self.version == u'0.8.0.dev1':
                            data = self.as_json(args=args)
                            try:
                                json_sort = args.json_sort
                                json_indent = args.json_indent
                            except AttributeError:
                                json_sort = False
                                json_indent = 2
                            json.dump(data, f, sort_keys=json_sort, indent=json_indent)
                        # self.as_json(f, *_args, **_kwargs)
            elif issubclass(type(fn), io.IOBase):
                self._local.export(fn, 0, *_args, **_kwargs)
            return os.EX_OK
        else:
            raise SFFValueError("export failed due to validation error")

    def as_json(self, args=None):
        """For all contained classes this method returns a dictionary which will be serialised into JSON. Only at the
        top level (SFFSegmentation) will the final serialisation be done.

        :param args: command line arguments
        :type args: :py:class:`argparse.Namespace`
        :return: a set of nested dictionaries
        :rtype: dict
        """
        raise NotImplementedError

    @classmethod
    def from_json(cls, data, args=None):
        """Deserialise the given json object into an EMDB-SFF object

        :param dict data: the data to be converted into `SFF*` objects
        :param args: command line arguments
        :type args: :py:class:`argparse.Namespace`
        :return: the corresponding `SFF*` object
        :rtype: :py:class:`.base.SFFType` subclass
        """
        raise NotImplementedError

    def as_hff(self, parent_group, name=None, args=None):
        """Returns the current object as a group in an HDF5 file with the given name

        For instances which are subclasses of :py:class:`.base.SFFIndexType` `name` will be
        a string version of the index (`id`). If `id` is `None` then we will generate a
        unique one so as to write the object to file. Therefore, the process of writing to
        HDF5 could end up looking slightly different from the original if the original
        had missing indexes for some objects.

        :param parent_group: an HDF5 Group that will contain the objects in this object
        :type parent_group: :py:class:`Group`
        :param args: command line arguments
        :type args: :py:class:`argparse.Namespace`
        :param name: the name to be given to this object in the object hierarchy (default: None)
        :type name: str or None
        :return: the populated parent group
        :rtype: :py:class:`Group`
        """
        raise NotImplementedError

    @classmethod
    def from_hff(cls, parent_group, name=None, args=None):
        """Convert HDF5 objects into EMDB-SFF objects
        It should either return a valid object or raise an :py:class:`SFFValueError` due to failed validation

        :param parent_group: an HDF5 Group that will contain the objects in this object
        :type parent_group: :py:class:`Group`
        :param args: command line arguments
        :type args: :py:class:`argparse.Namespace`
        :param name: the name to be given to this object in the object hierarchy (default: None)
        :type name: str or None
        :return: the corresponding `SFF*` object
        :rtype: :py:class:`.base.SFFType` subclass
        """
        raise NotImplementedError

    def _is_valid(self):
        """On output ensure that all required attributes have a valid value"""
        invalid_attrs = list()
        for attr_name, attr_value in inspect.getmembers(self):
            # don't even consider dunders
            if attr_name.startswith('__'):
                continue
            # getattr_static prevents dynamic lookup;
            # see https://docs.python.org/3.7/library/inspect.html#fetching-attributes-statically
            attr_obj = _getattr_static(self, attr_name)
            if isinstance(attr_obj, SFFAttribute):  # we're only interested in data descriptors
                value = getattr(self, attr_name)
                if attr_obj._required and value is None:
                    invalid_attrs.append(attr_name)
        if invalid_attrs:
            print_date("{} is missing the following required attributes: {}".format(self, ', '.join(invalid_attrs)))
            return False
        else:
            return True


class SFFIndexType(SFFType):
    """Subclass to handle objects with indexes (IDs)"""
    index_attr = ""
    u"""the name of the attribute on the class which will be treated as the ID"""
    increment_by = 1
    u"""by default we increment by 1"""
    start_at = 0
    u"""used when resetting `index_attr` attribute"""
    index_in_super = False
    u"""when an index is applied to a set of subclasses we set `index_in_super` to True"""

    @staticmethod
    def update_index(cls, obj, current, **kwargs):
        """Set the index value in `obj` and return the next value

        :param cls: the class of obj
        :param int current: the current value of the index
        :param obj: the instance
        :param kwargs: keyword arguments
        :return next: the next value of the index
        :rtype nex: int
        """
        # set the index on the instance
        setattr(obj, cls.index_attr, current)
        # update the index
        if u'id' in kwargs:
            next = kwargs[u'id'] + cls.increment_by
        elif u'vID' in kwargs:
            next = kwargs[u'vID'] + cls.increment_by
        elif u'PID' in kwargs:
            next = kwargs[u'PID'] + cls.increment_by
        else:
            next = current + cls.increment_by
        return next

    def __new__(cls, new_obj=True, *args, **kwargs):
        # make sure we have a non-blank `index_attr` in the class
        try:
            assert cls.index_attr
        except AssertionError:
            raise SFFTypeError(cls.index_attr, str, u'subclasses must provide an index attribute')
        # make sure there is an attribute with the value of the `index_attr` string
        try:
            assert hasattr(cls, cls.index_attr)
        except AssertionError:
            raise AttributeError(u"'{}' is missing a class variable '{}'".format(cls, cls.index_attr))
        # make sure the `index_attr` attribute is set to an integer
        try:
            _index_attr = getattr(cls, cls.index_attr)
            assert isinstance(_index_attr, numbers.Integral)
        except AssertionError:
            raise SFFTypeError(cls.index_attr, numbers.Integral)
        # create the instance
        # todo: add new_obj=new_obj for call to super
        obj = super(SFFIndexType, cls).__new__(cls)
        if new_obj:
            # current index
            current = getattr(cls, cls.index_attr)
            # if the index is in the superclass
            if obj.index_in_super:
                try:
                    assert hasattr(cls, u'update_counter')
                except AssertionError:
                    raise AttributeError(u"{} superclass does not have an 'update_counter' classmethod".format(cls))
                next = SFFIndexType.update_index(cls, obj, current, **kwargs)
                # update the index attr
                cls.update_counter(next)
            else:
                next = SFFIndexType.update_index(cls, obj, current, **kwargs)
                # update the index attr
                setattr(cls, cls.index_attr, next)
        return obj

    def __init__(self, *args, **kwargs):
        # we don't want the `new_obj` kwarg to propagate so we terminate it here
        if u'new_obj' in kwargs:
            # only set the `index_attr` to None if `new_obj=False`
            if not kwargs[u'new_obj']:
                setattr(self, self.index_attr, None)
        super(SFFIndexType, self).__init__(*args, **kwargs)
        # fixme: adds `vID` and `PID` to segments ?! (harmless bug)
        # id
        if u'id' in kwargs:
            self._local.id = kwargs[u'id']
        else:
            self._local.id = getattr(self, self.index_attr)
        # vID: vertices
        if u'vID' in kwargs:
            self._local.vID = kwargs[u'vID']
        else:
            self._local.vID = getattr(self, self.index_attr)
        # PID: polygons
        if u'PID' in kwargs:
            self._local.PID = kwargs[u'PID']
        else:
            self._local.PID = getattr(self, self.index_attr)

    @classmethod
    def reset_id(cls):
        """Reset the `index_attr` attribute to its starting value"""
        setattr(cls, cls.index_attr, cls.start_at)

    @classmethod
    def from_gds_type(cls, inst=None):
        if isinstance(inst, cls.gds_type):
            obj = cls(new_obj=False)
            obj._local = inst
        elif inst is None:
            obj = inst
        else:
            raise SFFTypeError(inst, cls.gds_type)
        return obj


class SFFListType(SFFType):
    """Subclass to confer list-like behaviour"""
    iter_attr = None
    u"""the name of the attribute in the ``generateDS`` class that we iterate over together with 
    the `SFFType` subclass to cast each received object to
    
    The *iterable attribute* of the class. It refers to an attribute of the class pointed to by :py:attr:`gds_type` which is iterable.

    It should be a two-tuple having the name of the generateDS class and ``SFF*`` class to adapt it to.

    Only one attribute per class can be specified.

    For example, consider the following class definition for some fictional ``SFFTest`` class that adapts a class
    called ``test`` that was generated by generateDS.

    .. code:: python

        import emdb_sff

        class SFFTest(SFFType):
            gds_type = emdb_sff.test
            repr_str = "SFFTest object with {} SFFItem objects inside"
            repr_args = ("len()",)
            iter_attr = ('i', SFFItem)

            # attributes
            items = SFFAttribute('items', sff_type=SFFItem)

    In this sample:

    -   the generateDS API is located in the module called ``emdb_sff``;

    -   ``test`` is a class in the ``emdb_sff`` module;

    -   ``i`` is an iterable attribute of ``test``;

    -   ``i`` is adapted by the ``SFFItem`` class (which should have its :py:attr:`gds_type` set to the class for
        ``i``);

    Now consider this class in action:

    .. code:: python

        from sfftkrw.schema import SFFTest

        T = SFFTest()
        # ...
        # populate T with some valid data
        # ...
        # now we can iterate over the data
        for i in T: # because it has an iter_attr specified
            # i is an SFFItem object
            print(i)
            # prints 'SFFTest object with 37 SFFItem objects inside'

    In addition to being iterable, the iterable attribute enable the following operations on objects of the
    subclass:

    -   length i.e. len(obj);

        .. code:: python

            len(T)
            # 37

    -   indexing e.g. ``obj[<int>]``;

        .. code:: python

            T[15]

    
    """
    sibling_classes = []
    u"""a list of pairs of classes which are all subclasses of some convenience class
    
    For example: :py:class:`SFFShape` is the parent of :py:class:`SFFCone`, :py:class:`SFFCuboid`, 
    :py:class:`SFFCylinder` and :py:class:`SFFEllipsoid`. This is because the :py:class:`SFFShape` class manages a 
    continuous set of IDs for the different shapes. However, when we iterate over a `SFFShapePrimitiveList` 
    we can't get a generic shape; we need individual subclasses. Therefore, this class variable defines how
    we return individual subclass instances from a `SFFShapePrimitiveList`."""
    min_length = 0

    def __new__(cls, new_obj=True, *args, **kwargs):
        # make sure `iter_attr` is not empty
        try:
            assert cls.iter_attr
        except AssertionError:
            raise ValueError(u"attribute 'iter_attr' in {} cannot be empty".format(cls))
        # make sure `iter_attr` consists of a string and a class
        try:
            assert isinstance(cls.iter_attr[0], _str)
        except AssertionError:
            raise SFFTypeError(cls.iter_attr[0], _str)
        try:
            assert issubclass(cls.iter_attr[1], SFFType) or cls.iter_attr[1] == _str or cls.iter_attr[1] == int
        except AssertionError:
            raise SFFTypeError(cls.iter_attr[1], SFFType)
        # print(kwargs, file=sys.stderr)
        if new_obj:
            # reset ID only if `cls.iter_attr` is an `SFFType` subclass
            if issubclass(cls.iter_attr[1], SFFType):
                cls.iter_attr[1].reset_id()
        obj = super(SFFListType, cls).__new__(cls, new_obj=new_obj, *args, **kwargs)
        return obj

    def __init__(self, *args, **kwargs):
        self._id_dict = _dict()
        super(SFFListType, self).__init__(*args, **kwargs)

    def _is_valid(self):
        if len(self) < self.min_length:
            print_date("{} has fewer than min_length={} items: {}".format(self, self.min_length, len(self)))
            return False
        for item in self:
            if not item._is_valid():
                return False
        return True

    @classmethod
    def from_gds_type(cls, inst=None):
        if isinstance(inst, cls.gds_type):
            obj = cls(new_obj=False)
            obj._local = inst
            obj._update_dict()
        elif inst is None:
            obj = inst
        else:
            raise SFFTypeError(inst, cls.gds_type)
        return obj

    def _cast(self, instance):
        """Private method used in conjunction with `sibling_classes`.

        We iterate of the list of sibling-subclass pairs.

        The sibling is the one defined in generateDS while the
        subclass is the `SFFType` subclass.
        """
        for sibling, subclass in self.sibling_classes:
            if isinstance(instance, sibling):
                return subclass.from_gds_type(instance)
            # we must return else...
        else:
            raise SFFTypeError(instance, self.sibling_classes)

    def __iter__(self):
        """When we iterate over subclasses we want to recast back from generateDS types to
        adapter types.

        For values which remain as native Python types (strings and integers) we perform
        a simple type cast.
        """
        iter_name, iter_type = self.iter_attr
        if self.sibling_classes:  # if the contained objects are subclasses of some generic class
            return iter(list(map(self._cast, getattr(self._local, iter_name))))
        else:  # there is only one type of contained objects
            if issubclass(iter_type, SFFType):
                return iter(list(map(iter_type.from_gds_type, getattr(self._local, iter_name))))
            elif iter_type in [_str, int]:
                return iter(list(map(iter_type, getattr(self._local, iter_name))))

    def __len__(self):
        iter_name, _ = self.iter_attr
        return len(getattr(self._local, iter_name))

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        return all(list(map(lambda v: v[0] == v[1], zip(self, other))))

    def __getitem__(self, index):
        iter_name, iter_type = self.iter_attr
        if self.sibling_classes:
            item = getattr(self._local, iter_name)[index]
            return self._cast(item)
        else:
            if issubclass(iter_type, SFFType):
                return iter_type.from_gds_type(getattr(self._local, iter_name)[index])
            elif iter_type in [_str, int]:
                return iter_type(getattr(self._local, iter_name)[index])

    def __setitem__(self, index, value):
        iter_name, iter_type = self.iter_attr
        # get the container
        cont = getattr(self._local, iter_name)
        if iter_type not in [_str, int] and isinstance(value, iter_type):
            cont[index] = value._local
            self._add_to_dict(value.id, value)
        elif iter_type in [_str, int] and (isinstance(value, _str) or isinstance(value, int)):
            cont[index] = value
        else:
            raise SFFTypeError(value, iter_type, u"or int or str")

    def __delitem__(self, index):
        iter_name, _ = self.iter_attr
        # get the name of the iterable in _local (a list) then delete index pos from it
        cont = getattr(self._local, iter_name)
        sff_item = self[index]
        del cont[index]
        if hasattr(sff_item, u'id'):
            self._del_from_dict(sff_item.id)

    def append(self, item):
        """Append to the list"""
        iter_name, iter_type = self.iter_attr
        cont = getattr(self._local, iter_name)
        if iter_type not in [_str, int] and isinstance(item, iter_type):
            cont.append(item._local)
            self._add_to_dict(item.id, item)
        elif iter_type in [_str, int] and (isinstance(item, _str) or isinstance(item, int)):
            cont.append(item)
        else:
            raise SFFTypeError(item, SFFType)

    def clear(self):
        """Remove all items"""
        iter_name, _ = self.iter_attr
        cont = getattr(self._local, iter_name)
        _clear(cont)
        self._id_dict.clear()

    def copy(self):
        """Create a shallow copy"""
        iter_name, _ = self.iter_attr
        copy = type(self)()  # create a new instance of the class
        # assign _local to a copy of self
        setattr(copy._local, iter_name, getattr(self._local, iter_name)[:])
        copy._id_dict = self._id_dict
        return copy

    def extend(self, other):
        """Extend this list using this and other"""
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            raise SFFTypeError(other, type(self))
        iter_name, _ = self.iter_attr
        cont = getattr(self._local, iter_name)
        cont_other = getattr(other._local, iter_name)
        cont.extend(cont_other)
        self._id_dict.update(other._id_dict)

    def insert(self, index, item):
        """Insert into the list at the given index"""
        iter_name, iter_type = self.iter_attr
        cont = getattr(self._local, iter_name)
        if iter_type not in [_str, int] and isinstance(item, iter_type):
            cont.insert(index, item._local)
            self._add_to_dict(item.id, item)
        elif iter_type in [_str, int] and (isinstance(item, _str) or isinstance(item, int)):
            cont.insert(index, item)
        else:
            raise SFFTypeError(item, SFFType, u"or int or str")

    def pop(self, index=-1):
        """Remove and return the indexed (default: last) item"""
        iter_name, iter_type = self.iter_attr
        cont = getattr(self._local, iter_name)
        popped = cont.pop(index)
        if self.sibling_classes:
            sff_popped = self._cast(popped)
            self._del_from_dict(sff_popped.id)
            return sff_popped
        else:
            if issubclass(iter_type, SFFType):
                sff_popped = iter_type.from_gds_type(popped)
                self._del_from_dict(sff_popped.id)
                return sff_popped
            elif iter_type in [_str, int]:
                return iter_type(popped)

    def remove(self, item):
        """Removes the first occurrence of item"""
        iter_name, iter_type = self.iter_attr
        cont = getattr(self._local, iter_name)
        if iter_type not in [_str, int] and isinstance(item, iter_type):
            cont.remove(item._local)
        elif iter_type in [_str, int] and (isinstance(item, _str) or isinstance(item, int)):
            cont.remove(item)
        else:
            raise SFFTypeError(item, SFFType, u"or int or str")

    def reverse(self):
        """Reverses the items in place"""
        iter_name, _ = self.iter_attr
        getattr(self._local, iter_name).reverse()

    def get_ids(self):
        """Return a list of IDs of the contained objects

        Should only work if the contained objects have IDs i.e. it should not work
        for `SFFComplexes` and `SFFMacromolecules`
        """
        return self._id_dict.keys()

    def _add_to_dict(self, k, v):
        """Private method that adds to the convenience dictionary"""
        if k in self._id_dict:
            raise KeyError(u"item with ID={} already present".format(k))
        elif k is not None:
            self._id_dict[k] = v

    def _del_from_dict(self, k):
        """Private method that removes from the convenience dictionary"""
        del self._id_dict[k]

    def _update_dict(self):
        iter_name, iter_type = self.iter_attr
        if iter_type not in [_str, int] and issubclass(iter_type, SFFType):
            self._id_dict.update({i.id: i for i in self if i.id is not None})

    def get_by_id(self, id):
        """A convenience dictionary to retrieve contained objects by ID

        Items with no ID will not be found in the dictionary
        """
        return self._id_dict[id]


class SFFAttribute(object):
    """Descriptor for :py:class:`.SFFType` subclass attributes

    The adapter classes specify class attributes as accessors of values in the ``generateDS`` API. These are
    accomplished using this class to ``get``, ``set`` and ``delete`` values taking into account translation
    between the adapter and the ``generateDS`` API.

    This is done by referencing the ``obj._local`` variable which is the proxy for the underlying objects.

    Please see the :py:mod:`.api` module for how this is applied.

    :param name: which ``emdb_sff`` attribute to get the data from
    :type name: bytes or unicode
    :param sff_type: class of attribute (default: None - standard Python types like int, str, float)
    :type sff_type: `SFFType`
    :param bool required: whether or not this is a required (mandatory) attribute; default is `False`
    :param default: default value that this attribute takes; can be anything
    :param str help: help text associated with the attribute
    :type help: bytes or unicode
    """

    # todo: add kwarg 'required=False' and do validation check for required attributes
    def __init__(self, name, sff_type=None, required=False, default=None, help=""):
        """Initialiser for an attribute

        This class acts as an intermediary between ``SFFType`` and ``emdb_sff`` attributes. Each ``SFFType``
        defines a ``_local`` attribute (defined from the ``gds_type`` class attribute, which points to
        the ``emdb_sff`` object.

        :param name: which ``emdb_sff`` attribute to get the data from
        :type name: bytes or unicode
        :param sff_type: class of attribute (default: None - standard Python types like int, str, float)
        """
        self._name = name
        self.__doc__ = help
        self._sff_type = sff_type
        self._required = required
        self._default = default

    def __get__(self, obj, _):  # replaced objtype with _
        if self._sff_type:
            value = self._sff_type.from_gds_type(getattr(obj._local, self._name, self._default))
            # if the value is None and this is a SFFListType subclass return an empty subclass
            if issubclass(self._sff_type, SFFListType) and value is None:
                value = self._sff_type()
        else:
            value = getattr(obj._local, self._name, self._default)
        # if the value is None and we have a default return the default
        if self._default is not None and value is None:
            return self._default
        # otherwise return the value or None
        else:
            return value

    def __set__(self, obj, value):
        if self._sff_type:
            if isinstance(value, self._sff_type):
                setattr(obj._local, self._name, value._local)
            else:
                raise SFFTypeError(value, self._sff_type)
        else:
            # _print("value = '{}'".format(value))
            setattr(obj._local, self._name, value)

    def __delete__(self, obj):
        delattr(obj._local, self._name)


def _assert_or_raise(obj, klass, exception=SFFTypeError):
    try:
        assert isinstance(obj, klass)
    except AssertionError:
        raise exception(obj, klass)
