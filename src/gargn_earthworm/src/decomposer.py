# File name: decomposer.py
# Author: Nupur Garg
# Date created: 12/25/2016
# Python Version: 3.5


import ast
import json
from .slice import Slice
from .generatecfg import CFGGenerator
from .config import Config


_LEN_PROGRESS_BAR = 40
_DEFAULT_JSON_FILE = 'gargn_earthworm/src/default.json'


# TODO: Create a suggestions.txt file and output it to the screen
# Generates suggestions.
def generate_suggestions(source, debug=False, slow=True, noprogress=True):
    total_func_complexity = 0
    progress = 0

    # Parse JSON file.
    config = parse_json(None)

    # Generate AST.
    node = ast.parse(source)

    # Generate CFG.
    generator = CFGGenerator(debug)
    cfg = generator.generate(node, source)
    num_funcs = cfg.get_num_funcs()

    # Generates suggestions.
    suggestions = []
    for func_num, func_block in enumerate(cfg.get_funcs()):
        func_slice = Slice(func_block, config, slow)
        suggestions.extend(func_slice.get_suggestions())
        total_func_complexity += func_slice.get_avg_lineno_slice_complexity()

    return suggestions



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
