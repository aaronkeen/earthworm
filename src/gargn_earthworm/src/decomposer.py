# File name: decomposer.py
# Author: Nupur Garg
# Date created: 12/25/2016
# Python Version: 3.5


from __future__ import print_function
import argparse
import ast
import sys
import textwrap
import json

from .globals import *
from .error import *
from .slice import Slice
from .generatecfg import CFGGenerator
from .config import Config
from .linter import get_linter_suggestions


_LEN_PROGRESS_BAR = 40
_DEFAULT_JSON_FILE = 'gargn_earthworm/src/default.json'


# Prints AST node recursively.
def print_node(node, tabs):
    tab_str = '     '

    if not isinstance(node, ast.AST):
        return

    print('%s%s' %(tab_str*tabs, type(node)))
    for key, attr in node.__dict__.items():
        print('%s%s  ~~~  %s' %(tab_str*(tabs+1), key, attr))
        if isinstance(attr, list):
            for item in attr:
                print_node(item, tabs+2)
        else:
            print_node(attr, tabs+2)


# Prints AST structure.
def print_ast(node, debug):
    if debug:
        for child_node in node.__dict__['body']:
            print_node(child_node, tabs=0)
            print('')


# Opens and reads file.
def readfile(filename):
    try:
        f = open(filename)
    except IOError as e:
        raise FileNotFoundError(filename)
    return f.read()


# Processes commandline arguments.
def process_args():
    parser = argparse.ArgumentParser(description='Code to decompose.')
    parser.add_argument('filename', help='file to parse')
    parser.add_argument('--config', '-c', help='YAML configuration file')
    parser.add_argument('--slow', action='store_true', help='generate all suggestions')
    parser.add_argument('--debug', action='store_true', help='print debug messages')
    parser.add_argument('--noprogress', action='store_true', help='Do not print progress bar')
    args = parser.parse_args()
    return args


# Generates progress bars.
def progress_bar(noprogress, func_num, num_funcs):
    if not noprogress:
        percent = func_num / float(num_funcs + 1)
        arrow = '-' * int(round(percent * _LEN_PROGRESS_BAR)-1) + '>'
        spaces = ' ' * (_LEN_PROGRESS_BAR - len(arrow))

        sys.stdout.write("\rStatus: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()


# Removes progress bar.
def remove_progress_bar(noprogress):
    if not noprogress:
        sys.stdout.write("\r")
        sys.stdout.flush()


# Adds an indent to the text.
def indent(text, tab):
    padding = ' ' * tab
    return ''.join(padding+line for line in text.splitlines(True))


# TODO: Create a suggestions.txt file and output it to the screen
# Generates suggestions.
def generate_suggestions(source, debug=False, slow=True, noprogress=True):
    total_func_complexity = 0
    progress = 0

    # Process arguments.
    #args = process_args()
    #source = readfile(filename)
    #print('\n\nRunning file... {}\n'.format(args.filename))

    # Parse JSON file.
    config = parse_json(None)

    # Generate AST.
    node = ast.parse(source)
    print_ast(node, debug) # Debug = false

    # Generate Linter suggestions.
    #suggestions = get_linter_suggestions(node, source, debug)
    #if suggestions:
    #    print('Each message below indicates formatting related messages. '
    #          'Fixing of the primary suggestions from the decomposer.\n')
    #    for lineno, messages in sorted(suggestions.items()):
    #        print('\tline {}: {}'.format(lineno, ' '.join(messages)))
    #    print('\n')

    # Generate CFG.
    generator = CFGGenerator(debug)
    cfg = generator.generate(node, source)
    num_funcs = cfg.get_num_funcs()
    #progress_bar(noprogress, func_num=0, num_funcs=num_funcs)

    # Generates suggestions.
    suggestions = []
    for func_num, func_block in enumerate(cfg.get_funcs()):
        progress_bar(noprogress, func_num=func_num + 1, num_funcs=num_funcs)
        func_slice = Slice(func_block, config, slow)
        suggestions.extend(func_slice.get_suggestions())
        total_func_complexity += func_slice.get_avg_lineno_slice_complexity()
    #remove_progress_bar(noprogress)

    '''
    # Print suggestions.
    if suggestions:
        print('Each message below indicates lines of \'{}\' you may be able to '
              'refactor into new function. The parameters and return values '
              'provided correspond with the new function. Use your own '
              'discretion when determining if the decomposition is fit for '
              'you.'.format(filename), end=' ')
        if not slow:
            print('For additional suggestions try using the flag --slow.', end=' ')
        print('\n')
        for suggestion in suggestions:
            print('{}'.format(suggestion))
    else:
        print('No suggestions detected.', end=' ')
        if not slow:
            print('For additional suggestions try using the flag --slow.\n')
        else:
            print('{}'.format(' ' * _LEN_PROGRESS_BAR))
    '''

    return suggestions

#    print('Line number complexity: {0:.2f}\n\n'.format(total_func_complexity))


# Generates a Config object from a dictionary.
def generate_config_obj(info):
    config = Config()
    config.min_diff_complexity_between_slices = info['generating_suggestions']['min_diff_complexity_between_slices']
    config.min_diff_ref_and_live_var = info['generating_suggestions']['min_diff_ref_and_live_var']
    config.min_linenos_diff_reference_livevar_instr = info['generating_suggestions']['min_linenos_diff_reference_livevar_instr']

    config.min_lines_in_suggestion = info['validating_suggestions']['min_lines_in_suggestion']
    config.min_variables_parameter_in_suggestion = info['validating_suggestions']['min_variables_parameter_in_suggestion']
    config.max_variables_parameter_in_suggestion = info['validating_suggestions']['max_variables_parameter_in_suggestion']
    config.max_variables_return_in_suggestion = info['validating_suggestions']['max_variables_return_in_suggestion']
    config.min_lines_func_not_in_suggestion = info['validating_suggestions']['min_lines_func_not_in_suggestion']
    return config


# Parses a JSON file into a Config object.
def parse_json(filename=None):
    filename = filename if filename else _DEFAULT_JSON_FILE
    info = None

    # Opens file.
    try:
        data_file = open(filename, 'r')
    except EnvironmentError as e:
        raise FileNotFoundError(filename)

    # Gets config object.
    obj_json = data_file.read()
    info = json.loads(obj_json)
    config = generate_config_obj(info)
    data_file.close()
    return config


def main():
    try:
        generate_suggestions()
    except DecomposerError as error:
        print(error.message)


if __name__ == '__main__':
    main()
