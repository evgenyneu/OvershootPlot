import tkinter as tk

def show_option_menu(container, row, column, text, default_index, command,
        variable, variables):
    # Label
    options_label = tk.Label(container, text=text, bg='white')
    options_label.grid(row=row,column=column,sticky=tk.W, padx=5, pady=5)
    variable.set(variables[default_index])

    option_menu = tk.OptionMenu(container, variable, *variables, command=command)
    option_menu.config(bg="white", width=18)
    option_menu.grid(row=row,column=column+1,sticky=tk.EW, padx=5, pady=5)

    return option_menu


def show_option_menu_wit_default_value(container, row, column, text, default_value, command,
        variable, variables):

    index_value = 0

    try:
        index_value = variables.index(default_value)
    except ValueError:
        index_value = 0

    return show_option_menu(container=container, row=row, column=column, text=text,
        default_index=index_value, command=command, variable=variable, variables=variables)

