from utils import configs


def stats_to_json(stats, columns):
    """
    Helper function to convert 2D list into JSON with columns names
    """
    stats_json = {col: [] for col in columns}
    for row in stats:
        for col, item in zip(stats_json, row):
            stats_json[col].append(item)
    return stats_json
    

def header_fn(data):
    """
    
    """
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
    """
    
    """
    season_stats_raw = data['season_stats']
    pos = data['header']['pos']

    season_stats = []
    while season_stats_raw[-1].split(" ")[0].isnumeric():
        season_stats.append(season_stats_raw.pop())

    season_stats.reverse()

    season_stats[-1] = season_stats[-1].replace("2022 (Projected)", "2022(Projected)")

    for i, data in enumerate(season_stats):
        season_stats[i] = [item for item in data.split(" ") if item]

    season_stats[-1] = season_stats[-1][:2] + [None] + season_stats[-1][2:]

    prefix = configs.season_stats['prefix_cols']
    suffix = configs.season_stats['suffix_cols']
    columns = prefix + configs.col_names[pos] + suffix

    data['season_stats'] = stats_to_json(season_stats, columns)
    return data


def gamelog_stats_fn(data, table_name):
    """
    
    """
    gamelog_raw = data[table_name]
    pos = data['header']['pos']

    gamelog_stats = [row.replace('at ', '@').split(" ") for row in gamelog_raw[4:]]
    if "=" in gamelog_stats[-1]:
        gamelog_stats.pop()

    prefix = configs.gamelog_stats['prefix_cols']
    suffix = configs.gamelog_stats['suffix_cols']
    columns = prefix + configs.col_names[pos] + suffix

    data[table_name] = stats_to_json(gamelog_stats, columns)
    return data


def gamelog_stats_2021_fn(data): 
    """
    
    """
    return gamelog_stats_fn(data, '2021_gamelog_stats')


def gamelog_stats_2020_fn(data): 
    """
    
    """
    return gamelog_stats_fn(data, '2020_gamelog_stats')


def gamelog_stats_2019_fn(data): 
    """
    
    """
    return gamelog_stats_fn(data, '2019_gamelog_stats')
