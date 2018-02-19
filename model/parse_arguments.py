# Functions for parsing command line arguments

import argparse
from argparse import RawTextHelpFormatter
from .configuration_constants import variables_for_plotting
from shared.parse_arguments import arguments_for_axis_single, arguments_for_axis_multiple, verify_single_argument, verify_multiple_argument, setup_shared_arguments, input_file_argument
from shared.configuration_constants import OVERSHOOT_DIRECTION_IN, OVERSHOOT_DIRECTION_OUT



def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Plots stellar overshoot parameters for a single model at one instance of time.',
        formatter_class=RawTextHelpFormatter)

    input_file_argument(parser)

    parser.add_argument('-m', action='store', dest='model_number',
        help="The model number to use in the plot. The first model from the file is used by default.",
        type=int)


    # Zone number
    # -----------

    zone_number_help = """Convective zone number to show:
  The zone number 1 is the closest to the core."""

    parser.add_argument('-z', action='store', dest='zone_number', default=1, type=int,
        help=zone_number_help)

    #  zone boundary
    # -----------

    parser.add_argument("-d", action='store', dest='overshoot_direction', default=OVERSHOOT_DIRECTION_IN,
        choices=[OVERSHOOT_DIRECTION_IN, OVERSHOOT_DIRECTION_OUT],
        help="Direction of the overshoot")

    # X Axis
    # -----------

    arguments_for_axis_single(
        parser=parser,
        axis_name='X',
        option_name='-x',
        variable_name='x',
        values=variables_for_plotting,
        default='j')

    # Y Axis
    # -----------

    arguments_for_axis_multiple(
        parser=parser,
        axis_name='Y',
        option_name='-y',
        variable_name='y',
        values=variables_for_plotting)

    # Other arguments
    # ------------

    setup_shared_arguments(parser)

    parser.add_argument('-noboundaries', action='store_true', help="Do not plot the overshoot boundaries", default=False)
    parser.add_argument('-title', action='store', help="Text for the title. Title is hidden if value is 'none'.")

    # Parse arguments
    # ---------

    arguments = parser.parse_args()

    verify_single_argument(
        option_name='-x',
        selected_argument=arguments.x,
        allowed_arguments=variables_for_plotting)

    verify_multiple_argument(
        option_name='-y',
        selected_arguments=arguments.y,
        allowed_arguments=variables_for_plotting,
        default=['r_rsun'])

    return arguments
