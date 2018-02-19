# Functions for plotting the data for a single model

from matplotlib.path import Path
import matplotlib.patches as patches
from .configuration_constants import variables_for_plotting, convective_zone_types
from shared.plot import set_axes_limits, layout_plot, label_for_axes, invert_axes, set_axes_labels as shared_set_axes_labels
from shared.list_monotonic import monotonic
from shared.configuration_constants import OVERSHOOT_DIRECTION_IN

def plot(arguments, model, plt):
    if model == None:
        plot_blank(plt=plt)
        plt.set_title("Data not found. Change Zone and Direction settings.")
        return

    for y_variable in arguments.y:
        plot_variable(plt, model, arguments.x, y_variable)

    set_axes_labels(plt, arguments)
    set_axes_limits(plt, arguments)

    if not arguments.noboundaries:
        plot_overshoot(plt=plt, model=model, arguments=arguments)

    show_title(plt=plt, model=model, arguments=arguments)
    invert_axes(plt, arguments)
    layout_plot(plt)

def set_axes_labels(plt, arguments):
    xlabel = label_for_axes(all=variables_for_plotting, name=arguments.x)
    descriptions = list(map(lambda name: label_for_axes(all=variables_for_plotting, name=name), arguments.y))
    ylabel = '\n'.join(descriptions)
    shared_set_axes_labels(plt=plt, arguments=arguments, xlabel=xlabel, ylabel=ylabel)

def plot_blank(plt):
    plt.plot([], [])

def plot_variable(plt, model, x_variable, y_variable):
    mesh_points = model['mesh_points']
    variable_x_data = list(map(lambda data: data[x_variable], mesh_points))
    variable_y_data = list(map(lambda data: data[y_variable], mesh_points))
    plt.plot(variable_x_data, variable_y_data)

def find_oveshoot_x_boundaries(model, x_variable):
    x_start = None
    x_end = None
    x_end_fixed = None

    point = find_mesh_point(model, model['overshoot_start'])
    if point != None: x_start = point[x_variable]

    if model['overshoot_direction'] == OVERSHOOT_DIRECTION_IN:
        if model['overshoot_start'] < model['overshoot_end']:
            exit("Error: OshStart is smaller then OshEnd")
    else:
        if model['overshoot_start'] > model['overshoot_end']:
            exit("Error: OshStart is greater then OshEnd")

    point_end = find_mesh_point(model, model['overshoot_end'])
    overshoot_increment = -1 if model['overshoot_direction'] == OVERSHOOT_DIRECTION_IN else 1
    point_end_plus_one = find_mesh_point(model, model['overshoot_end'] - overshoot_increment)

    if point_end != None and point_end_plus_one != None:
        x_end = point_end[x_variable]

        # Apply the overthoot fix
        # by interpolating between the values at the overshoot end and the next mesh point
        x_fix = (point_end_plus_one[x_variable] - point_end[x_variable]) * model['overtshoot_fix']
        x_end_fixed = x_end + x_fix

    return x_start, x_end_fixed

def find_mesh_point(model, j):
    if j == 0: j = 1
    return next(x for x in model['mesh_points'] if x['j'] == j)

def plot_overshoot(plt, model, arguments):
    osh_start, osh_end = None, None
    mesh_points = model['mesh_points']
    variable_x_data = list(map(lambda data: data[arguments.x], mesh_points))

    if not monotonic(variable_x_data): return

    x_start, x_end = find_oveshoot_x_boundaries(model, arguments.x)
    if x_start == None or x_end == None: return
    draw_overshoot_region(arguments, plt, x_start, x_end)

def draw_overshoot_region(arguments, plt, x_start, x_end):
    ylim = plt.get_ylim()
    plot_line1, = plt.plot([x_start, x_start], [ylim[0], ylim[1]], 'r:', lw=2, label="Overshoot start")
    plot_line2, = plt.plot([x_end, x_end], [ylim[0], ylim[1]], 'b--', lw=2, label="Overshoot end")

    if not arguments.nolegend:
        plt.legend(handles=[plot_line1,plot_line2])

def show_title(plt, model, arguments):
    if arguments.title == 'none': return
    title = arguments.title

    if title == None:
        model_number = model['model']
        direction = model['overshoot_direction']
        zone_number = model['zone_number']
        zone_type = model['type']

        if zone_type in convective_zone_types:
            zone_type = convective_zone_types[zone_type]['human_friendly']
        else:
            exit(f'Unknown zone type {zone_type}')

        title = f'Overshoot {direction} from {zone_type}, model {model_number}, convective zone {zone_number}'

    plt.set_title(title)



