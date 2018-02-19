import matplotlib
import tkinter as tk
from matplotlib.figure import Figure
from model.parse_arguments import parse_arguments
from model.parse_data import find_single_model, find_first_last_model, read_model_number
from model.plot import plot
from model.configuration_constants import variables_for_plotting, overshoot_directions
from gui.app import start_app
from gui.live_info import live_info_file_name, read_live_info_data
from gui.file_watcher import FileWatcher
from gui.graph_page import GraphPage
from gui.plot_controls import PlotControls
from gui.controls import show_option_menu
from gui.tk_app import TkApp


arguments = parse_arguments()

class MPLGraph(Figure):

    def __init__(self):
        Figure.__init__(self, figsize=(8, 5))
        self.plot = None

    def redraw(self, data):
        if self.plot != None: self.delaxes(self.plot)
        self.plot = self.add_subplot(111)
        plot(arguments, data, self.plot)

class PlotVariables():
    def __init__(self):
        self.first_model = None
        self.last_model = None

        self.model_number = tk.IntVar()
        self.model_number_slider = tk.IntVar()
        self.x_axis = tk.StringVar()
        self.y_axis = tk.StringVar()
        self.x_min = tk.StringVar()
        self.x_max = tk.StringVar()
        self.y_min = tk.StringVar()
        self.y_max = tk.StringVar()
        self.xinvert = tk.IntVar()
        self.yinvert = tk.IntVar()
        self.zone_number = tk.IntVar()
        self.overshoot_direction = tk.StringVar()

class MyPlotControls(PlotControls):
    def __init__(self, parent):
        PlotControls.__init__(self, parent)

        self.show_model_input(row=0, column=0)
        self.show_x_axis_options(row=1, column=0)
        self.show_y_axis_options(row=2, column=0)
        self.show_xinvert(row=0, column=3)
        self.show_yinvert(row=0, column=5)
        self.show_x_min(row=1, column=2)
        self.show_x_max(row=1, column=4)
        self.show_y_min(row=2, column=2)
        self.show_y_max(row=2, column=4)
        self.show_zone_options(row=1, column=6)
        self.show_overshoot_direction_options(row=2, column=6)
        self.update()

    def update(self):
        if self.variables.model_number.get() != arguments.model_number:
            self.variables.model_number.set(arguments.model_number)

        if self.page.data != None:
            new_zones = self.page.data['zones']

            if new_zones != self.number_of_zones:
                self.number_of_zones = new_zones
                self.update_zone_options()

            if self.variables.zone_number.get() != arguments.zone_number:
                self.variables.zone_number.set(arguments.zone_number)

    def show_overshoot_direction_options(self, row, column):
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

    def update_zone_options(self):
        menu = self.zone_options['menu']
        menu.delete(0, 'end')

        for name in range(1, self.number_of_zones + 1):
            menu.add_command(label=name, command=lambda value=name: self.zone_number_selected_update_variable(value))

    def show_zone_options(self, row, column):
        self.number_of_zones = 1

        self.zone_options = show_option_menu(container=self, row=row, column=column,
            text='Zone:', default_index=0,
            command=self.zone_number_selected, variable=self.variables.zone_number,
            variables=[1])

    def zone_number_selected(self, selected_value):
        arguments.zone_number = selected_value
        self.page.redraw_plot()

    def zone_number_selected_update_variable(self, selected_value):
        if self.variables.zone_number.get() == selected_value: return
        self.variables.zone_number.set(selected_value)
        self.zone_number_selected(selected_value)

    def show_model_input(self, row, column):
        self.show_label_with_entry(row=row, column=column, text="Model",
            variable=self.variables.model_number)

        self.variables.model_number.trace("w", self.did_change_model)

    def did_change_model(self, *args):
        arguments.model_number = self.variables.model_number.get()

        if arguments.model_number > self.variables.last_model or arguments.model_number < self.variables.first_model:
            arguments.model_number = self.variables.first_model

        if self.variables.model_number_slider.get() != arguments.model_number:
            self.variables.model_number_slider.set(arguments.model_number)

        self.page.redraw_plot()
        self.update() # Needed to update the list of zones for the new model

    def show_x_axis_options(self, row, column):
        self.show_axis_options_with_default_value(row=row, column=column,text="X Axis:",
            axis_options = variables_for_plotting, default_value=arguments.x,
            command=self.x_menu_selected, variable=self.variables.x_axis)

    def show_y_axis_options(self, row, column):
        default_value = 'nonsense'
        if len(arguments.y) > 0: default_value = arguments.y[0]

        self.show_axis_options_with_default_value(row=row, column=column, text="Y Axis:",
            axis_options = variables_for_plotting, default_value=default_value,
            command=self.y_menu_selected, variable=self.variables.y_axis)

    def x_menu_selected(self, selected_value):
        key = self.find_axis_variable(description=selected_value,
            axis_options=variables_for_plotting)
        if key == None: return;

        arguments.x = key
        self.page.redraw_plot()

    def y_menu_selected(self, selected_value):
        key = self.find_axis_variable(description=selected_value,
            axis_options=variables_for_plotting)

        if key == None: return;

        arguments.y = [key]
        self.page.redraw_plot()


