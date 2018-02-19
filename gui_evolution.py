import matplotlib
import platform
import tkinter as tk
from matplotlib.figure import Figure
from evolution.parse_arguments import parse_arguments
from evolution.parse_data import parse_models
from evolution.plot import plot
from evolution.configuration_constants import variables_x, variables_y, convective_zone_types, overshoot_directions
from shared.evo_string import try_convert_to_float
from gui.app import start_app
from gui.live_info import find_model_from_xvalue, live_info_for_model, view_mode_details
from gui.graph_page import GraphPage
from gui.plot_controls import PlotControls
from gui.tk_app import TkApp

arguments = parse_arguments()

class MPLGraph(Figure):

    def __init__(self):
        Figure.__init__(self, figsize=(8, 5))
        self.plot = None
        self.selection_plot = None

    def show_selection(self, x):
        if self.selection_plot == None:
            line = self.plot.lines[0]
            variable_y = line.get_ydata()
            if len(variable_y) == 0: return
            self.selection_plot, = self.plot.plot([x, x], [variable_y[0],variable_y[0]], 'co-', lw=1)
            self.show_selection(x)
        else:
            ylim = self.plot.get_ylim()
            self.selection_plot.set_data([x, x], [ylim[0], ylim[1]])

    def redraw(self, data):
        if self.plot != None: self.delaxes(self.plot)
        self.selection_plot = None
        self.plot = self.add_subplot(111)
        plot(arguments, data, self.plot)

class PlotVariables():
    def __init__(self):
        self.x_axis = tk.StringVar()
        self.y_axis = tk.StringVar()
        self.y_axis2 = tk.StringVar()
        self.x_min = tk.StringVar()
        self.x_max = tk.StringVar()
        self.y_min = tk.StringVar()
        self.y_max = tk.StringVar()
        self.xinvert = tk.IntVar()
        self.yinvert = tk.IntVar()
        self.zone_type = tk.StringVar()
        self.overshoot_direction = tk.StringVar()
        self.selected_model_info = tk.StringVar()

        self.zone1 = tk.IntVar()
        self.zone2 = tk.IntVar()
        self.zone3 = tk.IntVar()
        self.zone4 = tk.IntVar()
        self.zone5 = tk.IntVar()


