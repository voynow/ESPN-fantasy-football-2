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


def exe():
        
    # preparation
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    raw_data = split_on_newline(raw_data)
    
    # transformation
    transformation_functions = {
        'header': header_fn
    }
    for k, data in raw_data.items():
        grouped_data = group(data)
        for group_name in grouped_data:
            if group_name in transformation_functions:
                tarnsformation = transformation_functions[group_name]
                grouped_data[group_name] = tarnsformation(grouped_data[group_name])
                raw_data[k] = grouped_data

    # restructure
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    # save
    with open(semistructured_loc, "w") as f:
        json.dump(master_raw_data, f, indent=4)
        