#!/usr/local/bin/python2.7
# encoding: utf-8
# sffrw.py
"""
sfftkrw.sffrw -- Toolkit for reading and writing EMDB-SFF files

sfftkrw.sffrw is the main entry point for performing command-line operations.
"""
from __future__ import division, print_function

import importlib
import os
import re
import sys

from .core import _decode
from .core.print_tools import print_date
from .core.utils import get_version

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = '2017-02-15'
__updated__ = '2018-02-23'


def handle_convert(args):  # @UnusedVariable
    """
    Handle `convert` subcommand

    :param args: parsed arguments
    :type args: `argparse.Namespace`
    :param configs: configurations object
    :type configs: ``sfftk.core.configs.Configs``
    :return int status: status
    """
    schema_version = get_version(args.from_file)
    if args.verbose:
        print_date(u"Using schema version {}".format(schema_version))
    adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
        schema_version=schema_version.replace('.', '_')
    )
    adapter = importlib.import_module(adapter_name)
    if re.match(r'.*\.(sff|xml)$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFF (XML) file {}".format(args.from_file))
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
    elif re.match(r'.*\.(hff|h5|hdf5)$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFF (HDF5) file {}".format(args.from_file))
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
        if args.verbose:
            print_date("Created SFFSegmentation object")
    elif re.match(r'.*\.json$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFF (JSON) file {}".format(args.from_file))
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
        if args.verbose:
            print_date("Created SFFSegmentation object")
    else:
        raise ValueError("Unknown file type %s" % args.from_file)
    if args.primary_descriptor is not None:
        seg.primary_descriptor = args.primary_descriptor
    if args.details is not None:
        seg.details = args.details
    # export as args.format
    if args.verbose:
        print_date("Exporting to {}".format(args.output))
    # perform actual export
    status = seg.export(args.output, args)
    if args.verbose:
        if status == os.EX_OK:
            print_date("Done")
        else:
            print_date("Error")
    return status


def handle_view(args):  # @UnusedVariable
    """Handle `view` subcommand
    
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    :param configs: configurations object
    :type configs: ``sfftk.core.configs.Configs``
    :return int status: status
    """
    schema_version = get_version(args.from_file)
    if args.verbose:
        print_date(u"Using schema version {}".format(schema_version))
    adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
        schema_version=schema_version.replace('.', '_')
    )
    adapter = importlib.import_module(adapter_name)
    if re.match(r'.*\.(sff|xml)$', args.from_file, re.IGNORECASE):
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
        print("*" * 50)
        print(u"EMDB-SFF Segmentation version {}".format(_decode(seg.version, u'utf-8')))
        print(u"Segmentation name: {}".format(_decode(seg.name, u'utf-8')))
        print(u"Format: XML")
        print(u"Primary descriptor: {}".format(_decode(seg.primary_descriptor, u'utf-8')))
        print(u"No. of segments: {}".format(len(seg.segments)))
        print(u"*" * 50)
    elif re.match(r'.*\.(hff|h5|hdf5)$', args.from_file, re.IGNORECASE):
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
        print("*" * 50)
        print(u"EMDB-SFF Segmentation version {}".format(_decode(seg.version, u'utf-8')))
        print(u"Segmentation name: {}".format(_decode(seg.name, u'utf-8')))
        print(u"Format: HDF5")
        print(u"Primary descriptor: {}".format(_decode(seg.primary_descriptor, u'utf-8')))
        print(u"No. of segments: {}".format(len(seg.segments)))
        print(u"*" * 50)
    elif re.match(r'.*\.json$', args.from_file, re.IGNORECASE):
        seg = adapter.SFFSegmentation.from_file(args.from_file, args)
        print("*" * 50)
        print(u"EMDB-SFF Segmentation version {}".format(_decode(seg.version, u'utf-8')))
        print(u"Segmentation name: {}".format(_decode(seg.name, u'utf-8')))
        print(u"Format: JSON")
        print(u"Primary descriptor: {}".format(_decode(seg.primary_descriptor, u'utf-8')))
        print(u"No. of segments: {}".format(len(seg.segments)))
        print(u"*" * 50)
    else:
        print(u"Not implemented view for files of type .{}".format(args.from_file.split('.')[-1]), file=sys.stderr)
    return os.EX_OK


def _module_test_runner(mod, args):
    """Module test runner 
    
    :param module mod: the module where the tests will be found
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    import unittest
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    print_date(u"Found {} test cases in the suite...".format(suite.countTestCases()))
    if not args.dry_run:
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
    return os.EX_OK


def _testcase_test_runner(tc, args):
    """TestCase test runner
    
    :param tc: test case
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(tc)
    print_date(u"Found {} test cases in the suite...".format(suite.countTestCases()))
    if not args.dry_run:
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
    return os.EX_OK


def _discover_test_runner(path, args, top_level_dir=None):
    """Test runner that looks for tests in *path*
    
    :param str path: path to search for tests
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    import unittest
    suite = unittest.TestLoader().discover(path, top_level_dir=top_level_dir)
    print_date(u"Found {} test cases in the suite...".format(suite.countTestCases()))
    if not args.dry_run:
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
    return os.EX_OK


def handle_tests(args):
    """Handle `test` subcommand
    
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    :param configs: configurations object
    :type configs: ``sfftk.core.configs.Configs``
    :return int status: status
    """
    if 'all' in args.tool:
        from .unittests import test_main
        _module_test_runner(test_main, args)
        _discover_test_runner("sfftkrw.unittests", args)
    else:
        if 'main' in args.tool:
            from .unittests import test_main
            _module_test_runner(test_main, args)
        if 'core' in args.tool:
            from .unittests import test_core
            _module_test_runner(test_core, args)
        if 'schema' in args.tool:
            from .unittests import test_base
            from . import SUPPORTED_EMDB_SFF_VERSIONS
            _module_test_runner(test_base, args)
            # schema tests are only run for the current data model
            for schema_version in SUPPORTED_EMDB_SFF_VERSIONS:
                test_adapter_name = 'sfftkrw.unittests.test_adapter_v{schema_version}'.format(
                    schema_version=schema_version.replace('.', '_')
                )
                test_adapter = importlib.import_module(test_adapter_name)
                _module_test_runner(test_adapter, args)
    return os.EX_OK


def main():
    try:
        from .core.parser import parse_args
        args = parse_args(sys.argv[1:])
        # missing args
        if args == os.EX_USAGE:
            return os.EX_USAGE
        elif args == os.EX_OK:  # e.g. show version has no error but has no handler either
            return os.EX_OK
        # subcommands
        if args.subcommand == 'convert':
            return handle_convert(args)
        elif args.subcommand == "view":
            return handle_view(args)
        elif args.subcommand == "tests":
            return handle_tests(args)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return os.EX_OK
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
