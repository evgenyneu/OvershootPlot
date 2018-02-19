# Functions for parsing a single model from the input data file

from shared.parse_data import read_model_number, variable_with_name, reverse_readline

def find_single_model(filename, model_number, zone_number, overshoot_direction, offset=None):
    with open(filename) as f:
        if offset != None: f.seek(offset)

        while True:
            line = f.readline()
            if not line: break # end of file
            current_model_number = read_model_number(line)
            if current_model_number == None: continue;
            if model_number and current_model_number != model_number: continue;
            model = parse_model(f, current_model_number, line)

            # Match the zone number
            total_zones = model['zones']
            if zone_number < 1 or zone_number > total_zones: return None
            if model['zone_number'] != zone_number: continue

            # Match the overshoot direction
            if model['overshoot_direction'] != overshoot_direction: continue
            return model

    return None # The requested model was not found in the file

def find_first_last_model(filename):
    first_model = None
    last_model = None

    # Find first model number
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line: break # end of file
            current_model_number = read_model_number(line)
            if current_model_number == None: continue
            first_model = current_model_number
            break;

    # Search the file in reverse order to find the last model
    for line in reverse_readline(filename):
        current_model_number = read_model_number(line)
        if current_model_number == None: continue
        last_model = current_model_number
        break;

    return first_model, last_model

def parse_model(f, model_number, line):
    model = {}

    model['model'] = int(variable_with_name(line, 'Nmodel'))
    model['type'] = variable_with_name(line, 'con zone')

     # Number of zones
    line = f.readline()
    model['zone_number'] = int(variable_with_name(line, 'Zone'))
    model['zones'] = int(variable_with_name(line, 'Total'))
    model['overshoot_direction'] = variable_with_name(line, 'Osh direction')

    # Overshoot bounds
    line = f.readline()
    model['overshoot_start'] = int(variable_with_name(line, 'OshStart'))
    model['overshoot_end'] = int(variable_with_name(line, 'OshEnd'))
    model['overtshoot_fix'] = float(variable_with_name(line, 'OshInterp toward CZ'))

    for i in range(7): f.readline() # skip the lines that are not needed

    model['model'] = model_number

    mesh_points = []
    model['mesh_points'] = mesh_points

    # Read the table under the header
    while True:
        line = f.readline()
        if not line: break # end of file
        if line.isspace(): break # end of table
        mesh_point = parse_mesh_point(line)
        mesh_points.append(mesh_point)

    return model

def parse_mesh_point(line):
    mesh_point = {}
    data = line.split()
    mesh_point['j'] = int(data[0])
    mesh_point['type'] = data[1]
    mesh_point['m_msun'] = float(data[2])
    mesh_point['r_rsun'] = float(data[3])
    mesh_point['log_t'] = float(data[4])
    mesh_point['rho'] = float(data[5])
    mesh_point['v_cm_s'] = float(data[6])
    mesh_point['log_p'] = float(data[7])

    # Abundances
    mesh_point['abund_h'] = float(data[8])
    mesh_point['abund_he_3'] = float(data[9])
    mesh_point['abund_he_4'] = float(data[10])
    mesh_point['abund_c_12'] = float(data[11])
    mesh_point['abund_n_14'] = float(data[12])
    mesh_point['abund_o_16'] = float(data[13])
    mesh_point['abund_rest'] = float(data[14])

    return mesh_point
