#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_py

Unit tests for convert subcommand
"""
from __future__ import division, print_function

import glob
import importlib
import os
import shlex
import shutil
import sys

from . import TEST_DATA_PATH, Py23FixTestCase
from .. import SFFSegmentation
from .. import sffrw as Main
from ..core.parser import parse_args

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'


class TestMainHandleConvert(Py23FixTestCase):
    def setUp(self):
        super(TestMainHandleConvert, self).setUp()

    def tearDown(self):
        super(TestMainHandleConvert, self).tearDown()
        for s in glob.glob(os.path.join(TEST_DATA_PATH, '*.sff')):
            os.remove(s)
        hff_fn = os.path.join(TEST_DATA_PATH, 'test_data.hff')
        if os.path.exists(hff_fn):
            os.remove(hff_fn)
        json_fn = os.path.join(TEST_DATA_PATH, 'test_data.json')
        if os.path.exists(json_fn):
            os.remove(json_fn)

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
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.hff'),
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
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.sff'),
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
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # then convert to .sff
        args = parse_args('convert --verbose {} -o {}'.format(
            os.path.join(TEST_DATA_PATH, 'test_data.json'),
            os.path.join(TEST_DATA_PATH, 'test_data.sff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        sff_files = glob.glob(os.path.join(TEST_DATA_PATH, '*.json'))
        self.assertEqual(len(sff_files), 1)

    def test_json_exclude_geometry(self):
        """Test that we can convert to JSON and exclude geometry"""
        # convert normally
        output_fn = os.path.join(TEST_DATA_PATH, 'test_data.json')
        args = parse_args('convert --verbose -o {output} {input}'.format(
            output=output_fn,
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # read
        seg = SFFSegmentation.from_file(output_fn, args)
        segment = seg.segment_list[0]  # the first one
        # check that there is geometry
        self.stderrj(segment.as_json())
        self.assertIsNotNone(segment.three_d_volume)
        self.assertTrue(len(seg.lattice_list) > 0)
        # convert and exclude geometry
        args = parse_args('convert --verbose --exclude-geometry -o {output} {input}'.format(
            output=output_fn,
            input=os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.hff'),
        ), use_shlex=True)
        Main.handle_convert(args)
        # read
        seg = SFFSegmentation.from_file(output_fn, args)
        segment = seg.segment_list[0]  # the first one
        # check that there is no geometry
        self.stderrj(segment.as_json())
        self.assertIsNone(segment.three_d_volume)
        self.assertTrue(len(seg.lattice_list) == 0)


class TestMainHandleView(Py23FixTestCase):
    def test_read_sff(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.sff'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_hff(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.hff'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_json(self):
        """Test that we can view .mod"""
        args = parse_args('view {} '.format(
            os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1832.json'),
        ), use_shlex=True)
        self.assertEqual(0, Main.handle_view(args))

    def test_read_unknown(self):
        """Test that we cannot view unknown"""
        args = parse_args('view {}'.format(
            os.path.join(TEST_DATA_PATH, 'segmentations', 'test_data.xxx'),

        ), use_shlex=True)
        with self.assertRaises(ValueError):
            Main.handle_view(args)


class TestMainHandleTests(Py23FixTestCase):
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


class TestMainMain(Py23FixTestCase):
    def test_main_convert(self):
        """Test the main entry point"""
        _in_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1832.sff')
        in_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1832_copy.sff')
        shutil.copy(_in_file, in_file)
        cmd = shlex.split(u"sff convert --verbose {}".format(
            in_file,
        ))
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)
        copies = glob.glob(os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1832_copy.*'))
        if copies:
            for copy in copies:
                os.remove(copy)

    def test_main_view(self):
        """Test the main entry point"""
        in_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1832.sff')
        cmd = shlex.split(u"sff view {}".format(
            in_file,
        ))
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)

    def test_main_tests(self):
        """Test the main entry point"""
        cmd = shlex.split(u"sff tests all --dry-run")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)

    def test_main_error(self):
        """Test for wrong input"""
        cmd = shlex.split(u"sff tests")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_OK)
        cmd = shlex.split(u"sff convert file.sff -f file.abc")
        sys.argv = cmd
        status = Main.main()
        self.assertEqual(status, os.EX_USAGE)

    def test_abbreviated_import(self):
        """Test importing user-classes from sfftkrw"""
        mod_name = 'sfftkrw'
        mod = importlib.import_module(mod_name)
        self.assertEqual(mod.SFFSegmentation, SFFSegmentation)
        s1, s2 = mod.SFFSegmentation(), SFFSegmentation()
        # ensure we're working on the same version
        self.assertEqual(s1.version, s2.version)

    def test_import_api_namespaces(self):
        """Test that we can import all adapter classes from the package"""
        adapter_name = "sfftkrw"
        adapter = importlib.import_module(adapter_name)
        self.assertTrue(hasattr(adapter, u'SFFSegmentation'))
        self.assertTrue(hasattr(adapter, u'gds_api'))
