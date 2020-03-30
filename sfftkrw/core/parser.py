# -*- coding: utf-8 -*-
# parser.py
"""
parser.py
=========


"""
from __future__ import print_function

import argparse
import os
import re

from . import _dict_iter_keys
from .print_tools import print_date
from .. import SFFTKRW_VERSION, SFFTKRW_ENTRY_POINT, SUPPORTED_EMDB_SFF_VERSIONS
from ..core import _decode, _basestring

__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'
__updated__ = '2018-02-14'

verbosity_range = list(range(4))
multi_file_formats = ['stl', 'map', 'mrc', 'rec']
prepable_file_formats = ['mrc', 'map', 'rec']
rescalable_file_formats = ['stl']


def add_args(parser, the_arg):
    """Convenience function to add ``the_arg`` to the ``parser``.

    This relies on the argument being structured as a dictionary with the keys 
    ``args`` for positional arguments and ``kwargs`` for the keyword
    arguments. The value of doing this is that arguments that are reused
    in several parsers can be referred to by a variable instead of being 
    redefined. 

    Usage::

        >>> my_arg = {'arg': ['-x'], 'kwargs': {'help': 'help'}}
        >>> this_parser = argparse.ArgumentParser()
        >>> add_args(this_parser, my_arg)

    :param parser: the parser to be modified
    :type parser: :py:class:`argparse.ArgumentParser`
    :param dict the_arg: the argument specified as a dict with keys ``args`` and ``kwargs``
    :return: a modified parser object
    :rtype: :py:class:`argparse.ArgumentParser`
    """
    return parser.add_argument(*the_arg['args'], **the_arg['kwargs'])


Parser = argparse.ArgumentParser(
    prog=SFFTKRW_ENTRY_POINT, description="The EMDB-SFF Read/Write Toolkit (sfftk-rw)")
Parser.add_argument(
    '-V', '--version',
    action='store_true',
    default=False,
    help='show the sfftk-rw version string and the supported EMDB-SFF Read/Write version string',
)

subparsers = Parser.add_subparsers(
    title='Tools',
    dest='subcommand',
    description='The EMDB-SFF Read/Write Toolkit ({}) provides the following tools:'.format(SFFTKRW_ENTRY_POINT),
    metavar="EMDB-SFF Read/Write Tools"
)

# =========================================================================
# common arguments
# =========================================================================
sff_file = {
    'args': ['sff_file'],
    'kwargs': {
        'help': 'path (rel/abs) to an EMDB-SFF file',
    }
}
details = {
    'args': ['-D', '--details'],
    'kwargs': {
        'help': "populates <details>...</details> in the XML file"
    }
}

FORMAT_LIST = [
    ('sff', 'XML'),
    ('hff', 'HDF5'),
    ('json', 'JSON'),
]
format_ = {
    'args': ['-f', '--format'],
    'kwargs': {
        # 'default': 'sff',
        'help': "output file format; valid options are: {formats} [default: {default}]".format(
            default=FORMAT_LIST[0][0],
            formats=", ".join(map(lambda x: "{} ({})".format(x[0], x[1]), FORMAT_LIST))
        ),
    }
}
exclude_geometry = {
    'args': ['-x', '--exclude-geometry'],
    'kwargs': {
        'default': False,
        'action': 'store_true',
        'help': 'do not include the geometry in the conversion; geometry is included by default [default: False]',
    }
}
header = {
    'args': ['-H', '--header'],
    'kwargs': {
        'default': False,
        'action': 'store_true',
        'help': 'show EMDB-SFF header (global) attributes [default: False]'
    }
}
segment_id = {
    'args': ['-i', '--segment-id'],
    'kwargs': {
        'help': 'refer to a segment by its ID'
    }
}
name = {
    'args': ['-N', '--name'],
    'kwargs': {
        'help': "the segmentation name"
    }
}
output = {
    'args': ['-o', '--output'],
    'kwargs': {
        'default': None,
        'help': "file to convert to; the extension (.sff, .hff, .json) determines the output format [default: None]"
    }
}
primary_descriptor = {
    'args': ['-R', '--primary-descriptor'],
    'kwargs': {
        'help': "populates the <primary_descriptor>...</primary_descriptor> to this value [valid values:  three_d_volume, mesh_list, shape_primitive_list]"
    }
}
segment_name = {
    'args': ['-s', '--segment-name'],
    'kwargs': {
        'help': "the name of the segment"
    }
}
json_sort = {
    'args': ['--json-sort'],
    'kwargs': {
        'default': False,
        'action': 'store_true',
        'help': "output JSON sorted lexicographically [default: False]"
    }
}
json_indent = {
    'args': ['--json-indent'],
    'kwargs': {
        'type': int,
        'default': 2,
        'help': "size in spaces of the JSON indent [default: 2]"
    }
}
verbose = {
    'args': ['-v', '--verbose'],
    'kwargs': {
        'action': 'store_true',
        'default': False,
        'help': "verbose output"
    },
}

