# Shared functions for plotting

def set_axes_labels(plt, arguments, xlabel, ylabel):
    if arguments.xlabel: xlabel = arguments.xlabel
    plt.set_xlabel(xlabel)

    if arguments.ylabel: ylabel = arguments.ylabel
    plt.set_ylabel(ylabel)

def set_axes_limits(plt, arguments):
    if arguments.xmin: plt.set_xlim(xmin=float(arguments.xmin))
    if arguments.xmax: plt.set_xlim(xmax=float(arguments.xmax))
    if arguments.ymin: plt.set_ylim(ymin=float(arguments.ymin))
    if arguments.ymax: plt.set_ylim(ymax=float(arguments.ymax))

def layout_plot(plt):
    plt.ticklabel_format(style='sci', axis='both', scilimits=(-4,4), useOffset=False)

def show_plot(plt, arguments):
    if arguments.output_file:
        plt.savefig(arguments.output_file)
    else:
        plt.show()

def add_subplot(plt):
    return plt.figure(tight_layout=True).add_subplot(111)

def invert_axes(plt, arguments):
    if arguments.xinvert: plt.invert_xaxis()
    if arguments.yinvert: plt.invert_yaxis()

def label_for_axes(all, name):
    item = all[name]
    label = item['description']
    units = None
    if 'units' in item: units = item['units']
    if units != None: label = f'{label} ({units})'
    return label