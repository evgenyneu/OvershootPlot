# Functions for plotting the data

from .configuration_constants import variables_x, variables_y, convective_zone_types, overshoot_directions
from shared.plot import set_axes_limits, layout_plot, invert_axes, set_axes_labels as shared_set_axes_labels
import matplotlib.lines as mlines

def plot(arguments, models, plt):
    models = filter_models(arguments=arguments, models=models)
    legend={}

    for plot_index, y_variable in enumerate(arguments.y):
        plot_variable(arguments=arguments,
            plt=plt, models=models, x_variable=arguments.x, y_variable=y_variable,
            legend=legend, plot_index=plot_index)

    show_legend(plt,arguments,legend)
    set_axes_labels(plt, arguments)
    set_axes_limits(plt, arguments)
    invert_axes(plt, arguments)
    layout_plot(plt)

def set_axes_labels(plt, arguments):
    xlabel = variables_x[arguments.x]['description']
    descriptions = list(map(lambda name: variables_y[name]['description'], arguments.y))
    ylabel = '\n'.join(descriptions)
    shared_set_axes_labels(plt=plt, arguments=arguments, xlabel=xlabel, ylabel=ylabel)

def filter_models(arguments, models):
    if arguments.zone_type != None and arguments.zone_type != 'all':
        models = list(filter(lambda x: x['type'] == arguments.zone_type, models))

    if len(arguments.zone_numbers) != 0:
        models = list(filter(lambda x: x['zone_number'] in arguments.zone_numbers, models))


    if arguments.overshoot_direction != None and arguments.overshoot_direction != 'both':
        models = list(filter(lambda x: x['overshoot_direction'] == arguments.overshoot_direction, models))

    return models

def plot_variable(arguments,plt, models, x_variable, y_variable, legend, plot_index):
    for zone_number in range(1, 10):
        models_by_zone_number = list(filter(lambda x: x['zone_number'] == zone_number, models))
        if len(models_by_zone_number) == 0: continue;
        plot_zone(arguments=arguments,plt=plt, models=models_by_zone_number,
            x_variable=x_variable, y_variable=y_variable, legend=legend, plot_index=plot_index)

def plot_zone(arguments,plt, models, x_variable, y_variable, legend, plot_index):
    for zone_name, zone_settins in convective_zone_types.items():
        models_by_type = list(filter(lambda x: x['type'] == zone_name, models))
        if len(models_by_type) == 0: continue;

        for direction in list(overshoot_directions.keys())[1:]:
            models_by_direction = list(filter(lambda x: x['overshoot_direction'] == direction, models_by_type))
            if len(models_by_direction) == 0: continue;

            color = 'b'
            linestyle = '-'
            label = None

            if ('shared_among_zones' in variables_y[y_variable]
                and variables_y[y_variable]['shared_among_zones']):

                scatter_variable(plt=plt, models=models_by_direction,
                    x_variable=x_variable, y_variable=y_variable)

                return

            if direction in zone_settins['direction']:
                direction_data = zone_settins['direction'][direction]

                colors = direction_data['color']
                if plot_index >= len(colors):
                    color = colors[-1]
                else:
                    color = colors[plot_index]

                linestyle = direction_data['linestyle']

            label = zone_settins['label']
            label = f'{label} {direction}'

            if plot_index > 0:
                label = f'{label} #{plot_index+1}'

            plot_variable_with_style(plt=plt, models=models_by_direction,
                x_variable=x_variable, y_variable=y_variable,
                color=color, label=label, linestyle=linestyle, legend=legend)

def plot_variable_with_style(plt, models, x_variable, y_variable, color, label, linestyle, legend):
    if len(models) == 0: return

    legend[label] = {
        'color': color,
        'linestyle': linestyle
    }

    variable_y = list(map(lambda x: x[y_variable], models))
    variable_x = list(map(lambda x: x[x_variable], models))
    plt.plot(variable_x, variable_y, color=color, linestyle=linestyle)

def scatter_variable(plt, models, x_variable, y_variable):
    if len(models) == 0: return
    variable_y = list(map(lambda x: x[y_variable], models))
    variable_x = list(map(lambda x: x[x_variable], models))
    plt.scatter(variable_x, variable_y)

def show_legend(plt, arguments, legend):
    if arguments.nolegend: return
    items = []

    for label, settings in legend.items():
        if label == None: continue
        items.append(mlines.Line2D([], [], color=settings['color'], linestyle=settings['linestyle'], label=label))

    if len(items) > 0: plt.legend(handles=items)
