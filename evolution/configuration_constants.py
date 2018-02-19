# Names that are used as options when running the plotter.
from shared.configuration_constants import OVERSHOOT_DIRECTION_IN, OVERSHOOT_DIRECTION_OUT, CONVECTIVE_ZONE_CORE, CONVECTIVE_ZONE_ENVELOPE, CONVECTIVE_ZONE_SHELL

variables_y = {
    'convection_r_rsun': {
        'description': 'Convection r (Radius/Rsun)'
    },
    'convection_r_m': {
        'description': 'Convection r (m)'
    },
    'overshoot_r_rsun': {
        'description': 'Overshoot r (Radius/Rsun)'
    },
    'overshoot_r_m': {
        'description': 'Overshoot r (m)'
    },
    'overshoot_dr_rsun': {
        'description': 'Overshoot dr (Radius/Rsun)'
    },
    'overshoot_dr_m': {
        'description': 'Overshoot dr (m)'
    },

    'convection_m_msun': {
        'description': 'Convection m (Mass/Msun)'
    },
    'convection_m_g': {
        'description': 'Convection m (g)'
    },
    'overshoot_m_msun': {
        'description': 'Overshoot m (Mass/Msun)'
    },
    'overshoot_m_g': {
        'description': 'Overshoot m (g)'
    },
    'overshoot_dm_msun': {
        'description': 'Overshoot dm (Mass/Msun)'
    },
    'overshoot_dm_g': {
        'description': 'Overshoot dm (g)'
    },
    'zones': {
        'description': 'Total convective zones',
        'shared_among_zones': True
    },
}

variables_x = {
    'time_s': {
        'description': 'Time (s)'
    },
    'time_year': {
        'description': 'Time (year)'
    },
    'model': {
        'description': 'Model number'
    }
}

convective_zone_types = {
    'all': {
        'description': 'All zone types',
        'direction': {
            OVERSHOOT_DIRECTION_IN: {
                'color': ['r'],
                'linestyle': '-'
            },
            OVERSHOOT_DIRECTION_OUT: {
                'color': ['r'],
                'linestyle': ':'
            }
        },
        'label': 'all'
    },
    CONVECTIVE_ZONE_CORE: {
        'description': 'Core',
        'direction': {
            OVERSHOOT_DIRECTION_IN: {
                'color': ['r'],
                'linestyle': '-'
            },
            OVERSHOOT_DIRECTION_OUT: {
                'color': ['r'],
                'linestyle': ':'
            }
        },
        'label': 'Core'
    },
    CONVECTIVE_ZONE_ENVELOPE: {
        'description': 'Envelope',
        'direction': {
            OVERSHOOT_DIRECTION_IN: {
                'color': ['#5578ff','#ff3c00'],
                'linestyle': '-'
            },
            OVERSHOOT_DIRECTION_OUT: {
                'color': ['#012cc7','#af2900'],
                'linestyle': ':'
            }
        },
        'label': 'Evelope'
    },
    CONVECTIVE_ZONE_SHELL: {
        'description': 'Shell',
        'direction': {
            OVERSHOOT_DIRECTION_IN: {
                'color': ['#e9b101','#cf00ee'],
                'linestyle': '-'
            },
            OVERSHOOT_DIRECTION_OUT: {
                'color': ['#ad8301','#8a009e'],
                'linestyle': ':'
            }
        },
        'label': 'Shell'
    }
}

overshoot_directions = {
    'both': {
        'description': 'Both'
    },
    OVERSHOOT_DIRECTION_IN: {
        'description': 'Overshoot in'
    },
    OVERSHOOT_DIRECTION_OUT: {
        'description': 'Overshoot out'
    }
}