class MyPlotControls(PlotControls):
    def __init__(self, parent):
        PlotControls.__init__(self, parent)

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        self.show_zone_types(row=0, column=0)
        self.show_x_axis_options(row=1, column=0)
        self.show_y_axis_options(row=2, column=0)
        self.show_y_axis_options2(row=3, column=0)
        self.show_xinvert(row=0, column=3)
        self.show_yinvert(row=0, column=5)
        self.show_x_min(row=1, column=2)
        self.show_x_max(row=1, column=4)
        self.show_y_min(row=2, column=2)
        self.show_y_max(row=2, column=4)
        self.show_selected_model_info(row=3, column=3, columnspan=6)

        self.show_overshoot_directions(row=0, column=6)
        self.show_zones(row=1, column=6)

    def show_zones(self, row, column):
        model_label = tk.Label(self, text="Zones", bg='white', padx=5, pady=5)
        model_label.grid(row=row,column=column,sticky=tk.W)

        checkboxes = tk.Frame(self)
        checkboxes.grid(row=row,column=column+1,sticky=tk.EW)

        self.add_zone_checkbox(index=0,parent=checkboxes,variable=self.variables.zone1)
        self.add_zone_checkbox(index=1,parent=checkboxes,variable=self.variables.zone2)
        self.add_zone_checkbox(index=2,parent=checkboxes,variable=self.variables.zone3)
        self.add_zone_checkbox(index=3,parent=checkboxes,variable=self.variables.zone4)
        self.add_zone_checkbox(index=4,parent=checkboxes,variable=self.variables.zone5)

    def add_zone_checkbox(self, index, parent, variable):
        button = tk.Checkbutton(parent, text=str(index+1), variable=variable, background='white')
        button.grid(row=0,column=index,sticky=tk.W)

        # Set initial value
        value = 0
        for selected_zone_number in arguments.zone_numbers:
            if selected_zone_number == index+1:
                value = 1
                break

        variable.set(value)

        variable.trace("w", self.did_change_zone)

    def did_change_zone(self, *args):
        zones=[]
        if bool(self.variables.zone1.get()): zones.append(1)
        if bool(self.variables.zone2.get()): zones.append(2)
        if bool(self.variables.zone3.get()): zones.append(3)
        if bool(self.variables.zone4.get()): zones.append(4)
        if bool(self.variables.zone5.get()): zones.append(5)
        arguments.zone_numbers = zones
        self.page.redraw_plot()

    def show_zone_types(self, row, column):
        self.show_axis_options_with_default_value(row=row, column=column,text="Zone type:",
            axis_options=convective_zone_types,
            default_value=arguments.zone_type,
            command=self.zone_type_selected,
            variable=self.variables.zone_type)

    def zone_type_selected(self, selected_value):
        key = self.find_axis_variable(description=selected_value, axis_options=convective_zone_types)
        if key == None: return;

        arguments.zone_type = key
        self.page.redraw_plot()

    def show_overshoot_directions(self, row, column):
        self.show_axis_options_with_default_value(row=row, column=column,text="Direction:",
            axis_options=overshoot_directions,
            default_value=arguments.overshoot_direction,
            command=self.overshoot_direction_selected,
            variable=self.variables.overshoot_direction)

    def overshoot_direction_selected(self, selected_value):
        key = self.find_axis_variable(description=selected_value, axis_options=overshoot_directions)
        if key == None: return;

        arguments.overshoot_direction = key
        self.page.redraw_plot()

    def show_x_axis_options(self, row, column):
        self.show_axis_options_with_default_value(row=row, column=column,text="X Axis:",
            axis_options=variables_x,
            default_value=arguments.x,
            command=self.x_menu_selected,
            variable=self.variables.x_axis)

    def show_y_axis_options(self, row, column):
        default_value = 'nonsense'
        if len(arguments.y) > 0: default_value = arguments.y[0]

        self.show_axis_options_with_default_value(row=row, column=column, text="Y Axis:",
            axis_options=variables_y,
            default_value=default_value,
            command=self.y_menu_selected, variable=self.variables.y_axis)

    def show_y_axis_options2(self, row, column):
        variables_y2 = {
            'none': {'description': 'None'}
        }

        for key, value in variables_y.items(): variables_y2[key] = value

        default_value = 'none'
        if len(arguments.y) > 1: default_value = arguments.y[1]

        self.show_axis_options_with_default_value(row=row, column=column, text="Y Axis #2:",
            axis_options=variables_y2,
            default_value=default_value,
            command=self.y_menu_selected, variable=self.variables.y_axis2)

    def x_menu_selected(self, selected_value):
        key = self.find_axis_variable(description=selected_value, axis_options=variables_x)
        if key == None: return;

        arguments.x = key
        self.page.redraw_plot()

    def y_menu_selected(self, selected_value):
        key1 = self.find_axis_variable(
            description=self.variables.y_axis.get(),
            axis_options=variables_y)

        if key1 == None: return;
        arguments.y = [key1]

        key2 = self.find_axis_variable(
            description=self.variables.y_axis2.get(),
            axis_options=variables_y)

        if key2 != None and key2 != 'none': arguments.y.append(key2)

        self.page.redraw_plot()

    def show_selected_model_info(self, row, columnspan, column):
        model_label = tk.Label(self, bg='white',
            textvariable=self.variables.selected_model_info,
            padx=5, pady=5)

        self.variables.selected_model_info.set("Click on graph to see details. Right click to see model details if gui_model.py is opened.")

        model_label.grid(row=row,column=column,columnspan=columnspan, sticky=tk.W)


class MyGraphPage(GraphPage):

    def __init__(self, parent, variables, arguments):
        GraphPage.__init__(self, parent, variables, arguments)
        self.previous_loaded_file = None
        self.show_controls()

    def show_controls(self):
        self.plot_controls = MyPlotControls(self)
        self.plot_controls.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def add_plot_figure(self, fig):
        GraphPage.add_plot_figure(self, fig)
        self.mpl_canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        if event.xdata == None: return
        selected_model = find_model_from_xvalue(xvalue=event.xdata, models=self.data,
            variable_name=arguments.x)

        if selected_model != None:
            info = live_info_for_model(selected_model)
            self.variables.selected_model_info.set(info)
            self.fig.show_selection(event.xdata)
            self.mpl_canvas.draw()

        if event.button == 3: # Right-click
            view_mode_details(model_number=selected_model['model'], file=arguments.file)

    def load_data(self):
        if arguments.file == self.previous_loaded_file: return # already loaded
        self.previous_loaded_file = arguments.file
        self.data = parse_models(arguments.file)

class MyTkApp(TkApp):
    def __init__(self,parent):
        TkApp.__init__(self,parent)

    def initialize(self):
        self.variables = PlotVariables()

        self.graph_page = MyGraphPage(self, self.variables, arguments)
        self.fig = MPLGraph()
        self.create_ui()

if __name__ == "__main__":
    app = MyTkApp(None)
    start_app(app=app, title="Overshoot Evolution Plot")

