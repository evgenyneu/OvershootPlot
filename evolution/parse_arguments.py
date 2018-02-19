# Functions for parsing command line arguments

import argparse
from argparse import RawTextHelpFormatter
from .configuration_constants import convective_zone_types, variables_x, variables_y, overshoot_directions
from shared.parse_arguments import arguments_for_axis_multiple, arguments_for_axis_single, verify_multiple_argument, verify_single_argument, setup_shared_arguments, input_file_argument

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Plots stellar overshoot parameters changing with time.',
        formatter_class=RawTextHelpFormatter)

    input_file_argument(parser)

    #  zone type
    # -----------

    zone_help = "Type of convective zone to show:\n"

    for key, value in convective_zone_types.items():
        zone_help += f"  {key}: {value['description']}\n"

    parser.add_argument('-t', action='store', dest='zone_type', default='all', help=zone_help)

    # Zone number
    # -----------

    zone_number_help = """Convective zone number to show:
  The zone number 1 is the closest to the core.
  All zones are shown by default.
  You can use this option multiple times to show many zones."""

    parser.add_argument('-z', action='append', dest='zone_numbers', default=[], type=int,
        help=zone_number_help)

    #  zone boundary
    # -----------

    parser.add_argument("-d", action='store', dest='overshoot_direction', default='both',
        choices=overshoot_directions.keys(), help="Direction of the overshoot")

     #  zone boundary
    # -----------

    parser.add_argument("-skip", action='store', dest='skip_models', default=None, type=int,
        help="""Specify the number of models to skip every time a model is read from the data file.
  Large number will help loading big files faster.
  Use 0 to load every model.""")

    # X Axis
    # -----------

    arguments_for_axis_single(
        parser=parser,
        axis_name='X',
        option_name='-x',
        variable_name='x',
        values=variables_x,
        default='model')

    # Y Axis
    # -----------

    arguments_for_axis_multiple(
        parser=parser,
        axis_name='Y',
        option_name='-y',
        variable_name='y',
        values=variables_y)

    # Other arguments
    # ------------

    setup_shared_arguments(parser)

    # Parse arguments
    # ---------

    arguments = parser.parse_args()

    verify_single_argument(
        option_name='-x',
        selected_argument=arguments.x,
        allowed_arguments=variables_x)

    verify_multiple_argument(
        option_name='-y',
        selected_arguments=arguments.y,
        allowed_arguments=variables_y,
        default=['overshoot_r_m'])

    verify_single_argument(
        option_name='-z',
        selected_argument=arguments.zone_type,
        allowed_arguments=convective_zone_types)

    return arguments