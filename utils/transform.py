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

    
season_stats_col_names = {
    'base': [        
        'season', 
        'team', 
        'games_played', 
        'FPts',
        'FPts/G'
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


def header_fn(header):
    
    header = header[2:]

    position_team = header.pop(0).split(", ")
    position_team.append("")
    (pos, team) = position_team[:2]

    draft_class_replace_tuples = (" ", "_"), (":_",": "), ("(", ""), (")", "")
    for t in draft_class_replace_tuples:
        header[0] = header[0].replace(*t)
    header.append(header.pop().replace("  ", " "))

    header.append(f'pos: {pos.lower()}')
    header.append(f'team: {team.lower()}')

    header_key_values = [item.replace(": ", " ").split(" ") for item in header]

    header_dict_collection = {}
    for row in header_key_values:
        for i, item in enumerate(row):
            if i % 2:
                header_dict_collection[key] = item.lower()
            else:
                key = item.lower()

    return header_dict_collection


def season_stats_fn(season_stats_raw, pos):

    season_stats = []
    while season_stats_raw[-1].split(" ")[0].isnumeric():
        season_stats.append(season_stats_raw.pop())

    season_stats.reverse()

    season_stats[-1] = season_stats[-1].replace("2022 (Projected)", "2022(Projected)")

    for i in range(len(season_stats)):
        season_stats[i] = [item for item in season_stats[i].split(" ") if item]

    season_stats[-1] = season_stats[-1][:2] + [None] + season_stats[-1][2:]

    columns = season_stats_col_names['base'] + season_stats_col_names[pos]
    season_stats_json = {col: [] for col in columns}
    for row in season_stats:
        for col, item in zip(season_stats_json, row):
            season_stats_json[col].append(item)
    
    return season_stats_json


def exe():
        
    # preparation
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    raw_data = split_on_newline(raw_data)
    
    # transformation
    transformation_functions = {
        'header': header_fn,
        'season_stats': season_stats_fn,
    }
    for k, data in raw_data.items():
        grouped_data = group(data)
        for group_name in grouped_data:
            if group_name in transformation_functions:
                tarnsformation = transformation_functions[group_name]
                if group_name == 'season_stats':
                    pos = grouped_data['header']['pos']
                    grouped_data[group_name] = tarnsformation(grouped_data[group_name], pos)
                else:
                    grouped_data[group_name] = tarnsformation(grouped_data[group_name])
                raw_data[k] = grouped_data

    # restructure
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    # save
    with open(semistructured_loc, "w") as f:
        json.dump(master_raw_data, f, indent=4)
        