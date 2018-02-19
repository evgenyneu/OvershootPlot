# Plots overshoot parameters for a single model (one snapshot in time).
#
# Run this from your console to show help:
#
#   python3 plot_model.py -h
#
# Source: https://github.com/evgenyneu/OvershootPlot
#

from model.parse_arguments import parse_arguments
from model.parse_data import find_single_model
from model.plot import plot
import matplotlib.pyplot as plt
from shared.plot import show_plot, add_subplot

arguments = parse_arguments()
model = find_single_model(filename=arguments.file, model_number=arguments.model_number,
    zone_number=arguments.zone_number, overshoot_direction=arguments.overshoot_direction)

if not model: exit(f"Could not find model.")
plot(arguments, model, add_subplot(plt))
show_plot(plt, arguments)
