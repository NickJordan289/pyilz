from pyilz.get_game_state import get_game_state
from pyilz.parse_land import parse_land
from pyilz.get_buildings import get_building_storage


def _get_storage_buildings(df):
    storage_buildings_suffix = ['SILO', 'UNIT']
    # pop off _{number} from buildingTypeString and put into column Level
    df['Level'] = df['buildingTypeString'].str.extract(
        r'_(\d+)', expand=False).fillna(0).astype(int)
    # remove _{number} from buildingTypeString and put into column Type
    df['Type'] = df['buildingTypeString'].str.extract(
        r'(.+?)_\d+$', expand=False).str.rstrip('_')
    # get rows where Type ends with SILO or UNIT
    df = df[df['Type'].str.endswith(tuple(storage_buildings_suffix))]
    return df


def get_storage(tier=1):
    state = get_game_state()
    parse = parse_land(state['data'][2]['data'])
    storage_buildings = _get_storage_buildings(parse)
    storage = {
        'hydrogen': 0,
        'silicon': 0,
        'carbon': 0,
        'crypton': 0,
        'hyperion': 0,
        'solon': 0,
    }
    for _, row in storage_buildings.iterrows():
        amount, resource = get_building_storage(
            row['Type'], row['Level'], tier)
        storage[resource] += amount
    return storage


# def get_resources():
#    return {
#        'Hydrogen': 100000,
#        'Silicon': 100000,
#        'Carbon': 100000,
#        'Crypton': 100000,
#        'Hyperion': 100000,
#        'Solon': 100000,
#    }
