#!/usr/local/bin/python2.7
# encoding: utf-8
# sffrw.py
"""
sfftkrw.sff -- Toolkit to handle operations for EMDB-SFF files

sfftkrw.sff is the main entry point for performing command-line operations.
"""
from __future__ import division, print_function

import os
import re
import sys

from . import schema
from .core.print_tools import print_date

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
    if re.match(r'.*\.sff$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFf (XML) file {}".format(args.from_file))
        seg = schema.SFFSegmentation(args.from_file)
    elif re.match(r'.*\.hff$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFF (HDF5) file {}".format(args.from_file))
        seg = schema.SFFSegmentation(args.from_file)
        if args.verbose:
            print_date("Created SFFSegmentation object")
    elif re.match(r'.*\.json$', args.from_file, re.IGNORECASE):
        if args.verbose:
            print_date("Converting from EMDB-SFF (JSON) file {}".format(args.from_file))
        seg = schema.SFFSegmentation(args.from_file)
        if args.verbose:
            print_date("Created SFFSegmentation object")
    else:
        raise ValueError("Unknown file type %s" % args.from_file)
    if args.primary_descriptor is not None:
        seg.primaryDescriptor = args.primary_descriptor
    if args.details is not None:
        seg.details = args.details
    # export as args.format
    if args.verbose:
        print_date("Exporting to {}".format(args.output))
    # perform actual export
    status = seg.export(args.output)
    if args.verbose:
        print_date("Done")
    return status


def handle_view(args):  # @UnusedVariable
    """Handle `view` subcommand
    
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    :param configs: configurations object
    :type configs: ``sfftk.core.configs.Configs``
    :return int status: status
    """
    if re.match(r'.*\.sff$', args.from_file, re.IGNORECASE):
        seg = schema.SFFSegmentation.from_file(args.from_file)
        print("*" * 50)
        print("EMDB-SFF Segmentation version {}".format(seg.version))
        print("Segmentation name: {}".format(seg.name))
        print("Format: XML")
        print("Primary descriptor: {}".format(seg.primary_descriptor))
        print("No. of segments: {}".format(len(seg.segments)))
        print("*" * 50)
    elif re.match(r'.*\.hff$', args.from_file, re.IGNORECASE):
        seg = schema.SFFSegmentation.from_file(args.from_file)
        print("*" * 50)
        print("EMDB-SFF Segmentation version {}".format(seg.version))
        print("Segmentation name: {}".format(seg.name))
        print("Format: HDF5")
        print("Primary descriptor: {}".format(seg.primary_descriptor))
        print("No. of segments: {}".format(len(seg.segments)))
        print("*" * 50)
    elif re.match(r'.*\.json$', args.from_file, re.IGNORECASE):
        seg = schema.SFFSegmentation.from_file(args.from_file)
        print("*" * 50)
        print("EMDB-SFF Segmentation version {}".format(seg.version))
        print("Segmentation name: {}".format(seg.name))
        print("Format: JSON")
        print("Primary descriptor: {}".format(seg.primary_descriptor))
        print("No. of segments: {}".format(len(seg.segments)))
        print("*" * 50)
    else:
        print("Not implemented view for files of type .{}".format(args.from_file.split('.')[-1]), file=sys.stderr)
    return os.EX_OK


def _module_test_runner(mod, args):
    """Module test runner 
    
    :param module mod: the module where the tests will be found
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    import unittest
    suite = unittest.TestLoader().loadTestsFromModule(mod)
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
            from .unittests import test_base, test_adapter
            _module_test_runner(test_base, args)
            _module_test_runner(test_adapter, args)
        if 'formats' in args.tool:
            from .unittests import test_formats
            _module_test_runner(test_formats, args)
        if 'readers' in args.tool:
            from .unittests import test_readers
            _module_test_runner(test_readers, args)
        if 'notes' in args.tool:
            from .unittests import test_notes
            _module_test_runner(test_notes, args)
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
        if args.subcommand == 'prep':
            return handle_prep(args)
        elif args.subcommand == 'convert':
            return handle_convert(args)
        elif args.subcommand == 'notes':
            return handle_notes(args)
        elif args.subcommand == "view":
            return handle_view(args)
        elif args.subcommand == "config":
            return handle_config(args)
        elif args.subcommand == "tests":
            return handle_tests(args)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return os.EX_OK
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
