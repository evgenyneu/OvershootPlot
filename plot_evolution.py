# Plots stellar overshoot parameters that are evolving with time.
#
# Run this from your console to show help:
#
#   python3 plot_evolution.py -h
#
# Source: https://github.com/evgenyneu/OvershootPlot
#

from evolution.parse_arguments import parse_arguments
from evolution.parse_data import parse_models
from evolution.plot import plot
import matplotlib.pyplot as plt
from shared.plot import show_plot, add_subplot

arguments = parse_arguments()
models = parse_models(filename=arguments.file, skip_models=arguments.skip_models)
plot(arguments, models, add_subplot(plt))
show_plot(plt, arguments)
