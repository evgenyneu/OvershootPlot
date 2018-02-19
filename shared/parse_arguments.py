# Functions for parsing command line arguments

from version import __version__

def input_file_argument(parser):
    parser.add_argument('file', action='store', default='OshInfo.xxx', nargs='?',
        help='Data file to plot from. OshInfo.xxx is used by default.')

def arguments_for_axis_multiple(parser, axis_name, option_name, variable_name, values):
    variable_help = arguments_help_for_axis(axis_name=axis_name, values=values)
    variable_help += f"\n  Note: multiple variables can be plotted: {option_name}=var1 {option_name}=var2.\n\n"
    parser.add_argument(option_name, action='append', dest=variable_name, default=[], help=variable_help)

def arguments_for_axis_single(parser, axis_name, option_name, variable_name, values, default):
    variable_help = arguments_help_for_axis(axis_name=axis_name, values=values)
    parser.add_argument(option_name, dest=variable_name, default=default, help=variable_help)
    variable_help += "\n\n"

def arguments_help_for_axis(axis_name, values):
    variable_help = f"Variable(s) for plotting on the {axis_name}-axis:\n"

    for key, value in values.items():
        variable_help += f"  {key}: {value['description']}\n"

    return variable_help

def verify_multiple_argument(option_name, selected_arguments, allowed_arguments, default):
    if len(selected_arguments) == 0:
        for default_intem in default:
            selected_arguments.append(default_intem)

    check_argument_allowed(
        option_name=option_name,
        selected_arguments=selected_arguments,
        allowed_arguments=allowed_arguments)

def verify_single_argument(option_name, selected_argument, allowed_arguments):
    check_argument_allowed(
        option_name=option_name,
        selected_arguments=[selected_argument],
        allowed_arguments=allowed_arguments)

def check_argument_allowed(option_name, selected_arguments, allowed_arguments):
    for variable in selected_arguments:
        if not variable in allowed_arguments.keys():
            allowed_names = list(map(lambda name: f"'{name}'", allowed_arguments.keys()))
            quit(f"error: argument {option_name}: invalid choice: {variable} (choose from {', '.join(allowed_names)}).")

def setup_shared_arguments(parser):
    parser.add_argument('-f', action='store', dest='output_file',
        help='Name of the output image file.\nBy default the graph is shown in a window.\nSupply file extension to choose a format, for example "-f=output.pdf".')

    parser.add_argument('-xmin', action='store', help="Set the minimum limit of the X-axis", type=float)
    parser.add_argument('-xmax', action='store', help="Set the maximum limit of the X-axis", type=float)
    parser.add_argument('-ymin', action='store', help="Set the minimum limit of the Y-axis", type=float)
    parser.add_argument('-ymax', action='store', help="Set the maximum limit of the Y-axis", type=float)
    parser.add_argument('-xinvert', action='store_true', help="Invert X-axis", default=False)
    parser.add_argument('-yinvert', action='store_true', help="Invert Y-axis", default=False)

    parser.add_argument('-xlabel', action='store', help="Label for the X-axis")
    parser.add_argument('-ylabel', action='store', help="Label for the Y-axis")

    parser.add_argument('-nolegend', action='store_true', help="Hide legend", default=False)

    parser.add_argument('-V', '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))