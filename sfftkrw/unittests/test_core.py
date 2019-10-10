# -*- coding: utf-8 -*-
# test_core.py
"""Unit tests for :py:mod:`sfftkrw.core` package"""
from __future__ import division, print_function

import glob
import os
import random
import shlex
import shutil
import sys

from random_words import RandomWords, LoremIpsum

from . import TEST_DATA_PATH, _random_integer, Py23FixTestCase
from .. import BASE_DIR
from ..core import print_tools
from ..core import utils, _dict_iter_items, _dict
from ..core.configs import Configs, get_config_file_path, load_configs, \
    get_configs, set_configs, del_configs
from ..core.parser import Parser, parse_args, tool_list

rw = RandomWords()
li = LoremIpsum()

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-05-15"


class TestParser(Py23FixTestCase):
    def test_default(self):
        """Test that default operation is OK"""
        args, configs = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)
        self.assertIsNone(configs)

    def test_use_shlex(self):
        """Test that we can use shlex i.e. treat command as string"""
        args, configs = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)
        self.assertIsNone(configs)

    def test_fail_use_shlex(self):
        """Test that we raise an error when use_shlex=True but _args not str"""
        args, configs = parse_args("--version", use_shlex=True)
        self.assertEqual(args, os.EX_OK)
        self.assertIsNone(configs)


