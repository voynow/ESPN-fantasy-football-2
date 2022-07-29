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


def exe():
        
    # preparation
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    
    # transformation
    raw_data = split_on_newline(raw_data)
    for k, data in raw_data.items():  
        raw_data[k] = group(data)

    # restructure
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    # save
    with open(semistructured_loc, "w") as f:
        json.dump(master_raw_data, f, indent=4)
        