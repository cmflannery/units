""" conversions.py provides unit conversion for units.py """

conversion_units = {
    'm': 'm',
    'km': 'm',
    'in': 'm',
    'ft': 'm',
    'yd': 'm',
    'mi': 'm',
    'kg': 'kg',
    'g': 'kg',
    'lbm': 'kg',
    'slug': 'kg',
    'N': 'N',
    's': 's',
    'min': 's',
    'h': 's'
}
conversion_factors = {
    'm': 1.0,
    'km': 1000,
    'in': 0.0254,
    'ft': 0.3048,
    'yd': 0.9144,
    'mi': 1609.34,
    'kg': 1.0,
    'g': 0.001,
    'lbm': 0.4536,
    'slug': 14.5939,
    'N': 1.0,
    's': 1.0,
    'min': 60,
    'h': 3600
}
conversion_units_IM = {
    'm': 'ft',
    'kg': 'lbm',
    'N': 'lbf',
    's': 's'
}
conversion_factors_IM = {
    'm': 3.2808,
    'kg': 2.2046,
    'N': 0.2248,
    's': 1.0
}
