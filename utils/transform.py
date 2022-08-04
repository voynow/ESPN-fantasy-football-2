from curses import raw
import json
from turtle import position

raw_loc = 'data/raw.json'
semistructured_loc = 'data/semistructured.json'


structure_strings = [
    '2021 Gamelog Stats', 
    '2020 Gamelog Stats', 
    '2019 Gamelog Stats', 
    'Season Stats'
]

    
season_stats_map = {
    'base_prefix': [        
        'season', 
        'team', 
        'games_played',
    ],

    'base_suffix': [ 
        'fpts',
        'fpts/G',
    ],

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
        'rushing_att',
        'rushing_yard',
        'rushing_avg',
        'rushing_td',
    ],

    'kicker': [
        'fgm', 
        'fga', 
        'fg%', 
        'epm', 
        'epa'
    ]
}


gamelog_stats_map = {
    'base_prefix': [        
        'week', 
        'opp', 
        'result',
        'score'
    ],

    'base_suffix': [ 
        'FPts',
    ],

    'quarterback': [
        'cmp', 
        'passing_att', 
        'cmp%', 
        'passing_yard', 
        'passing_td', 
        'int'
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


def split_on_newline(raw_data):

    for key in raw_data:
        raw_data[key] = raw_data[key].split("\n\n")

    for key in raw_data:
        data_split = []
        for item in raw_data[key]:
            data_split.append(item.split("\n"))
        raw_data[key] = data_split

    return raw_data


def group(data):
    
    player_dict = {}

    player_dict['header'] = data[0] + data[2]

    for row in data:
        for string in structure_strings:
            if row[0] == string:
                string_key = string.replace(" ", "_").lower()
                player_dict[string_key] = row
    
    return player_dict


def header_fn(data):

    header_raw = data['header']
    
    header_raw = header_raw[2:]

    position_team = header_raw.pop(0).split(", ")
    position_team.append("")
    (pos, team) = position_team[:2]

    draft_class_replace_tuples = (" ", "_"), (":_",": "), ("(", ""), (")", "")
    for t in draft_class_replace_tuples:
        header_raw[0] = header_raw[0].replace(*t)
    header_raw.append(header_raw.pop().replace("  ", " "))

    header_raw.append(f'pos: {pos.lower()}')
    header_raw.append(f'team: {team.lower()}')

    header_key_values = [item.replace(": ", " ").split(" ") for item in header_raw]

    header_dict_collection = {}
    for row in header_key_values:
        for i, item in enumerate(row):
            if i % 2:
                header_dict_collection[key] = item.lower()
            else:
                key = item.lower()

    data['header'] = header_dict_collection
    return data


def season_stats_fn(data):

    season_stats_raw = data['season_stats']
    pos = data['header']['pos']

    season_stats = []
    while season_stats_raw[-1].split(" ")[0].isnumeric():
        season_stats.append(season_stats_raw.pop())

    season_stats.reverse()

    season_stats[-1] = season_stats[-1].replace("2022 (Projected)", "2022(Projected)")

    for i in range(len(season_stats)):
        season_stats[i] = [item for item in season_stats[i].split(" ") if item]

    season_stats[-1] = season_stats[-1][:2] + [None] + season_stats[-1][2:]

    columns = season_stats_map['base_prefix'] + season_stats_map[pos] + season_stats_map['base_suffix']
    season_stats_json = {col: [] for col in columns}
    for row in season_stats:
        for col, item in zip(season_stats_json, row):
            season_stats_json[col].append(item)
    
    data['season_stats'] = season_stats_json
    return data


def gamelog_stats_fn(data, table_name):

    gamelog_raw = data[table_name]
    pos = data['header']['pos']

    gamelog = [row.replace('at ', '@').split(" ") for row in gamelog_raw[4:]]
    if "=" in gamelog[-1]:
        gamelog.pop()

    columns = gamelog_stats_map['base_prefix'] + gamelog_stats_map[pos] + gamelog_stats_map['base_suffix']
    gamelog_json = {col: [] for col in columns}
    for row in gamelog:
        for col, item in zip(gamelog_json, row):
            gamelog_json[col].append(item)
    
    data[table_name] = gamelog_json
    return data


def gamelog_stats_2021_fn(data): return gamelog_stats_fn(data, '2021_gamelog_stats')
def gamelog_stats_2020_fn(data): return gamelog_stats_fn(data, '2020_gamelog_stats')
def gamelog_stats_2019_fn(data): return gamelog_stats_fn(data, '2019_gamelog_stats')


def exe():
        
    # preparation
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    raw_data = split_on_newline(raw_data)
    
    # transformation
    transformation_functions = {
        'header': header_fn,
        'season_stats': season_stats_fn,
        '2021_gamelog_stats': gamelog_stats_2021_fn,
        '2020_gamelog_stats': gamelog_stats_2020_fn,
        '2019_gamelog_stats': gamelog_stats_2019_fn,
    }
    for k, data in raw_data.items():
        grouped_data = group(data)
        for group_name in grouped_data:
            if group_name in transformation_functions:
                tarnsformation = transformation_functions[group_name]
                grouped_data = tarnsformation(grouped_data)
                raw_data[k] = grouped_data

    # restructure
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    # save
    with open(semistructured_loc, "w") as f:
        json.dump(master_raw_data, f, indent=4)
        