class MyGraphPage(GraphPage):

    def __init__(self, parent, variables, arguments):
        GraphPage.__init__(self, parent, variables, arguments)
        self.data = None
        self.previous_loaded_line_offset = None
        self.previous_loaded_file = None
        self.previous_loaded_model_number = None
        self.previous_loaded_zone_number = None
        self.previous_loaded_overshoot_direction = None
        self.show_model_slider()
        self.show_controls()

    def update_controls(self):
        if self.variables.model_number_slider.get() != arguments.model_number:
            self.variables.model_number_slider.set(arguments.model_number)

        self.update_slider()
        self.plot_controls.update()

    def update_slider(self):
        self.scale.configure(from_=self.variables.first_model)
        self.scale.configure(to=self.variables.last_model)
        tickinterval = int((self.variables.last_model - self.variables.first_model)/7)
        self.scale.configure(tickinterval=tickinterval)

    def show_model_slider(self):
        self.scale = tk.Scale(self, length=780,
            orient=tk.HORIZONTAL, command=self.slider_changed,
            variable=self.variables.model_number_slider, bg='white')

        self.update_slider()
        self.scale.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def show_controls(self):
        self.plot_controls = MyPlotControls(self)
        self.plot_controls.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def slider_changed(self, position):
        arguments.model_number = self.variables.model_number_slider.get()

        if self.variables.model_number.get() != arguments.model_number:
            self.variables.model_number.set(arguments.model_number)

    def load_data(self):
        if (arguments.file == self.previous_loaded_file and
            self.previous_loaded_model_number == arguments.model_number and
            self.previous_loaded_zone_number == arguments.zone_number and
            self.previous_loaded_overshoot_direction == arguments.overshoot_direction):
            return # already loaded

        if arguments.file != self.previous_loaded_file:
            self.previous_loaded_line_offset = None

        self.previous_loaded_file = arguments.file
        self.previous_loaded_model_number = arguments.model_number
        self.previous_loaded_zone_number = arguments.zone_number
        self.previous_loaded_overshoot_direction = arguments.overshoot_direction

        self.store_models_file_offsets(filename=arguments.file)

        model_offset = self.previous_loaded_line_offset[arguments.model_number]


        self.data = find_single_model(filename=arguments.file, model_number=arguments.model_number,
            zone_number=arguments.zone_number, overshoot_direction=arguments.overshoot_direction,
            offset=model_offset)

    def store_models_file_offsets(self, filename):
        """
        Store the offsets for the models in the data file.
        This will allow to users to quickly view different models
        by changing the slider, without a need to read the entire file line by line
        from the start.
        """
        if self.previous_loaded_line_offset != None: return

        with open(filename) as file:
            self.previous_loaded_line_offset = {}
            offset = 0
            for line in file:
                model_number = read_model_number(line)

                if (model_number != None and
                    (model_number not in self.previous_loaded_line_offset)):
                    self.previous_loaded_line_offset[model_number] = offset

                offset += len(line)

class MyTkApp(TkApp):
    def __init__(self,parent):
        TkApp.__init__(self,parent)

    def initialize(self):
        self.variables = PlotVariables()
        self.init_from_data_file()

        self.graph_page = MyGraphPage(self, self.variables, arguments)
        self.fig = MPLGraph()
        self.create_ui()
        self.graph_page.update_controls()

        self.watcher = FileWatcher(live_info_file_name())
        self.watch_live_info_changes()

    def init_from_data_file(self):
        self.variables.first_model, self.variables.last_model = find_first_last_model(arguments.file)

        if (arguments.model_number == None
            or arguments.model_number < self.variables.first_model
            or arguments.model_number > self.variables.last_model):
            arguments.model_number = self.variables.first_model

    def watch_live_info_changes(self):
        self.watcher.check_file_changed(self.did_live_info_change)
        self.after(500, self.watch_live_info_changes)

    def did_live_info_change(self):
        file, model_number = read_live_info_data()
        if model_number == None: return
        if file == None: return
        arguments.file = file
        arguments.model_number = model_number
        self.init_from_data_file()
        self.graph_page.update_controls()

if __name__ == "__main__":
    app = MyTkApp(None)
    start_app(app=app, title="Overshoot Model Plot")

