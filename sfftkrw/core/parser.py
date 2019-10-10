# -*- coding: utf-8 -*-
# parser.py
"""
parser.py
=========

A large number of functions in ``sfftk`` consume only two arguments: ``args``, which is the direct output of Python's
:py:class:`argparse.ArgumentParser` and a ``configs`` dictionary, which consists of all persistent configs. This
module includes both the parser object ``Parser`` as well as a :py:func:`sfftk.core.parser.parse_args` function
which does sanity checking of all command line arguments.
"""
from __future__ import print_function

import argparse
import os
import re
import sys
from copy import deepcopy

from . import _dict_iter_keys
from .print_tools import print_date
from ..core import _decode, _input

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
    prog='sff-rw', description="The EMDB-SFF Read/Write Toolkit (sfftk-rw)")
Parser.add_argument(
    '-V', '--version',
    action='store_true',
    default=False,
    help='show the sfftk-rw version string and the supported EMDB-SFF Read/Write version string',
)

subparsers = Parser.add_subparsers(
    title='Tools',
    dest='subcommand',
    description='The EMDB-SFF Read/Write Toolkit (sfftk-rw) provides the following tools:',
    metavar="EMDB-SFF tools"
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
        'help': "output file format; valid options are: {} [default: sff]".format(
            ", ".join(map(lambda x: "{} ({})".format(x[0], x[1]), FORMAT_LIST))
        ),
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
config_path = {
    'args': ['-p', '--config-path'],
    'kwargs': {
        'help': "path to configs file"
    }
}
primary_descriptor = {
    'args': ['-R', '--primary-descriptor'],
    'kwargs': {
        'help': "populates the <primaryDescriptor>...</primaryDescriptor> to this value [valid values:  threeDVolume, meshList, shapePrimitiveList]"
    }
}
segment_name = {
    'args': ['-s', '--segment-name'],
    'kwargs': {
        'help': "the name of the segment"
    }
}
shipped_configs = {
    'args': ['-b', '--shipped-configs'],
    'kwargs': {
        'default': False,
        'action': 'store_true',
        'help': 'use shipped configs only if config path and user configs fail [default: False]'
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
    'convert', description="Perform conversions to EMDB-SFF", help="converts from/to EMDB-SFF")
convert_parser.add_argument('from_file', help="file to convert from")
add_args(convert_parser, config_path)
add_args(convert_parser, shipped_configs)
convert_parser.add_argument('-t', '--top-level-only', default=False,
                            action='store_true', help="convert only the top-level segments [default: False]")
# convert_parser.add_argument('-M', '--contours-to-mesh', default=False, action='store_true', help="convert an 'contourList' EMDB-SFF to a 'meshList' EMDB-SFF")
convert_parser.add_argument(*details['args'], **details['kwargs'])
convert_parser.add_argument(
    *primary_descriptor['args'], **primary_descriptor['kwargs'])
convert_parser.add_argument(*verbose['args'], **verbose['kwargs'])
# convert_parser.add_argument('-s', '--sub-tomogram-average', nargs=2,
#                             help="convert a subtomogram average into an EMDB-SFF file; two arguments are required: the "
#                                  "table file and volume file (in that order)")
group = convert_parser.add_mutually_exclusive_group()
group.add_argument(*output['args'], **output['kwargs'])
group.add_argument(*format_['args'], **format_['kwargs'])

# =========================================================================
# config subparser
# =========================================================================
config_parser = subparsers.add_parser(
    'config',
    description="Configuration utility",
    help="manage sfftk configs"
)
config_subparsers = config_parser.add_subparsers(
    title='sfftk configurations',
    dest='config_subcommand',
    description='Persistent configurations utility',
    metavar='Commands:'
)

# =============================================================================
# config: get
# =============================================================================
get_config_parser = config_subparsers.add_parser(
    'get',
    description='Get the value of a single configuration parameter',
    help='get single sfftk config'
)
get_config_parser.add_argument(
    'name',
    nargs="?",
    default=None,
    help="the name of the argument to retrieve",
)
add_args(get_config_parser, config_path)
add_args(get_config_parser, shipped_configs)
get_config_parser.add_argument(
    '-a', '--all',
    action='store_true',
    default=False,
    help='get all configs'
)
add_args(get_config_parser, verbose)

# =============================================================================
# config: set
# =============================================================================
set_config_parser = config_subparsers.add_parser(
    'set',
    description='Set the value of a single configuration parameter',
    help='set single sfftk config'
)
set_config_parser.add_argument(
    'name', help="the name of the argument to set",
)
set_config_parser.add_argument(
    'value', help="the value of the argument to set",
)
add_args(set_config_parser, config_path)
add_args(set_config_parser, shipped_configs)
add_args(set_config_parser, verbose)
set_config_parser.add_argument(
    '-f', '--force',
    action='store_true',
    default=False,
    help='force overwriting of an existing config; do not ask to confirm [default: False]'
)

# =============================================================================
# config: del
# =============================================================================
del_config_parser = config_subparsers.add_parser(
    'del',
    description='Delete the named configuration parameter',
    help='delete single sfftk config'
)
del_config_parser.add_argument(
    'name',
    nargs='?',
    default=None,
    help="the name of the argument to be deleted"
)
add_args(del_config_parser, config_path)
add_args(del_config_parser, shipped_configs)
del_config_parser.add_argument(
    '-a', '--all',
    action='store_true',
    default=False,
    help='delete all configs (asks the user to confirm before deleting) [default: False]'
)
del_config_parser.add_argument(
    '-f', '--force',
    action='store_true',
    default=False,
    help='force deletion; do not ask to confirm deletion [default: False]'
)
add_args(del_config_parser, verbose)

# =========================================================================
# view subparser
# =========================================================================
view_parser = subparsers.add_parser(
    'view', description="View a summary of an SFF file", help="view file summary")
view_parser.add_argument('from_file', help="any SFF file")
add_args(view_parser, config_path)
add_args(view_parser, shipped_configs)
view_parser.add_argument(
    '-V', '--version', action='store_true', help="show SFF format version")
view_parser.add_argument('-C', '--show-chunks', action='store_true',
                         help="show sequence of chunks in IMOD file; only works with IMOD model files (.mod) [default: False]")
view_parser.add_argument(*verbose['args'], **verbose['kwargs'])

# get the full list of tools from the Parser object
# tool_list = Parser._actions[1].choices.keys()
# print(tool_list)
tool_list = ['all', 'core', 'formats', 'notes', 'readers', 'schema', 'main']

# tests
test_help = "one or none of the following: {}".format(", ".join(tool_list))
tests_parser = subparsers.add_parser(
    'tests', description="Run unit tests", help="run unit tests")
tests_parser.add_argument('tool', nargs='+', help=test_help)
add_args(tests_parser, config_path)
add_args(tests_parser, shipped_configs)
tests_parser.add_argument('-v', '--verbosity', default=1, type=int,
                          help="set verbosity; valid values: %s [default: 0]" % ", ".join(map(str, verbosity_range)))


def check_multi_file_formats(file_names):
    """Check file names for file formats

    When working with multifile segmentations, this function checks that all files are consistent

    :param list file_names: a list of file names
    :return: a tuple consisting of whether or not the set of file formats if valid, the set of file formats observed
        and the set of invalid file formats
    :rtype: tuple[bool, set, set]
    """
    is_valid_format = True
    file_formats = set()
    invalid_formats = set()
    for fn in file_names:
        ff = fn.split('.')[-1].lower()
        if ff in multi_file_formats:
            file_formats.add(ff)
        else:
            invalid_formats.add(ff)
            is_valid_format = False
    if len(file_formats) == 1:
        file_format = file_formats.pop()
    else:
        file_format = None
        invalid_formats.union(file_formats)
    return is_valid_format, file_format, invalid_formats


# parser function
def parse_args(_args, use_shlex=False):
    """
    Parse and check command-line arguments and also return configs.

    This function does all the heavy lifting in ensuring that commandline
    arguments are properly formatted and checked for sanity. It also 
    extracts configs from the config files.

    In this way command handlers (defined in ``sfftk/sff.py`` e.g. ``handle_convert(...)``)
    assume correct argument values and can concentrate on functionality.

    :param list _args: list of arguments (``use_shlex=False``); string of arguments (``use_shlex=True``)
    :type _args: list or str
    :param bool use_shlex: treat ``_args`` as a string instead for parsing using ``shlex`` lib
    :return: parsed arguments
    :rtype: tuple[:py:class:`argparse.Namespace`, :py:class:`sfftk.core.configs.Configs`]
    """
    if use_shlex:  # if we treat _args as a command string for shlex to process
        try:
            assert isinstance(_args, str)
        except AssertionError:
            return os.EX_USAGE, None
        import shlex
        _args = shlex.split(_args)
    # if we have no subcommands then show the available tools
    if len(_args) == 0:
        Parser.print_help()
        return os.EX_OK, None
    # if we only have a subcommand then show that subcommand's help
    elif len(_args) == 1:
        # print(_args[0])
        # print(Parser._actions[2].choices)
        # if _args[0] == 'tests':
        #     pass
        if _args[0] == '-V' or _args[0] == '--version':
            from .. import SFFTKRW_VERSION
            print_date("sfftk-rw version: {}".format(SFFTKRW_VERSION))
            return os.EX_OK, None
        # anytime a new argument is added to the base parser subparsers are bumped down in index
        elif _args[0] in _dict_iter_keys(Parser._actions[2].choices):
            exec('{}_parser.print_help()'.format(_args[0]))
            return os.EX_OK, None
    # if we have 'notes' as the subcommand and a sub-subcommand show the
    # options for that sub-subcommand
    elif len(_args) == 2:
        if _args[0] == 'config':
            if _args[1] in _dict_iter_keys(Parser._actions[2].choices['config']._actions[1].choices):
                exec('{}_config_parser.print_help()'.format(_args[1]))
                return os.EX_OK, None
    # parse arguments
    args = Parser.parse_args(_args)
    from .configs import get_config_file_path
    # get the file to use for configs given args
    config_file_path = get_config_file_path(args)
    if config_file_path is None:
        print_date("Invalid destination for configs. Omit --shipped-configs to write to user configs.")
        return None, None
    from .configs import load_configs
    # now get configs to use
    configs = load_configs(config_file_path)

    # check values
    # config
    if args.subcommand == 'config':
        if args.verbose:
            print_date("Reading configs from {}...".format(config_file_path))
        # handle config-specific argument modifications here
        if args.config_subcommand == 'del':
            if args.name not in configs and not args.all:
                print_date("Missing config with name '{}'. Aborting...".format(args.name))
                return None, configs
            # if force pass
            if not args.force:
                default_choice = 'n'
                # get user choice
                user_choice = _input("Are you sure you want to delete config '{}' [y/N]? ".format(
                    args.name)).lower()
                if user_choice == '':
                    choice = default_choice
                elif user_choice == 'n' or user_choice == 'N':
                    choice = 'n'
                elif user_choice == 'y' or user_choice == 'Y':
                    choice = 'y'
                else:
                    print_date("Invalid choice: '{}'")
                    return os.EX_USAGE, configs
                # act on user choice
                if choice == 'n':
                    print_date("You have opted to cancel deletion of '{}'".format(args.name))
                    return os.EX_USAGE, configs
                elif choice == 'y':
                    pass
        elif args.config_subcommand == 'set':
            if args.name in configs:
                # if force pass
                if not args.force:
                    default_choice = 'n'
                    # get user choice
                    user_choice = _input("Are you sure you want to overwrite config '{}={}' [y/N]? ".format(
                        args.name, configs[args.name])).lower()
                    if user_choice == '':
                        choice = default_choice
                    elif user_choice == 'n' or user_choice == 'N':
                        choice = 'n'
                    elif user_choice == 'y' or user_choice == 'Y':
                        choice = 'y'
                    else:
                        print_date("Invalid choice: '{}'")
                        return os.EX_USAGE, configs
                    # act on user choice
                    if choice == 'n':
                        print_date("You have opted to cancel overwriting of '{}'".format(args.name))
                        return None, configs
                    elif choice == 'y':
                        pass
    # view
    elif args.subcommand == 'view':
        if args.show_chunks:
            if not re.match(r".*\.mod$", args.from_file, re.IGNORECASE):
                print_date("Invalid file type to view chunks. Only works with IMOD files")
                return os.EX_USAGE, configs
    # convert
    elif args.subcommand == 'convert':
        # convert details to unicode
        if args.details is not None:
            args.details = _decode(args.details, 'utf-8')
        # set the output file
        if args.output is None:
            from_file = args.from_file
            dirname = os.path.dirname(from_file)
            if args.format:
                try:
                    assert args.format in map(lambda x: x[0], FORMAT_LIST)
                except AssertionError:
                    print_date("Invalid output format: {}; valid values are: {}".format(
                        args.format, ", ".join(map(lambda x: x[0], FORMAT_LIST))))
                    return os.EX_USAGE, configs
                fn = ".".join(os.path.basename(from_file).split(
                    '.')[:-1]) + '.{}'.format(args.format)
                args.__setattr__('output', os.path.join(dirname, fn))
            # convert file.sff to file.hff
            elif re.match(r'.*\.sff$', from_file):
                fn = ".".join(
                    os.path.basename(from_file).split('.')[:-1]) + '.hff'
                args.__setattr__('output', os.path.join(dirname, fn))
            # convert file.hff to file.sff
            elif re.match(r'.*\.hff$', from_file):
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
                    'threeDVolume', 'meshList', 'shapePrimitive']
            except:
                if args.verbose:
                    print_date(
                        "Invalid value for primary descriptor: {}".format(args.primary_descriptor))
                return os.EX_USAGE, configs
            if args.verbose:
                print_date(
                    "Trying to set primary descriptor to {}".format(args.primary_descriptor))
    # tests
    elif args.subcommand == 'tests':
        # check if we have a temp-annotated file and complain then die if one exists
        if os.path.exists(configs['__TEMP_FILE']):
            print_date("Unable to run tests with {} in current path ({})".format(configs['__TEMP_FILE'],
                                                                                 os.path.abspath(__file__)))
            print_date("Run 'sff notes save <file.sff>' or 'sff notes trash @' before proceeding.")
            return os.EX_USAGE, configs
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
                return os.EX_USAGE, configs
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
                return os.EX_USAGE, configs

    return args, configs
