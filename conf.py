dmxmidi_conf = {
    'dmx': {
        'lights': {
            'ledbar_1': {'type': 'rgb', 'start_channel': 0},
            'ledbar_2': {'type': 'rgb', 'start_channel': 3},
            'ledbar_3': {'type': 'rgb', 'start_channel': 6},
            'ledbar_4': {'type': 'rgb', 'start_channel': 9},
            'par64_1': {'type': 'rgba', 'start_channel': 12},
            'par64_2': {'type': 'rgba', 'start_channel': 17}
        },
        'array': ['par64_1', 'ledbar_1', 'ledbar_2', 'ledbar_3', 'ledbar_4', 'par64_2'],
        'rgb_colors': {
            'blk': [0, 0, 0],
            'red': [1, 0, 0],
            'grn': [0, 1, 0],
            'yel': [1, 1, 0],
            'blu': [0, 0, 1],
            'mgn': [1, 0, 1],
            'cyn': [0, 1, 1],
            'wht': [1, 1, 1]
        },
        'scenes': [
            ['blk', 'blk', 'blk', 'blk', 'blk', 'blk'],
            ['blu', 'red', 'blu', 'red', 'blu', 'red'],
            ['red', 'blu', 'red', 'blu', 'red', 'blu'],
            ['wht', 'wht', 'wht', 'wht', 'wht', 'wht'],

            ['blu', 'blk', 'blk', 'blk', 'blk', 'blk'],
            ['blk', 'blu', 'blk', 'blk', 'blk', 'blk'],
            ['blk', 'blk', 'blu', 'blk', 'blk', 'blk'],
            ['blk', 'blk', 'blk', 'blu', 'blk', 'blk'],
            ['blk', 'blk', 'blk', 'blk', 'blu', 'blk'],
            ['blk', 'blk', 'blk', 'blk', 'blk', 'blu'],
            ['blu', 'blk', 'blk', 'blk', 'blk', 'blu'],
            ['blk', 'blu', 'blk', 'blk', 'blu', 'blk'],
            ['blk', 'blk', 'blu', 'blu', 'blk', 'blk'],
            ['blu', 'blu', 'blu', 'blu', 'blu', 'blu'],

            ['blu', 'blu', 'blu', 'blu', 'blu', 'blu'],
            ['cyn', 'cyn', 'cyn', 'cyn', 'cyn', 'cyn'],
            ['grn', 'grn', 'grn', 'grn', 'grn', 'grn'],
            ['yel', 'yel', 'yel', 'yel', 'yel', 'yel'],
            ['red', 'red', 'red', 'red', 'red', 'red'],
            ['mgn', 'mgn', 'mgn', 'mgn', 'mgn', 'mgn']

        ],
        'chases': [
            {'division': 4, 'sequence': [0]},
            {'division': 4, 'sequence': [1, 2]},
            {'division': 8, 'sequence': [1, 1, 2, 2]},
            {'division': 4, 'sequence': [1, 0, 2, 0]},
            {'division': 4, 'sequence': [3, 0, 4, 5,  6, 7, 8, 9,  8, 7, 6, 5,  10, 11, 12, 13]},
            {'division': 1, 'sequence': [14, 15, 16, 17, 18, 19]},
            {'division': 1, 'sequence': [14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19]}
        ]
    },
    'midi': {
        'device': 'UM-1',
        'setup': [
            ['note_on', 100, 127],
            ['note_on', 102, 1],
            ['note_on', 71, 127],
            ['note_on', 90, 127],
            ['note_on', 95, 127]
        ],
        'channels': 22,
        'start_note': 73
    },
    'patches' : [
        {'name': 'Cryin', 'tempo': 190},
        {'name': 'Edge of glory', 'tempo': 124},
        {'name': 'Sweet child omine', 'tempo': 126},
        {'name': 'Excited', 'tempo': 182},
        {'name': 'Thriller', 'tempo': 117},
        {'name': 'Beat it', 'tempo': 138},
        {'name': 'Keinu', 'tempo': 70},
        {'name': 'You know my name', 'tempo': 137},
        {'name': 'Beibi', 'tempo': 172},
        {'name': 'Tinakenkätyttö', 'tempo': 140},
        {'name': 'Sata salamaa', 'tempo': 128}
    ]
}