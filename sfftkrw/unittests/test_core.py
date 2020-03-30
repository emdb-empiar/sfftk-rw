# -*- coding: utf-8 -*-
# test_core.py
"""Unit tests for :py:mod:`sfftkrw.core` package"""
from __future__ import division, print_function

import os
import random
import sys

from random_words import RandomWords, LoremIpsum

rw = RandomWords()
li = LoremIpsum()

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase
from ..core import print_tools
from ..core import utils
from ..core.parser import parse_args, tool_list

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-05-15"


class TestParser(Py23FixTestCase):
    def test_default(self):
        """Test that default operation is OK"""
        args = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)

    def test_use_shlex(self):
        """Test that we can use shlex i.e. treat command as string"""
        args = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)

    def test_fail_use_shlex(self):
        """Test that we raise an error when use_shlex=True but _args not str"""
        args = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)


class TestCorePrintUtils(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCorePrintUtils, cls).setUpClass()
        cls._weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def setUp(self):
        self.temp_fn = 'temp_file.txt'
        if sys.version_info[0] > 2:
            self.temp_file = open(self.temp_fn, 'w+', newline='\r\n')
        else:
            self.temp_file = open(self.temp_fn, 'w+')

    def tearDown(self):
        os.remove(self.temp_fn)

    def test_print_date_default(self):
        """Test default arguments for print_tools.print_date(...)"""
        print_tools.print_date("Test", stream=self.temp_file)
        self.temp_file.flush()  # flush buffers
        self.temp_file.seek(0)  # rewind the files
        data = self.temp_file.readlines()[0]
        _words = data.split(' ')
        self.assertIn(_words[0], self._weekdays)  # the first part is a date
        self.assertEqual(_words[-1][-1], '\n')  #  the last letter is a newline

    def test_print_date_non_basestring(self):
        """Test exception when print_string is not a basestring subclass"""
        with self.assertRaises(ValueError):
            print_tools.print_date(3)

    def test_print_date_no_newline(self):
        """Test that we lack a newline at the end"""
        print_tools.print_date("Test", stream=self.temp_file, newline=False)
        self.temp_file.flush()  # flush buffers
        self.temp_file.seek(0)  # rewind the files
        data = self.temp_file.readlines()[0]
        _words = data.split(' ')
        self.assertNotEqual(_words[-1][-1], '\n')

    def test_print_date_no_date(self):
        """Test that we lack a date at the beginning"""
        print_tools.print_date("Test", stream=self.temp_file, incl_date=False)
        self.temp_file.flush()  # flush buffers
        self.temp_file.seek(0)  # rewind the files
        data = self.temp_file.readlines()[0]
        _words = data.split(' ')
        self.assertNotIn(_words[0], self._weekdays)  # the first part is a date

    def test_print_date_no_newline_no_date(self):
        """Test that we can exclude both newline and the date"""
        print_tools.print_date("Test", stream=self.temp_file, newline=False, incl_date=False)
        self.temp_file.flush()
        self.temp_file.seek(0)
        data = self.temp_file.readline()
        self.assertEqual(data, 'Test')

    def test_printable_ascii_string(self):
        """Test whether we can get a printable substring"""
        s_o = li.get_sentence().encode('utf-8')
        unprintables = list(range(14, 32))
        s_u = b''.join([chr(random.choice(unprintables)).encode('utf-8') for _ in range(100)])
        s = s_o + s_u
        s_p = print_tools.get_printable_ascii_string(s)
        self.assertEqual(s_p, s_o)
        s_pp = print_tools.get_printable_ascii_string(s_u)
        self.assertEqual(s_pp, b'')
        s_b = print_tools.get_printable_ascii_string('')
        self.assertEqual(s_b, b'')

    def test_print_static(self):
        """Test that we can print_static

        * write two sentences
        * only the second one appears because first is overwritten
        """
        s = li.get_sentence()
        print_tools.print_static(s, stream=self.temp_file)
        self.temp_file.flush()
        s1 = li.get_sentence()
        print_tools.print_static(s1, stream=self.temp_file)
        self.temp_file.flush()
        self.temp_file.seek(0)
        _data = self.temp_file.read()
        data = _data[0]
        self.assertEqual(data[0], '\r')
        self.assertTrue(len(_data) > len(s) + len(s1))
        r_split = _data.split('\r')  # split at the carriage reset
        self.assertTrue(len(r_split), 3)  # there should be three items in the list
        self.assertEqual(r_split[1].split('\t')[1], s)  # split the first string and get the actual string (ex. date)
        self.assertEqual(r_split[2].split('\t')[1], s1)  # split the second string and get the actual string (ex. date)

    def test_print_static_no_date(self):
        """Test print static with no date"""
        s = li.get_sentence()
        print_tools.print_static(s, stream=self.temp_file, incl_date=False)
        self.temp_file.flush()
        s1 = li.get_sentence()
        print_tools.print_static(s1, stream=self.temp_file, incl_date=False)
        self.temp_file.seek(0)
        data = self.temp_file.readlines()[0]
        self.assertEqual(data[0], '\r')
        self.assertTrue(len(data) > len(s) + len(s1))
        r_split = data.split('\r')  # split at the carriage reset
        self.assertTrue(len(r_split), 3)  # there should be three items in the list
        self.assertEqual(r_split[1], s)  # split the first string and get the actual string (ex. date)
        self.assertEqual(r_split[2], s1)  # split the second string and get the actual string (ex. date)

    def test_print_static_valueerror(self):
        """Test that we assert print_string type"""
        with self.assertRaises(ValueError):
            print_tools.print_static(1)

    def test_print_static_str(self):
        """Test that we can work with unicode"""
        s = li.get_sentence()
        print_tools.print_static(str(s), stream=self.temp_file)
        self.temp_file.flush()
        self.temp_file.seek(0)
        data = self.temp_file.readlines()[0]
        self.assertEqual(data[0], '\r')
        r_split = data.split('\r')
        self.assertEqual(len(r_split), 2)
        self.assertEqual(r_split[1].split('\t')[1], s)


