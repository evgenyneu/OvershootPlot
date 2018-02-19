import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import NavigationToolbar2

class GraphPage(tk.Frame):

    def __init__(self, parent, variables, arguments):
        tk.Frame.__init__(self, parent, bg='white')
        self.variables = variables
        self.arguments = arguments
        self.fig = None
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5)

    def did_press_home(self, *args):
        self.redraw_plot()

    def add_plot_figure(self, fig):
        self.fig = fig
        self.mpl_canvas = FigureCanvasTkAgg(fig, self)
        self.mpl_canvas.show()
        self.mpl_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        NavigationToolbar2.home = self.did_press_home

        self.toolbar = NavigationToolbar2TkAgg(self.mpl_canvas, self)
        self.toolbar.configure(bg='white')
        self.toolbar.update()
        self.mpl_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def redraw_plot(self):
        if self.fig == None: return
        self.load_data_and_draw(figure=self.fig)
        self.mpl_canvas.draw()
        self.toolbar.update()

    def load_data_and_draw(self, figure):
        self.load_data()
        figure.redraw(data=self.data)