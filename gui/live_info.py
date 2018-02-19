from decimal import Decimal
from shared.parse_data import variable_with_name

def find_model_from_xvalue(xvalue, models, variable_name):
    xvalue = int(round(xvalue))

    selected_model = None
    increasing = models[0]['model'] < models[-1]['model']
    for model in models:
        value = model[variable_name]
        if increasing:
            if xvalue > value: selected_model = model
        else:
            if xvalue < value: selected_model = model

    return selected_model

def live_info_for_model(model):
    model_number = model['model']
    zones = model['zones']
    info = f'Model={model_number}, Zones={zones}'
    return info

def live_info_file_name():
    return "overshoot_communicate12386432.tmp"

def view_mode_details(model_number, file):
    with open(live_info_file_name(), "w") as text_file:
        print(f'file={file} model_number={model_number}', file=text_file)

def read_live_info_data():
    try:
        with open(live_info_file_name()) as f:
            line = f.readline()
            file = variable_with_name(line, 'file')
            model_number = int(variable_with_name(line, 'model_number'))
            return file, model_number
    except IOError:
        return None, None
