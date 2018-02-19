import tkinter as tk
from shared.evo_string import try_convert_to_float
from gui.controls import show_option_menu

class PlotControls(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='white')
        self.page = parent
        self.arguments = parent.arguments
        self.variables = parent.variables

    def show_xinvert(self, row, column):
        self.show_checkbox(row=row, column=column, text="X Invert", variable=self.variables.xinvert)
        self.variables.xinvert.set(self.arguments.xinvert)
        self.variables.xinvert.trace("w", self.did_change_xinvert)

    def show_yinvert(self, row, column):
        self.show_checkbox(row=row, column=column, text="Y Invert", variable=self.variables.yinvert)
        self.variables.yinvert.set(self.arguments.yinvert)
        self.variables.yinvert.trace("w", self.did_change_yinvert)

    def show_checkbox(self, row, column, text, variable):
        button = tk.Checkbutton(self, text=text, variable=variable, background='white')
        button.grid(row=row,column=column,sticky=tk.W)

    def did_change_xinvert(self, *args):
        self.arguments.xinvert = bool(self.variables.xinvert.get())
        self.page.redraw_plot()

    def did_change_yinvert(self, *args):
        self.arguments.yinvert = bool(self.variables.yinvert.get())
        self.page.redraw_plot()

    def show_x_min(self, row, column):
        self.show_label_with_entry(row=row, column=column, text="X Min:",
            variable=self.variables.x_min)

        if self.arguments.xmin != None: self.variables.x_min.set(self.arguments.xmin)
        self.variables.x_min.trace("w", self.did_change_x_min)

    def show_x_max(self, row, column):
        self.show_label_with_entry(row=row, column=column, text="X Max:",
            variable=self.variables.x_max)

        if self.arguments.xmax != None: self.variables.x_max.set(self.arguments.xmax)
        self.variables.x_max.trace("w", self.did_change_x_max)

    def show_y_min(self, row, column):
        self.show_label_with_entry(row=row, column=column, text="Y Min:",
            variable=self.variables.y_min)

        if self.arguments.ymin != None: self.variables.y_min.set(self.arguments.ymin)
        self.variables.y_min.trace("w", self.did_change_y_min)

    def show_y_max(self, row, column):
        self.show_label_with_entry(row=row, column=column, text="Y Max:",
            variable=self.variables.y_max)

        if self.arguments.ymax != None: self.variables.y_max.set(self.arguments.ymax)
        self.variables.y_max.trace("w", self.did_change_y_max)

    def did_change_x_min(self, *args):
        value_str = self.variables.x_min.get()
        value = try_convert_to_float(value_str)

        if value == None:
            self.arguments.xmin = None
        else:
            self.arguments.xmin = value_str

        self.arguments.xmin = value_str
        self.page.redraw_plot()

    def did_change_x_max(self, *args):
        value_str = self.variables.x_max.get()
        value = try_convert_to_float(value_str)

        if value == None:
            self.arguments.xmax = None
        else:
            self.arguments.xmax = value_str

        self.page.redraw_plot()

    def did_change_y_min(self, *args):
        value_str = self.variables.y_min.get()
        value = try_convert_to_float(value_str)

        if value == None:
            self.arguments.ymin = None
        else:
            self.arguments.ymin = value_str


        self.page.redraw_plot()

    def did_change_y_max(self, *args):
        value_str = self.variables.y_max.get()
        value = try_convert_to_float(value_str)

        if value == None:
            self.arguments.ymax = None
        else:
            self.arguments.ymax = value_str

        self.page.redraw_plot()

    def show_label_with_entry(self, row, column, text, variable):
        model_label = tk.Label(self, text=text, bg='white', padx=5, pady=5)
        model_label.grid(row=row,column=column,sticky=tk.W)
        entry_model = tk.Entry(self, textvariable=variable, bg='white')
        entry_model.grid(row=row,column=column+1,sticky=tk.EW, padx=5, pady=5)


    def show_axis_options(self, row, column, text, default_index, command,
        variable, axis_options):

        variables = list(map(lambda name: axis_options[name]['description'],
            axis_options.keys()))

        show_option_menu(container=self, row=row, column=column,
            text=text, default_index=default_index,
            command=command, variable=variable,
            variables=variables)

    def show_axis_options_with_default_value(self, row, column, text, default_value, command,
        variable, axis_options):

        variables = list(map(lambda name: axis_options[name]['description'],
            axis_options.keys()))

        default_index = 0


        if default_value in axis_options:
            description = axis_options[default_value]['description']

            try:
                default_index = variables.index(description)
            except ValueError:
                pass

        show_option_menu(container=self, row=row, column=column,
            text=text, default_index=default_index,
            command=command, variable=variable,
            variables=variables)

    def find_axis_variable(self,description, axis_options):
        for key, value in axis_options.items():
            if value['description'] != description: continue
            return key