class TestCoreConfigs(Py23FixTestCase):
    user_configs = os.path.expanduser("~/.sfftkrw/sffrw.conf")
    user_configs_hide = os.path.expanduser("~/.sfftkrw/sffrw.conf.test")
    dummy_configs = os.path.expanduser("~/sffrw.conf.test")

    @classmethod
    def setUpClass(cls):
        cls.test_config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'test_sff.conf')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffrw.conf')
        cls.config_values = _dict()
        cls.config_values['__TEMP_FILE'] = './temp-annotated.json'
        cls.config_values['__TEMP_FILE_REF'] = '@'

    @classmethod
    def tearDownClass(cls):
        pass

    def load_values(self):
        """Load config values into test config file"""
        with open(self.config_fn, 'w') as f:
            for n, v in _dict_iter_items(self.config_values):
                f.write('{}={}\n'.format(n, v))

    def clear_values(self):
        """Empty test config file"""
        with open(self.config_fn, 'w') as _:
            pass

    def setUp(self):
        self.load_values()
        self.move_user_configs()

    def tearDown(self):
        self.clear_values()
        self.return_user_configs()

    def move_user_configs(self):
        # when running this test we need to hide ~/.sfftkrw/sffrw.conf if it exists
        # we move ~/.sfftkrw/sffrw.conf to ~/.sfftkrw/sffrw.conf.test
        # then move it back once the test ends
        # if the test does not complete we will have to manually copy it back
        # ~/.sfftkrw/sffrw.conf.test to ~/.sfftkrw/sffrw.conf
        if os.path.exists(self.user_configs):
            print('found user configs and moving them...', file=sys.stderr)
            shutil.move(
                self.user_configs,
                self.user_configs_hide,
            )

    def return_user_configs(self):
        # we move back ~/.sfftkrw/sffrw.conf.test to ~/.sfftkrw/sffrw.conf
        if os.path.exists(self.user_configs_hide):
            print('found moved user configs and returning them...', file=sys.stderr)
            shutil.move(
                self.user_configs_hide,
                self.user_configs,
            )
        else:  # it was never there to begin with
            try:
                os.remove(self.user_configs)
            except OSError:
                pass

    def make_dummy_user_configs(self, param='TEST', value='TEST_VALUE'):
        if not os.path.exists(os.path.dirname(self.user_configs)):
            os.mkdir(os.path.dirname(self.user_configs))
        with open(self.user_configs, 'w') as c:
            c.write("{}={}\n".format(param, value))

    def remove_dummy_user_configs(self):
        os.remove(self.user_configs)

    def make_dummy_configs(self, param='TEST_CONFIG', value='TEST_CONFIG_VALUE'):
        with open(self.dummy_configs, 'w') as c:
            c.write("{}={}\n".format(param, value))

    def remove_dummy_configs(self):
        os.remove(self.dummy_configs)

    def test_default_ro(self):
        """Test that on a fresh install we use shipped configs for get"""
        args = Parser.parse_args(shlex.split("config get --all"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == Configs.shipped_configs)

    def test_user_configs_ro(self):
        """Test that if we have user configs we get them"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("config get --all"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == self.user_configs)
        self.remove_dummy_user_configs()

    def test_shipped_default(self):
        """Test that we get shipped and nothing else when we ask for them"""
        args = Parser.parse_args(shlex.split("config get --shipped-configs --all"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, Configs.shipped_configs)

    def test_shipped_user_configs_exist_ro(self):
        """Test that even if user configs exist we can only get shipped configs"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("config get --shipped-configs --all"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, Configs.shipped_configs)
        self.remove_dummy_user_configs()

    def test_config_path_default_ro(self):
        """Test that we can get configs from some path"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("config get --config-path {} --all".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_user_configs()

    def test_config_path_over_shipped_ro(self):
        """Test that we use config path even if shipped specified"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(
            shlex.split("config get --config-path {} --shipped-configs --all".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_user_configs()

    def test_default_rw(self):
        """Test that when we try to write configs on a fresh install we get user configs"""
        args = Parser.parse_args(shlex.split("config set A B"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == self.user_configs)
        self.assertTrue(os.path.exists(self.user_configs))

    def test_user_configs_rw(self):
        """Test that if we have user configs we can set to them"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("config set A B"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == self.user_configs)
        self.remove_dummy_user_configs()

    def test_shipped_default_rw(self):
        """Test that we cannot write to shipped configs"""
        args = Parser.parse_args(shlex.split("config set --shipped-configs A B"))
        config_file_path = get_config_file_path(args)
        self.assertIsNone(config_file_path)

    def test_config_path_default_rw(self):
        """Test that we can get configs from some path"""
        self.make_dummy_configs()
        args = Parser.parse_args(shlex.split("config set --config-path {} A B".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_configs()

    def test_config_path_over_shipped_rw(self):
        """Test that we use config path even if shipped specified"""
        self.make_dummy_configs()
        args = Parser.parse_args(
            shlex.split("config set --config-path {} --shipped-configs A B".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_configs()

    def test_default_other(self):
        """Test that all non-config commands on a fresh install use shipped configs"""
        args = Parser.parse_args(shlex.split("view file.json"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == Configs.shipped_configs)
        self.assertFalse(os.path.exists(self.user_configs))

    def test_user_configs_other(self):
        """Test that if we have user configs we can set to them"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("view file.json"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == self.user_configs)
        self.remove_dummy_user_configs()

    def test_shipped_default_other(self):
        """Test that we cannot write to shipped configs even if we have user configs"""
        self.make_dummy_user_configs()
        args = Parser.parse_args(shlex.split("view file.json --shipped-configs"))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path == Configs.shipped_configs)
        self.remove_dummy_user_configs()

    def test_config_path_default_other(self):
        """Test that we can get configs from some path"""
        self.make_dummy_configs()
        args = Parser.parse_args(shlex.split("view --config-path {} file.json".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_configs()

    def test_config_path_over_shipped_other(self):
        """Test that we use config path even if shipped specified"""
        self.make_dummy_configs()
        args = Parser.parse_args(
            shlex.split("view --config-path {} --shipped-configs file.json".format(self.dummy_configs)))
        config_file_path = get_config_file_path(args)
        self.assertTrue(config_file_path, self.dummy_configs)
        self.remove_dummy_configs()

    def test_load_shipped(self):
        """Test that we actually load shipped configs"""
        args = Parser.parse_args(shlex.split("view file.json"))
        config_file_path = get_config_file_path(args)
        configs = load_configs(config_file_path)
        # user configs should not exist
        self.assertFalse(os.path.exists(os.path.expanduser("~/.sfftkrw/sffrw.conf")))
        self.assertEqual(configs['__TEMP_FILE'], './temp-annotated.json')
        self.assertEqual(configs['__TEMP_FILE_REF'], '@')

    def test_config_path(self):
        """Test that we can read configs from config path"""
        args = Parser.parse_args(shlex.split('view --config-path {} file.sff'.format(self.test_config_fn)))
        config_file_path = get_config_file_path(args)
        configs = load_configs(config_file_path)
        self.assertEqual(configs['HAPPY'], 'DAYS')

    def test_user_config(self):
        """Test that we can read user configs from ~/.sfftkrw/sffrw.conf"""
        # no user configs yet
        self.assertFalse(os.path.exists(os.path.expanduser("~/.sfftkrw/sffrw.conf")))
        # set a custom value to ensure it's present in user configs
        args = Parser.parse_args(shlex.split('config set --force NAME VALUE'))
        config_file_path = get_config_file_path(args)
        configs = load_configs(config_file_path)
        set_configs(args, configs)
        # now user configs should exist
        self.assertTrue(os.path.exists(os.path.expanduser("~/.sfftkrw/sffrw.conf")))
        args, configs = parse_args('view file.sff', use_shlex=True)
        self.assertEqual(configs['NAME'], 'VALUE')

    def test_precedence_config_path(self):
        """Test that config path takes precedence"""
        # set a custom value to ensure it's present in user configs
        args = Parser.parse_args(shlex.split('config set --force NAME VALUE'))
        config_file_path = get_config_file_path(args)
        configs = load_configs(config_file_path)
        set_configs(args, configs)
        args, configs = parse_args(
            'view --config-path {} --shipped-configs file.sff'.format(self.test_config_fn), use_shlex=True)
        self.assertEqual(configs['HAPPY'], 'DAYS')

    def test_precedence_shipped_configs(self):
        """Test that shipped configs, when specified, take precedence over user configs"""
        # set a custom value to ensure it's present in user configs
        args = Parser.parse_args(shlex.split('config set --force NAME VALUE'))
        config_file_path = get_config_file_path(args)
        configs = load_configs(config_file_path)
        set_configs(args, configs)
        args, configs = parse_args('view file.sff --shipped-configs', use_shlex=True)
        self.assertEqual(configs['__TEMP_FILE'], './temp-annotated.json')
        self.assertEqual(configs['__TEMP_FILE_REF'], '@')
        self.assertNotIn('NAME', configs)

    def test_get_configs(self):
        """Test that we can get a config by name"""
        args, configs = parse_args('config get __TEMP_FILE --config-path {}'.format(self.config_fn), use_shlex=True)
        self.assertTrue(get_configs(args, configs) == os.EX_OK)

    def test_get_all_configs(self):
        """Test that we can list all configs"""
        args, configs = parse_args('config get --all --config-path {}'.format(self.config_fn), use_shlex=True)
        self.assertTrue(get_configs(args, configs) == os.EX_OK)
        self.assertTrue(len(configs) > 0)

    def test_get_absent_configs(self):
        """Test that we are notified when a config is not found"""
        args, configs = parse_args('config get alsdjf;laksjflk --config-path {}'.format(self.config_fn), use_shlex=True)
        self.assertTrue(get_configs(args, configs) == 1)

    def test_set_configs(self):
        """Test that we can set configs"""
        args, configs_before = parse_args(
            'config set --force NAME VALUE --config-path {}'.format(self.config_fn), use_shlex=True)
        len_configs_before = len(configs_before)
        self.assertTrue(set_configs(args, configs_before) == 0)
        _, configs_after = parse_args('config get alsdjf;laksjflk --config-path {}'.format(self.config_fn),
                                      use_shlex=True)
        len_configs_after = len(configs_after)
        self.assertTrue(len_configs_before < len_configs_after)

    def test_set_new_configs(self):
        """Test that new configs will by default be written to user configs .i.e. ~/sfftkrw/sffrw.conf"""
        args, configs = parse_args('config set --force NAME VALUE', use_shlex=True)
        self.assertTrue(set_configs(args, configs) == os.EX_OK)
        _, configs = parse_args('config get --all', use_shlex=True)
        self.assertTrue('NAME' in configs)

    def test_set_force_configs(self):
        """Test that forcing works"""
        args, configs = parse_args('config set --force NAME VALUE', use_shlex=True)
        self.assertTrue(set_configs(args, configs) == os.EX_OK)
        self.assertTrue(configs['NAME'] == 'VALUE')
        args, configs_after = parse_args('config set --force NAME VALUE1', use_shlex=True)
        self.assertTrue(set_configs(args, configs_after) == os.EX_OK)
        self.assertTrue(configs_after['NAME'] == 'VALUE1')

    def test_del_configs(self):
        """Test that we can delete configs"""
        # first we get current configs
        args, configs = parse_args('config set --force NAME VALUE --config-path {}'.format(self.config_fn),
                                   use_shlex=True)
        # then we set an additional config
        self.assertTrue(set_configs(args, configs) == 0)
        # then we delete the config
        args, configs_before = parse_args(
            'config del --force NAME  --config-path {}'.format(self.config_fn), use_shlex=True)
        len_configs_before = len(configs_before)
        self.assertTrue(del_configs(args, configs_before) == 0)
        args, configs_after = parse_args('config get --all --config-path {}'.format(self.config_fn), use_shlex=True)
        len_configs_after = len(configs_after)
        self.assertTrue(len_configs_before > len_configs_after)

    def test_del_all_configs(self):
        """Test that we can delete all configs"""
        args, configs = parse_args('config del --force --all --config-path {}'.format(self.config_fn), use_shlex=True)
        print('args = ', args)
        self.assertTrue(del_configs(args, configs) == 0)
        _, configs = parse_args('config get --all --config-path {}'.format(self.config_fn), use_shlex=True)
        self.assertTrue(len(configs) == 0)

    def test_write_shipped_fails(self):
        """Test that we cannot save to shipped configs"""
        args, configs = parse_args(
            'config set --force NAME VALUE --config-path {}'.format(os.path.join(BASE_DIR, 'sffrw.conf')),
            use_shlex=True)
        self.assertTrue(set_configs(args, configs) == 1)


class TestCorePrintUtils(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
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
        cls.test_data_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        cls.test_sff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        cls.test_hff_file = os.path.join(TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')

    @classmethod
    def tearDownClass(cls):
        print("", file=sys.stderr)

    def test_default(self):
        """Test convert parser"""
        args, _ = parse_args('convert {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.subcommand, 'convert')
        self.assertEqual(args.from_file, self.test_data_file)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.top_level_only)
        self.assertIsNone(args.details)
        self.assertEqual(args.output, os.path.join(os.path.dirname(self.test_data_file), 'emd_1014.hff'))
        self.assertEqual(args.primary_descriptor, None)
        self.assertFalse(args.verbose)

    def test_config_path(self):
        """Test setting of arg config_path"""
        config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffrw.conf')
        args, _ = parse_args('convert --config-path {} {}'.format(config_fn, self.test_data_file), use_shlex=True)
        self.assertEqual(args.config_path, config_fn)

    def test_details(self):
        """Test convert parser with details"""
        args, _ = parse_args('convert -D "Some details" {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.details, 'Some details')

    def test_output_sff(self):
        """Test convert parser to .sff"""
        args, _ = parse_args('convert {} -o file.sff'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.sff')

    def test_output_hff(self):
        """Test convert parser to .hff"""
        args, _ = parse_args('convert {} -o file.hff'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.hff')

    def test_output_json(self):
        """Test convert parser to .json"""
        args, _ = parse_args('convert {} -o file.json'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.output, 'file.json')

    def test_hff_default_output_sff(self):
        """Test that converting an .hff with no args gives .sff"""
        args, _ = parse_args('convert {}'.format(self.test_hff_file), use_shlex=True)
        self.assertEqual(args.output, self.test_sff_file)

    def test_sff_default_output_hff(self):
        """Test that converting a .sff with no args gives .hff"""
        args, _ = parse_args('convert {}'.format(self.test_sff_file), use_shlex=True)
        self.assertEqual(args.output, self.test_hff_file)

    def test_primary_descriptor(self):
        """Test convert parser with primary_descriptor"""
        args, _ = parse_args('convert -R threeDVolume {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertEqual(args.primary_descriptor, 'threeDVolume')

    def test_wrong_primary_descriptor_fails(self):
        """Test that we have a check on primary descriptor values"""
        args, _ = parse_args('convert -R something {}'.format(self.test_data_file), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)

    def test_verbose(self):
        """Test convert parser with verbose"""
        args, _ = parse_args('convert -v {}'.format(self.test_data_file), use_shlex=True)
        # assertions
        self.assertTrue(args.verbose)


class TestCoreParserView(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sffrw.conf')
        print("view tests...", file=sys.stderr)

    @classmethod
    def tearDownClass(cls):
        print("", file=sys.stderr)

    def test_default(self):
        """Test view parser"""
        args, _ = parse_args('view file.sff', use_shlex=True)

        self.assertEqual(args.from_file, 'file.sff')
        self.assertFalse(args.version)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.show_chunks)

    def test_version(self):
        """Test view version"""
        args, _ = parse_args('view -V file.sff', use_shlex=True)

        self.assertTrue(args.version)

    def test_config_path(self):
        """Test setting of arg config_path"""
        config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffrw.conf')
        args, _ = parse_args('view --config-path {} file.sff'.format(config_fn), use_shlex=True)
        self.assertEqual(args.config_path, config_fn)

    def test_show_chunks_mod(self):
        """Test that we can view chunks"""
        args, _ = parse_args('view -C file.mod', use_shlex=True)
        self.assertTrue(args.show_chunks)

    def test_show_chunks_other_fails(self):
        """Test that show chunks only works for .mod files"""
        args, _ = parse_args('view -C file.sff', use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)


class TestCoreParserTests(Py23FixTestCase):
    def test_tests_default(self):
        """Test that tests can be launched"""
        args, _ = parse_args("tests all", use_shlex=True)
        self.assertEqual(args.subcommand, 'tests')
        self.assertCountEqual(args.tool, ['all'])

    def test_tests_one_tool(self):
        """Test that with any tool we get proper tool"""
        tool = random.choice(tool_list)
        args, _ = parse_args("tests {}".format(tool), use_shlex=True)
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
        args, _ = parse_args("tests {}".format(' '.join(tools)), use_shlex=True)
        self.assertCountEqual(args.tool, tools)

    def test_tool_fail(self):
        """Test that we catch a wrong tool"""
        args, _ = parse_args("tests wrong_tool_spec", use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)

    def test_tests_no_tool(self):
        """Test that with no tool we simply get usage info"""
        args, _ = parse_args("tests", use_shlex=True)
        self.assertEqual(args, os.EX_OK)

    def test_valid_verbosity(self):
        """Test valid verbosity"""
        args, _ = parse_args("tests all -v 0", use_shlex=True)
        self.assertEqual(args.verbosity, 0)
        args, _ = parse_args("tests all -v 1", use_shlex=True)
        self.assertEqual(args.verbosity, 1)
        args, _ = parse_args("tests all -v 2", use_shlex=True)
        self.assertEqual(args.verbosity, 2)
        args, _ = parse_args("tests all -v 3", use_shlex=True)
        self.assertEqual(args.verbosity, 3)

    def test_invalid_verbosity(self):
        """Test that verbosity is in [0,3]"""
        v1 = _random_integer(start=4)
        args, _ = parse_args("tests all -v {}".format(v1), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)
        v2 = -_random_integer(start=0)
        args, _ = parse_args("tests all -v {}".format(v2), use_shlex=True)
        self.assertEqual(args, os.EX_USAGE)


class TestCoreUtils(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        print("utils tests...", file=sys.stderr)

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
        with self.assertRaises(KeyError):
            utils.get_path(D, path)

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
        args, configs = parse_args(cmd, use_shlex=True)
        self.assertEqual(args.subcommand, 'view')
        self.assertEqual(args.from_file, 'file.sff')
        self.assertEqual(configs['__TEMP_FILE'], './temp-annotated.json')
        self.assertEqual(configs['__TEMP_FILE_REF'], '@')
