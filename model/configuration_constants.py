# Names that are used as options when running the plotter.
from shared.configuration_constants import OVERSHOOT_DIRECTION_IN, OVERSHOOT_DIRECTION_OUT, CONVECTIVE_ZONE_CORE, CONVECTIVE_ZONE_ENVELOPE, CONVECTIVE_ZONE_SHELL

variables_for_plotting = {
    'j': {
        'description': 'Mesh point',
    },
    'm_msun': {
        'description': 'Mass',
        'units': 'm/Msun'
    },
    'r_rsun': {
        'description': 'Radius',
        'units': 'r/RSun'
    },
    'log_t': {
        'description': 'Temperature',
        'units': 'Log(T)'
    },
    'rho': {
        'description': 'Density',
        'units': '$g/cm^3$'
    },
    'v_cm_s': {
        'description': 'Velocity',
        'units': 'cm/s'
    },
    'log_p': {
        'description': 'Pressure',
        'units': '$\\log{\\frac{g}{cm \\ s^2}}$'
    },

    'abund_h': {
        'description': 'H',
        'units': 'mass fraction'
    },
    'abund_he_3': {
        'description': 'He3',
        'units': 'mass fraction'
    },
    'abund_he_4': {
        'description': 'He4',
        'units': 'mass fraction'
    },
    'abund_c_12': {
        'description': 'C12',
        'units': 'mass fraction'
    },
    'abund_n_14': {
        'description': 'N14',
        'units': 'mass fraction'
    },
    'abund_o_16': {
        'description': 'O16',
        'units': 'mass fraction'
    },
    'abund_rest': {
        'description': 'Other elements',
        'units': 'mass fraction'
    },
}

convective_zone_types = {
    CONVECTIVE_ZONE_CORE: {
        'human_friendly': 'core'
    },
    CONVECTIVE_ZONE_ENVELOPE: {
        'human_friendly': 'evelope'
    },
    CONVECTIVE_ZONE_SHELL: {
        'human_friendly': 'shell'
    }
}

overshoot_directions = {
    OVERSHOOT_DIRECTION_IN: {
        'description': 'Overshoot in'
    },
    OVERSHOOT_DIRECTION_OUT: {
        'description': 'Overshoot out'
    }
}