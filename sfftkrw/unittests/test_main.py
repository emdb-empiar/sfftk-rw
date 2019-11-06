#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_py

Unit tests for convert subcommand
"""
from __future__ import division, print_function

import glob
import os
import sys
import shlex
import unittest

from . import TEST_DATA_PATH
from .. import sffrw as Main
from ..core.parser import parse_args

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'


class TestMainHandleConvert(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        for s in glob.glob(os.path.join(TEST_DATA_PATH, '*.sff')):
            os.remove(s)

    def test_unknown(self):
        """Test that unknown fails"""
        args = parse_args('convert --verbose -o {} {}'.format(
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
        args = parse_args('convert --verbose -o {} {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .hff
        args = parse_args('convert --verbose {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_hff(self):
        """Test that we can convert .hff"""
        #  first convert from .sff
        args = parse_args('convert --verbose -o {output} {input}'.format(
            output=os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .sff
        args = parse_args('convert --verbose {input} -o {output}'.format(
            input=os.path.join(TEST_DATA_PATH, 'test_data.hff'),
            output=os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)

    def test_json(self):
        """Test that we can convert .json"""
        #  first convert from some other format e.g. .mod
        args = parse_args('convert --verbose -o {output} {input}'.format(
            output=os.path.join(TEST_DATA_PATH, 'test_data.json'),
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .sff
        args = parse_args('convert --verbose {} -o {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.json'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.hff'))
        self.assertEqual(len(sff_files), 1)


class TestMainHandleView(unittest.TestCase):
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


class TestMainHandleTests(unittest.TestCase):
    """The test runners"""

    def test_module_test_runner(self):
        """Test correct functionality of `_module_test_runner`"""
        from ..sffrw import _module_test_runner
        from . import test_base
        args = parse_args(u"tests all", use_shlex=True)
        status = _module_test_runner(test_base, args)
        self.assertEqual(status, os.EX_OK)

    def test_discover_test_runner(self):
        """Test correct functionality of `_discover_test_runner`"""
        from ..sffrw import _discover_test_runner
        args = parse_args(u"tests schema", use_shlex=True)
        path = ".."  # no tests to be found here
        status = _discover_test_runner(path, args)
        self.assertEqual(status, os.EX_OK)

    def test_testcase_test_runner(self):
        """Test correct functionality of `_testcase_test_runner`"""
        from ..sffrw import _testcase_test_runner
        args = parse_args(u"tests schema", use_shlex=True)
        from .test_base import TestSFFTypeError
        status = _testcase_test_runner(TestSFFTypeError, args)
        self.assertEqual(status, os.EX_OK)

    def test_handle_tests_all(self):
        """Test the `tests all` tests command"""
        args = parse_args(u"tests all --dry-run", use_shlex=True)
        self.assertEqual(Main.handle_tests(args), os.EX_OK)

    def test_handle_tests_main(self):
        """Test the `tests main` tests command"""
        args = parse_args(u"tests main --dry-run", use_shlex=True)
        self.assertEqual(Main.handle_tests(args), os.EX_OK)

    def test_handle_tests_core(self):
        """Test the `tests core` tests command"""
        args = parse_args(u"tests core --dry-run", use_shlex=True)
        self.assertEqual(Main.handle_tests(args), os.EX_OK)

    def test_handle_tests_schema(self):
        """Test the `tests schema` tests command"""
        args = parse_args(u"tests schema --dry-run", use_shlex=True)
        self.assertEqual(Main.handle_tests(args), os.EX_OK)


class TestMainMain(unittest.TestCase):
    def test_main_convert(self):
        """Test the main entry point"""
        in_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'emd_1832.sff')
        cmd = shlex.split(u"sfr convert --verbose {}".format(
            in_file,
        ))
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)

    def test_main_view(self):
        """Test the main entry point"""
        in_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'emd_1832.sff')
        cmd = shlex.split(u"sfr view {}".format(
            in_file,
        ))
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)

    def test_main_tests(self):
        """Test the main entry point"""
        cmd = shlex.split(u"sfr tests all --dry-run")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)

    def test_main_error(self):
        """Test for wrong input"""
        cmd = shlex.split(u"sfr tests")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)
        cmd = shlex.split(u"sfr convert file.sff -f file.abc")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_USAGE)