# =========================================================================
# convert subparser
# =========================================================================
convert_parser = subparsers.add_parser(
    'convert', description="Perform EMDB-SFF file format interconversions", help="converts between EMDB-SFF formats")
convert_parser.add_argument('from_file', nargs='*', help="file to convert from")
convert_parser.add_argument(*details['args'], **details['kwargs'])
convert_parser.add_argument(
    *primary_descriptor['args'], **primary_descriptor['kwargs'])
convert_parser.add_argument(*verbose['args'], **verbose['kwargs'])
add_args(convert_parser, exclude_geometry)
add_args(convert_parser, json_indent)
add_args(convert_parser, json_sort)
group = convert_parser.add_mutually_exclusive_group()
group.add_argument(*output['args'], **output['kwargs'])
group.add_argument(*format_['args'], **format_['kwargs'])

# =========================================================================
# view subparser
# =========================================================================
view_parser = subparsers.add_parser(
    'view', description="View a summary of an SFF file", help="view file summary")
view_parser.add_argument('from_file', help="any SFF file")
view_parser.add_argument(
    '--sff-version', action='store_true', help="show SFF format version")
view_parser.add_argument(*verbose['args'], **verbose['kwargs'])

# get the full list of tools from the Parser object
tool_list = ['all', 'core', 'schema', 'main']

# tests
test_help = "one or none of the following: {}".format(", ".join(tool_list))
tests_parser = subparsers.add_parser(
    'tests', description="Run unit tests", help="run unit tests")
tests_parser.add_argument('tool', nargs='+', help=test_help)
tests_parser.add_argument('-v', '--verbosity', default=1, type=int,
                          help="set verbosity; valid values: %s [default: 0]" % ", ".join(map(str, verbosity_range)))

tests_parser.add_argument('--dry-run', default=False, action='store_true',
                          help='do not run tests [default: False]')


