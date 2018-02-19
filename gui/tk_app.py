import tkinter as tk

class TkApp(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def create_ui(self):
        self.graph_page.load_data_and_draw(figure=self.fig)
        self.graph_page.add_plot_figure(self.fig)
        self.fig.tight_layout()