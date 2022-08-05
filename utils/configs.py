
raw_loc = 'data/raw.json'
structured_loc = 'data/structured.json'


table_names = [
    'header',
    'Season Stats',
    '2021 Gamelog Stats', 
    '2020 Gamelog Stats', 
    '2019 Gamelog Stats', 
]

    
season_stats = {
    'prefix_cols': [        
        'season', 
        'team', 
        'games_played',
    ],

    'suffix_cols': [ 
        'fpts',
        'fpts/G',
    ],
}

gamelog_stats = {
    'prefix_cols': [        
        'week', 
        'opp', 
        'result',
        'score',
    ],

    'suffix_cols': [ 
        'FPts',
    ],
}


col_names = {
    'quarterback': [
        'cmp', 
        'passing_att', 
        'cmp%', 
        'passing_Yard', 
        'passing_td', 
        'int',
        'rushing_att', 
        'rushing_yard', 
        'rushing_avg', 
        'rushing_td',
    ],

    'running': [
        'rushing_att',
        'rushing_yard',
        'rushing_avg',
        'rushing_td',
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
    ],

    'wide': [
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
        'rushing_att',
        'rushing_yard',
        'rushing_avg',
        'rushing_td',
    ],

    'tight': [
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
    ],

    'kicker': [
        'fgm', 
        'fga', 
        'fg%', 
        'epm', 
        'epa'
    ]
}