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
from .. import sffrw as Main
from ..core.parser import parse_args

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'


class TestMain_handle_convert(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        for s in glob.glob(os.path.join(TEST_DATA_PATH, '*.sff')):
            os.remove(s)

    def test_unknown(self):
        """Test that unknown fails"""
        args = parse_args('convert -o {} {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.xxx'),
        ), use_shlex=True)
        with self.assertRaises(ValueError):
            Main.handle_convert(args)
        # sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.sff'))
        # self.assertEqual(len(sff_files), 0)

    def test_sff(self):
        """Test that we can convert .sff"""
        #  first convert from some other format e.g. .mod
        args = parse_args('convert -o {} {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .hff
        args = parse_args('convert {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_hff(self):
        """Test that we can convert .hff"""
        #  first convert from some other format e.g. .mod
        args = parse_args('convert -o {} {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .sff
        args = parse_args('convert {} -o {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_json(self):
        """Test that we can convert .json"""
        #  first convert from some other format e.g. .mod
        args = parse_args('convert -o {output} {input}'.format(
            output=os.path.join(TEST_DATA_PATH, 'test_data.json'),
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .sff
        args = parse_args('convert {} -o {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.json'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)


class TestMain_handle_view(unittest.TestCase):
    def test_read_sff(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.sff'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_hff(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.hff'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_json(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.json'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_unknown(self):
        """Test that we cannot view unknown"""
        args = parse_args('view {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.xxx'),

        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))
