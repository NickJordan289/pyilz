from pyilz.get_buildings import get_building_storage


def _get_storage_buildings(df):
    """
    Returns a filtered DataFrame containing only the storage buildings from the input DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the building data.

    Returns:
        pandas.DataFrame: A filtered DataFrame containing only the storage buildings.
    """
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


def get_storage(parsed_land, tier=1):
    """
    Calculates the total amount of resources that can be stored in the player's storage buildings.

    Args:
        parsed_land (pandas.DataFrame): A DataFrame containing information about the player's land.
        tier (int, optional): The tier of the storage buildings to consider. Defaults to 1.

    Returns:
        dict: A dictionary containing the total amount of each resource that can be stored.
    """
    storage_buildings = _get_storage_buildings(parsed_land)
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
