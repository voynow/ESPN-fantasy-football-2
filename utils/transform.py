import json

raw_loc = 'data/raw.json'
semistructured_loc = 'data/semistructured.json'

structure_strings = [
    '2021 Gamelog Stats', 
    '2020 Gamelog Stats', 
    '2019 Gamelog Stats', 
    'Season Stats'
]


def exe():
        
    master_raw_data = json.load(open(raw_loc, 'rb'))

    raw_data = {k: v['data'] for k, v in master_raw_data.items()}

    for key in raw_data:
        raw_data[key] = raw_data[key].split("\n\n")

    for key in raw_data:
        data_split = []
        for item in raw_data[key]:
            data_split.append(item.split("\n"))
        raw_data[key] = data_split

    for key, value in raw_data.items():        
        player_dict = {}
        player_dict['pos_team'] = value[0][-1].split(", ")
        player_dict['general'] = value[2]

        for item in value:
            for string in structure_strings:
                if item[0] == string:
                    string_key = string.replace(" ", "_").lower()
                    player_dict[string_key] = item

        raw_data[key] = player_dict


    with open(semistructured_loc, "w") as f:
        json.dump(raw_data, f, indent=4)
        