class TestCoreParserConvert(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        print("convert tests...", file=sys.stderr)
        cls.test_data_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
        cls.test_sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')
        cls.test_hff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.hff')

    @classmethod
    def tearDownClass(cls):
        print("", file=sys.stderr)

    def test_default(self):
        """Test convert parser"""
        args = parse_args('convert {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.subcommand, 'convert')
        self.assertEqual(args.from_file, self.test_data_file)
        self.assertIsNone(args.details)
        self.assertEqual(args.output, os.path.join(os.path.dirname(self.test_data_file), 'emd_1014.hff'))
        self.assertEqual(args.primary_descriptor, None)
        self.assertFalse(args.verbose)
        self.assertFalse(args.exclude_geometry)
        self.assertFalse(args.json_sort)
        self.assertEqual(args.json_indent, 2)

    def test_details(self):
        """Test convert parser with details"""
        args = parse_args('convert -D "Some details" {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.details, 'Some details')

    def test_output_sff(self):
        """Test convert parser to .sff"""
        args = parse_args('convert {} -o file.sff'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.sff')

    def test_output_hff(self):
        """Test convert parser to .hff"""
        args = parse_args('convert {} -o file.hff'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.hff')

    def test_output_json(self):
        """Test convert parser to .json"""
        args = parse_args('convert {} -o file.json'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.json')

    def test_hff_default_output_sff(self):
        """Test that converting an .hff with no args gives .sff"""
        args = parse_args('convert {}'.format(self.test_hff_file), use_shlex=True)
        self.assertEqual(args.output, self.test_sff_file)

    def test_sff_default_output_hff(self):
        """Test that converting a .sff with no args gives .hff"""
        args = parse_args('convert {}'.format(self.test_sff_file), use_shlex=True)
        self.assertEqual(args.output, self.test_hff_file)

    def test_primary_descriptor(self):
        """Test convert parser with primary_descriptor"""
        args = parse_args('convert -R threeDVolume {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.primary_descriptor, 'threeDVolume')

    def test_wrong_primary_descriptor_fails(self):
        """Test that we have a check on primary descriptor values"""
        args = parse_args('convert -R something {}'.format(self.test_data_file), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)

    def test_verbose(self):
        """Test convert parser with verbose"""
        args = parse_args('convert -v {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertTrue(args.verbose)

    def test_exclude_geometry(self):
        """Test flag to exclude geometry"""
        args = parse_args('convert -v -x {}'.format(self.test_data_file), use_shlex=True)
        self.assertTrue(args.exclude_geometry)

    def test_json_sort(self):
        """Test that we can sort for JSON"""
        args = parse_args('convert -v --json-sort -f json {}'.format(self.test_data_file), use_shlex=True)
        self.assertTrue(args.json_sort)

    def test_json_indent(self):
        """Test that we can sort for JSON"""
        indent = _random_integer(start=1, stop=10)
        args = parse_args(
            'convert -v -f json --json-indent {indent} {file_}'.format(
                indent=indent,
                file_=self.test_data_file
            ),
            use_shlex=True
        )
        self.assertEqual(args.json_indent, indent)
        # failure
        indent = - _random_integer(start=1, stop=10)
        args = parse_args(
            'convert -v -f json --json-indent {indent} {file_}'.format(
                indent=indent,
                file_=self.test_data_file
            ),
            use_shlex=True
        )
        self.assertEqual(args, os.EX_USAGE)

class TestCoreParserView(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        print("view tests...", file=sys.stderr)

    @classmethod
    def tearDownClass(cls):
        print("", file=sys.stderr)

    def test_default(self):
        """Test view parser"""
        args = parse_args('view file.sff', use_shlex=True)
        self.assertEqual(args.from_file, 'file.sff')
        self.assertFalse(args.version)

    def test_version(self):
        """Test view version"""
        args = parse_args('view --sff-version file.sff', use_shlex=True)
        self.assertTrue(args.sff_version)


class TestCoreParserTests(Py23FixTestCase):
    def test_tests_default(self):
        """Test that tests can be launched"""
        args = parse_args("tests all", use_shlex=True)
        self.assertEqual(args.subcommand, 'tests')
        self.assertCountEqual(args.tool, ['all'])
        self.assertFalse(args.dry_run)

    def test_tests_one_tool(self):
        """Test that with any tool we get proper tool"""
        tool = random.choice(tool_list)
        args = parse_args("tests {}".format(tool), use_shlex=True)
        self.assertCountEqual(args.tool, [tool])

    def test_multi_tool(self):
        """Test that we can specify multiple packages (tools) to test"""
        tools = set()
        while len(tools) < 3:
            tools.add(random.choice(tool_list))
        tools = list(tools)
        # normalise
        if 'all' in tools:
            tools = ['all']
        args = parse_args("tests {}".format(' '.join(tools)), use_shlex=True)
        self.assertCountEqual(args.tool, tools)

    def test_tool_fail(self):
        """Test that we catch a wrong tool"""
        args = parse_args("tests wrong_tool_spec", use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)

    def test_tests_no_tool(self):
        """Test that with no tool we simply get usage info"""
        args = parse_args("tests", use_shlex=True)
        self.assertEqual(args, os.EX_OK)

    def test_valid_verbosity(self):
        """Test valid verbosity"""
        args = parse_args("tests all -v 0", use_shlex=True)
        self.assertEqual(args.verbosity, 0)
        args = parse_args("tests all -v 1", use_shlex=True)
        self.assertEqual(args.verbosity, 1)
        args = parse_args("tests all -v 2", use_shlex=True)
        self.assertEqual(args.verbosity, 2)
        args = parse_args("tests all -v 3", use_shlex=True)
        self.assertEqual(args.verbosity, 3)

    def test_invalid_verbosity(self):
        """Test that verbosity is in [0,3]"""
        v1 = _random_integer(start=4)
        args = parse_args("tests all -v {}".format(v1), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)
        v2 = -_random_integer(start=0)
        args = parse_args("tests all -v {}".format(v2), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)

    def test_dry_run(self):
        """Test that we can set the `dry-run` argument"""
        args = parse_args(u"tests all --dry-run", use_shlex=True)
        self.assertTrue(args.dry_run)


class TestCoreUtils(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCoreUtils, cls).setUpClass()
        print("utils tests...", file=sys.stderr)
        cls.v7_sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        cls.v8_sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.8', 'emd_1014.sff')

    def test_get_path_one_level(self):
        """Test that we can get an item at a path one level deep"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': x, 1: y}
        path = ['a']
        self.assertEqual(utils.get_path(D, path), x)
        path = [1]
        self.assertEqual(utils.get_path(D, path), y)

    def test_get_path_two_level(self):
        """Test that we can get an item at a path two levels deep"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': {
            'b': x,
            1: y,
        }}
        path = ['a', 'b']
        self.assertEqual(utils.get_path(D, path), x)
        path = ['a', 1]
        self.assertEqual(utils.get_path(D, path), y)

    def test_get_path_three_levels(self):
        """Test that we can get an item at a path three levels deep"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': {
            'b': {
                'c': x,
            },
            1: {
                2: y,
            }
        }}
        path = ['a', 'b', 'c']
        self.assertEqual(utils.get_path(D, path), x)
        path = ['a', 1, 2]
        self.assertEqual(utils.get_path(D, path), y)

    def test_get_path_four_levels(self):
        """Test that we can get an item at a path four levels deep"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': {
            'b': {
                'c': {
                    'd': x,
                },
                1: {
                    2: y,
                }
            }
        }}
        path = ['a', 'b', 'c', 'd']
        self.assertEqual(utils.get_path(D, path), x)
        path = ['a', 'b', 1, 2]
        self.assertEqual(utils.get_path(D, path), y)

    def test_get_path_keyerror(self):
        """Test that we get a KeyError exception if the path does not exist"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': {
            'b': {
                'c': {
                    'd': x,
                },
                'e': {
                    'f': y,
                }
            }
        }}
        path = ['a', 'b', 'c', 'f']
        val = utils.get_path(D, path)
        self.assertIsNone(val)

    def test_get_path_nondict_type_error(self):
        """Test that we get an exception when D is not a dict"""
        D = ['some rubbish list']
        path = ['a']
        with self.assertRaises(AssertionError):
            utils.get_path(D, path)

    def test_get_path_unhashable_in_path(self):
        """Test that unhashable in path fails"""
        x = _random_integer()
        y = _random_integer()
        D = {'a': x, 'b': y}
        path = [[5]]
        with self.assertRaises(TypeError):
            utils.get_path(D, path)

    def test_rgba_to_hex(self):
        """Test converting colours"""
        hex1 = utils.rgba_to_hex((0, 0, 0, 0))
        self.assertEqual(hex1, '#000000')
        hex2 = utils.rgba_to_hex((0, 0, 0, 0), channels=4)
        self.assertEqual(hex2, '#00000000')
        hex3 = utils.rgba_to_hex((0, 0, 0))
        self.assertEqual(hex3, '#000000')
        hex4 = utils.rgba_to_hex((0, 0, 0), channels=4)
        self.assertEqual(hex4, '#000000ff')
        with self.assertRaises(ValueError):
            utils.rgba_to_hex((2, 2, 2, 0), channels=4)
        with self.assertRaises(ValueError):
            utils.rgba_to_hex((0, 0, 0, 0), channels=5)

    def test_parse_and_split(self):
        """Test the parser utility"""
        cmd = 'view file.sff'
        args = parse_args(cmd, use_shlex=True)
        self.assertEqual(args.subcommand, 'view')
        self.assertEqual(args.from_file, 'file.sff')

    def test_get_version(self):
        """Test that we can reliably get the version from an EMDB-SFF file"""
        v7_version = utils.get_version(self.v7_sff_file)
        self.assertEqual(v7_version, '0.7.0.dev0')
        v8_version = utils.get_version(self.v8_sff_file)
        self.assertEqual(v8_version, '0.8.0.dev1')

    def test_get_unique_id(self):
        from ..core.utils import get_unique_id
        id_1 = get_unique_id()
        self.stderr(id_1)
        # would a second import alter anything?
        from ..core.utils import get_unique_id
        id_2 = get_unique_id()
        self.assertTrue(id_1 + 1 == id_2)
