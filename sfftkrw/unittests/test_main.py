#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_py

Unit tests for convert subcommand
"""
from __future__ import division

import glob
import os
import unittest

from . import TEST_DATA_PATH
from .. import BASE_DIR
from .. import sffrw as Main
from ..core.parser import parse_args

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'

user = 'test_user'
password = 'test'
host = 'localhost'
port = '4064'


class TestMain_handle_convert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sffrw.conf')

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        for s in glob.glob(os.path.join(TEST_DATA_PATH, '*.sff')):
            os.remove(s)

    def test_seg(self):
        """Test that we can convert .seg"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.seg'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        self.assertEqual(len(sff_files), 1)

    def test_mod(self):
        """Test that we can convert .mod"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.mod'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        self.assertEqual(len(sff_files), 1)

    def test_am(self):
        """Test that we can convert .am"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.am'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        self.assertEqual(len(sff_files), 1)

    def test_surf(self):
        """Test that we can convert .surf"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.surf'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        self.assertEqual(len(sff_files), 1)

    def test_survos(self):
        """Test that we can convert SuRVoS (.h5) files"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.h5'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        self.assertEqual(len(sff_files), 1)

    def test_unknown(self):
        """Test that unknown fails"""
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.xxx'),
            self.config_fn,
        ), use_shlex=True)
        with self.assertRaises(ValueError):
            Main.handle_convert(args, configs)
        # sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        # self.assertEqual(len(sff_files), 0)

    def test_sff(self):
        """Test that we can convert .sff"""
        #  first convert from some other format e.g. .mod
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.mod'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        # then convert to .hff
        args, configs = parse_args('convert {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_hff(self):
        """Test that we can convert .hff"""
        #  first convert from some other format e.g. .mod
        args, configs = parse_args('convert -o {} {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.mod'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        # then convert to .sff
        args, configs = parse_args('convert {} -o {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_json(self):
        """Test that we can convert .json"""
        #  first convert from some other format e.g. .mod
        args, configs = parse_args('convert -o {output} {input} --config-path {config}'.format(
            output=os.path.join(TEST_DATA_PATH, 'test_data.json'),
            input=os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.mod'),
            config=self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        # then convert to .sff
        args, configs = parse_args('convert {} -o {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.json'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            self.config_fn,
        ), use_shlex=True)
        Main.handle_convert(args, configs)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)


"""
:TODO: view .hff, .json
"""


class TestMain_handle_view(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sffrw.conf')

    def test_read_am(self):
        """Test that we can view .am"""
        args, configs = parse_args('view {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.am'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))

    def test_read_map(self):
        """Test that we can view .map"""
        args, configs = parse_args('view {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.map'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))

    def test_read_mod(self):
        """Test that we can view .mod"""
        args, configs = parse_args('view {} --config-path {} --show-chunks'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.mod'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))

    def test_seg(self):
        """Test that we can view .seg"""
        args, configs = parse_args('view {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.seg'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))

    def test_read_surf(self):
        """Test that we can view .surf"""
        args, configs = parse_args('view {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.surf'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))

    def test_read_unknown(self):
        """Test that we cannot view unknown"""
        args, configs = parse_args('view {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.xxx'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args, configs))


class TestMain_handle_notes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sffrw.conf')

    def test_list(self):
        """Test that we can list notes"""
        args, configs = parse_args('notes list {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_notes_list(args, configs))

    def test_show(self):
        """Test that we can list notes"""
        args, configs = parse_args('notes show -i 15559 {} --config-path {}'.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff'),
            self.config_fn,
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_notes_show(args, configs))

    def test_search(self):
        """Test that we can list notes"""
        args, configs = parse_args('notes search "mitochondria" --config-path {}'.format(self.config_fn),
                                   use_shlex=True)
        self.assertEqual(0, Main.handle_notes_search(args, configs))


class TestMain_handle_prep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sffrw.conf')

    def setUp(self):
        self.test_data = os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.map')

    def tearDown(self):
        os.remove(os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data_prep.map'))

    def test_ccp4_binmap(self):
        """Test that we can prepare a CCP4 map by binning"""
        args, configs = parse_args('prep binmap -v {}'.format(self.test_data), use_shlex=True)
        self.assertEqual(os.EX_OK, Main.handle_prep(args, configs))
