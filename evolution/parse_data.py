# Functions for parsing the input data file

import collections
import os
from evolution.parse_arguments import parse_arguments
from shared.parse_data import read_model_number, variable_with_name
from shared.evo_string import ordinal
from .parse_data_optimize import get_skip_models

def parse_models(filename, skip_models=None):
    """
    Parses data into the list of models
    """
    models = []

    file_size = os.path.getsize(filename)
    if skip_models == None: skip_models = get_skip_models(file_size)
    if skip_models < 0: skip_models = 0
    models_skipped = -1
    last_read_model = -1

    with open(filename) as f:
        while True:
            line = f.readline()
            if not line: break # end of file

            model_number = read_model_number(line)
            if model_number == None: continue

            if model_number != last_read_model: models_skipped += 1
            if models_skipped > skip_models: models_skipped = 0

            if models_skipped == 0:
                models.append(parse_model(f=f,line=line, model_number=model_number))

            last_read_model = model_number

    return models

def parse_model(f, line,model_number):
    model = {}
    model['model'] = model_number
    model['type'] = variable_with_name(line, 'con zone')
    model['time_s'] = float(variable_with_name(line, 'Time'))
    model['time_year'] = float(variable_with_name(line, 's'))

    # Number of zones
    line = f.readline()
    model['zone_number'] = int(variable_with_name(line, 'Zone'))
    model['zones'] = int(variable_with_name(line, 'Total'))
    model['overshoot_direction'] = variable_with_name(line, 'Osh direction')

    # Overshoot mesh points
    line = f.readline()
    model['overshoot_start'] = int(variable_with_name(line, 'OshStart'))
    model['overshoot_end'] = int(variable_with_name(line, 'OshEnd'))

    # Distance
    line = f.readline()
    model['convection_r_rsun'] = float(variable_with_name(line, '  r'))
    model['convection_r_m'] = float(variable_with_name(line, 'RSun'))
    line = f.readline()
    model['overshoot_r_rsun'] = float(variable_with_name(line, 'Overshoot   r'))
    model['overshoot_r_m'] = float(variable_with_name(line, 'RSun'))
    line = f.readline()
    model['overshoot_dr_rsun'] = float(variable_with_name(line, 'Overshoot  dr'))
    model['overshoot_dr_m'] = float(variable_with_name(line, 'RSun'))

    # Mass
    line = f.readline()
    model['convection_m_msun'] = float(variable_with_name(line, '  m'))
    model['convection_m_g'] = float(variable_with_name(line, 'MSun'))
    line = f.readline()
    model['overshoot_m_msun'] = float(variable_with_name(line, 'Overshoot   m'))
    model['overshoot_m_g'] = float(variable_with_name(line, 'MSun'))
    line = f.readline()
    model['overshoot_dm_msun'] = float(variable_with_name(line, 'Overshoot  dm'))
    model['overshoot_dm_g'] = float(variable_with_name(line, 'MSun'))

    return model