# parser function
def parse_args(_args, use_shlex=False):
    """
    Parse and check command-line arguments.

    This function does all the heavy lifting in ensuring that commandline
    arguments are properly formatted and checked for sanity.

    In this way command handlers (defined in ``sfftk/sff.py`` e.g. ``handle_convert(...)``)
    assume correct argument values and can concentrate on functionality.

    :param list _args: list of arguments (``use_shlex=False``); string of arguments (``use_shlex=True``)
    :type _args: list or str or unicode
    :param bool use_shlex: treat ``_args`` as a string instead for parsing using ``shlex`` lib
    :return: parsed arguments
    :rtype: :py:class:`argparse.Namespace`
    """
    if use_shlex:  # if we treat _args as a command string for shlex to process
        try:
            assert isinstance(_args, _basestring)
        except AssertionError:
            return os.EX_USAGE
        import shlex
        _args = shlex.split(_args)
    # if we have no subcommands then show the available tools
    if len(_args) == 0:
        Parser.print_help()
        return os.EX_OK
    # if we only have a subcommand then show that subcommand's help
    elif len(_args) == 1:
        # print(_args[0])
        # _print(Parser._actions)
        # if _args[0] == 'tests':
        #     pass
        if _args[0] == '-V' or _args[0] == '--version':
            print_date(
                "sfftk-rw version: {} for EMDB-SFF {}".format(SFFTKRW_VERSION, ', '.join(SUPPORTED_EMDB_SFF_VERSIONS)))
            return os.EX_OK
        # anytime a new argument is added to the base parser subparsers are bumped down in index
        elif _args[0] in _dict_iter_keys(Parser._actions[2].choices):
            exec('{}_parser.print_help()'.format(_args[0]))
            return os.EX_OK
    # parse arguments
    args = Parser.parse_args(_args)

    # check values
    # view
    if args.subcommand == 'view':
        pass # no view-specific checks yet
    # convert
    elif args.subcommand == 'convert':
        # we only use the first file in sfftk-rw; sfftk may use more than one file
        args.from_file = args.from_file[0]
        # convert details to unicode
        if args.details is not None:
            args.details = _decode(args.details, 'utf-8')
        # set the output file
        if args.output is None:
            from_file = args.from_file
            dirname = os.path.dirname(from_file)
            if args.format:
                try:
                    assert args.format in list(map(lambda x: x[0], FORMAT_LIST))
                except AssertionError:
                    print_date("Invalid output format: {invalid}; valid values are: {formats}".format(
                        invalid=args.format,
                        formats=", ".join(map(lambda x: x[0], FORMAT_LIST)))
                    )
                    return os.EX_USAGE
                fn = ".".join(os.path.basename(from_file).split(
                    '.')[:-1]) + '.{}'.format(args.format)
                args.__setattr__('output', os.path.join(dirname, fn))
            # convert file.sff to file.hff
            elif re.match(r'.*\.(sff|xml)$', from_file):
                fn = ".".join(
                    os.path.basename(from_file).split('.')[:-1]) + '.hff'
                args.__setattr__('output', os.path.join(dirname, fn))
            # convert file.hff to file.sff
            elif re.match(r'.*\.(hff|h5|hdf5)$', from_file):
                fn = ".".join(
                    os.path.basename(from_file).split('.')[:-1]) + '.sff'
                args.__setattr__('output', os.path.join(dirname, fn))
            else:
                fn = ".".join(
                    os.path.basename(from_file).split('.')[:-1]) + '.sff'
                args.__setattr__('output', os.path.join(dirname, fn))
            if args.verbose:
                print_date("Setting output file to {}".format(args.output))

        # ensure valid primary_descriptor
        if args.primary_descriptor:
            try:
                assert args.primary_descriptor in [
                    u'threeDVolume', u'meshList', u'shapePrimitiveList',
                    u'three_d_volume', u'mesh_list', u'shape_primitive_list',
                ]
            except AssertionError:
                print_date(
                        "Invalid value for primary descriptor: {}".format(args.primary_descriptor))
                return os.EX_USAGE
            if args.verbose:
                print_date(
                    "Trying to set primary descriptor to {}".format(args.primary_descriptor))

        # report on geometry
        if args.exclude_geometry and (args.format == u'json' or re.match(r'.*\.(json)$', args.output, re.IGNORECASE)):
            print_date("Excluding geometry for JSON")

        # validate indent for json
        if args.format == u'json' or re.match(r'.*\.(json)$', args.output, re.IGNORECASE):
            try:
                assert args.json_indent >= 0
            except AssertionError:
                print_date("Invalid value for --json-indent: {}".format(args.json_indent))
                return os.EX_USAGE
            if args.verbose:
                print_date("Indenting JSON with indent={}".format(args.json_indent))

            if args.json_sort and args.verbose:
                print_date("JSON keys will be sorted lexicographically")

    # tests
    elif args.subcommand == 'tests':
        # normalise tool list
        # if 'all' is specified together with others then it should simply be 'all'
        if 'all' in args.tool:
            args.tool = ['all']
        # if isinstance(args.tool, list):
        for tool in args.tool:
            try:
                assert tool in tool_list
            except AssertionError:
                print_date(
                    "Unknown tool: {}; Available tools for test: {}".format(tool, ", ".join(tool_list))
                )
                return os.EX_USAGE
        if args.verbosity:
            try:
                assert args.verbosity in range(4)
            except:
                print_date(
                    "Verbosity should be in {}-{}: {} given".format(
                        verbosity_range[0],
                        verbosity_range[-1],
                        args.verbosity
                    )
                )
                return os.EX_USAGE

    return args
