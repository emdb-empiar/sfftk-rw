# -*- coding: utf-8 -*-
from __future__ import print_function

import importlib
import os
import random

import h5py

from . import TEST_DATA_PATH, Py23FixTestCase
from .. import EMDB_SFF_VERSION
from ..schema import base

adapter_name = 'sfftkrw.schema.adapter_{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
adapter = importlib.import_module(adapter_name)

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
emdb_sff = importlib.import_module(emdb_sff_name)


class TestSFFRGBA(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_hdf5_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test.hdf5')

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.test_hdf5_fn)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.red = random.random()
        self.green = random.random()
        self.blue = random.random()
        self.alpha = random.random()

    def test_default(self):
        """Test default colour"""
        colour = adapter.SFFRGBA()
        colour.red = self.red
        colour.green = self.green
        colour.blue = self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, 1.0)

    def test_kwarg_colour(self):
        """Test colour using kwargs"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_get_value(self):
        """Test colour.value"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        red, green, blue, alpha = colour.value
        self.assertEqual(colour.red, red)
        self.assertEqual(colour.green, green)
        self.assertEqual(colour.blue, blue)
        self.assertEqual(colour.alpha, alpha)

    def test_set_value(self):
        """Test colour.value = rgb(a)"""
        # rgb
        colour = adapter.SFFRGBA()
        colour.value = self.red, self.green, self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        # rgba
        colour.value = self.red, self.green, self.blue, self.alpha
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_as_hff(self):
        """Test convert to HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)

    def test_from_hff(self):
        """Test create from HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)
            colour2 = adapter.SFFRGBA.from_hff(h[u'container'])
            self.assertCountEqual(colour.value, colour2.value)

    def test_native_random_colour(self):
        """Test that using a kwarg random_colour will set random colours"""
        colour = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(0 <= colour.red <= 1)
        self.assertTrue(0 <= colour.green <= 1)
        self.assertTrue(0 <= colour.blue <= 1)
        self.assertTrue(0 <= colour.alpha <= 1)

    def test_validation(self):
        """Test that validation works"""
        c = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(c._is_valid())
        c = adapter.SFFRGBA()
        self.assertFalse(c._is_valid())

    def test_as_json(self):
        """Test export to JSON"""
        # empty
        c = adapter.SFFRGBA()
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            c.as_json()
        # populated
        c = adapter.SFFRGBA(random_colour=True)
        c_json = c.as_json()
        # _print(c_json)
        self.assertEqual(c_json[u'colour'], c.value)

    def test_from_json(self):
        """Test import from JSON"""
        c_json = {'colour': (0.8000087483646712, 0.017170600210644427, 0.5992636068532492, 1.0)}
        c = adapter.SFFRGBA.from_json(c_json)
        # _print(c)
        self.assertEqual(c.value, c_json[u'colour'])
