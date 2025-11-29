"""
Module implementing the color scales
"""

SEA = [
    '#d2ecff',
    '#B8DCF4',
    '#8BC1E3',
    '#5da6d1',
    '#4696C5',
    '#2f86b9',
    '#1876AD',
    '#0066a1',
    '#005383',
    '#004065',
    '#003351',
]

CLAY = [
    '#f9e3de',
    '#F4C7BC',
    '#ec9d8a',
    '#E37258',
    '#d96246',
    '#ce5134',
    '#bc4429',
    '#a9371d',
    '#98321a',
    '#872c17',
    '#651F0F',
    '#7b2815',
]


PLANT = [
    '#e9f0e4',
    '#D3E0C9',
    '#B3C9A0',
    '#A3BE8C',
    '#92B277',
    '#80A064',
    '#6d8e51',
    '#54733d',
    '#4f693a',
    '#495f36',
    '#425631',
]

SAND = [
    '#ffeeba',
    '#f4e1a9',
    '#F2D283',
    '#EFC35D',
    '#E8B847',
    '#e0ad30',
    '#D19E21',
    '#C18E11',
    '#A77A0A',
    '#986F09',
    '#8A6508',
]


EARTH = [
    '#f3e9e5',
    '#e7d3cb',
    '#D5B2A4',
    '#c2907c',
    '#B5806B',
    '#a8705a',
    '#9E6553',
    '#94594C',
    '#804E40',
    '#6c4333',
    '#59372A'
]

GRAY = [
    '#f8f8f8',
    '#f2f2f2',
    '#dcdcdc',
    '#bdbdbd',
    '#989898',
    '#7c7c7c',
    '#656565',
    '#525252',
    '#464646',
    '#3d3d3d',
    '#292929',
]


COLOR_SCALE_MAPPING = {
    'blue': SEA,
    'green': PLANT,
    'red': CLAY,
    'yellow': SAND,
    'brown': EARTH,
    'gray': GRAY,
}
