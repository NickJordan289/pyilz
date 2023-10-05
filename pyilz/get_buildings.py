import json
import math
import importlib.resources
import json
with importlib.resources.open_text("pyilz", "buildings.json") as file:
    buildings = json.load(file)['buildings']


def get_building_dimensions(name):
    """
    Returns the width and height of a building with the given name.

    Args:
        name (str): The name of the building.

    Returns:
        tuple: A tuple containing the width and height of the building.
               If the building is not found, returns a tuple with default
               values of 2 for width and height.
    """
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            return building['width'], building['height']
    return 2, 2


def get_building_starting_efficiency(name):
    """
    Returns the starting efficiency of a building with the given name.

    Args:
        name (str): The name of the building.

    Returns:
        int: The starting efficiency of the building, or 100 if not found.
    """
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            return building['efficiency'] if 'efficiency' in building else 100
    return 100


def get_building_radius(name):
    """
    Returns the radius of a building based on its name.

    Args:
        name (str): The name of the building.

    Returns:
        int: The radius of the building.
    """
    radius = 6
    if name == 'CONDENSER_PLANT' or name == 'PHOTODISINTEGRATION_PLANT' or name == 'SEQUESTRIAN_PLANT' or name == 'lcryptoncollider' or name == 'antisoloninverter' or name == 'hyperionlathe':
        radius = 7
    if name == 'MATERIALS_LAB':
        radius = 8
    if name == 'MARKETPLACE':
        radius = 12
    return radius


def get_building_storage(name: str, level: int, tier: int) -> tuple:
    """
    Returns the storage capacity and resource type of a building at a given level and tier.

    Args:
        name (str): The name of the building.
        level (int): The level of the building.
        tier (int): The tier of the land the building is on.

    Returns:
        tuple: A tuple containing the storage capacity (int) and resource type (str) of the building.
    """
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    land_tier_bonus_multiplier_percent = [0, 0, 33.33333333333, 100, 300, 900]
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            details = building['details']
            for detail in details:
                if detail['level'] == level:
                    if 'storage' not in detail:
                        return 0, None
                    storage = detail['storage']
                    if storage is None:
                        return 0, None
                    amount = int(storage['amount'])
                    resource = storage['resource']
                    return math.ceil(amount * (1 + (land_tier_bonus_multiplier_percent[tier] / 100))), resource


def get_active_output(name: str, level: int, tier: int, efficiency: int = 100) -> int:
    """
    Returns the active output of a building with the given name, level, and tier.

    Args:
        name (str): The name of the building.
        level (int): The level of the building.
        tier (int): The tier of the building.
        efficiency (int, optional): The efficiency of the building, defaults to 100.

    Returns:
        int: The active output of the building.
    """
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    land_tier_bonus_multiplier_percent = [0, 0, 33.33333333333, 100, 300, 900]
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            details = building['details']
            for detail in details:
                if detail['level'] == level:
                    activities = detail['activities']
                    active = activities['active']
                    if active is None:
                        return 0
                    amount = int(active['amount'])
                    return math.ceil((amount * efficiency / 100) * (1 + (land_tier_bonus_multiplier_percent[tier] / 100)))


def get_passive_output(name: str, level: int, tier: int, efficiency: int = 100) -> int:
    """
    Calculates the passive output of a building given its name, level, tier, and efficiency.

    Args:
        name (str): The name of the building.
        level (int): The level of the building.
        tier (int): The tier of the building.
        efficiency (int, optional): The efficiency of the building. Defaults to 100.

    Returns:
        int: The calculated passive output of the building. 
    """
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    land_tier_bonus_multiplier_percent = [0, 0, 33.33333333333, 100, 300, 900]
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            details = building['details']
            for detail in details:
                if detail['level'] == level:
                    activities = detail['activities']
                    passive = activities['passive']
                    if passive is None:
                        return 0
                    amount = int(passive['amount'])
                    return math.ceil((amount * efficiency / 100) * (1 + (land_tier_bonus_multiplier_percent[tier] / 100)))


if __name__ == '__main__':
    print('-- Active --')
    print(
        f'Level 5 Hydrogen Pump on Tier 2 Land at 150% efficiency: {get_active_output("Hydrogen Pump", 5, 2, 150)}')
    print(
        f'Level 6 Sequestrian Plant on Tier 2 Land at 150% efficiency: {get_active_output("Sequestrian Plant", 6, 2, 150)}')
    print(
        f'Level 6 Sequestrian Plant on Tier 3 Land at 150% efficiency: {get_active_output("Sequestrian Plant", 6, 3, 150)}')
    print('-- Passive --')
    print(
        f'Level 5 Hydrogen Pump on Tier 2 Land at 150% efficiency: {get_passive_output("Hydrogen Pump", 5, 2, 150)}')
    print(
        f'Level 6 Sequestrian Plant on Tier 2 Land at 150% efficiency: {get_passive_output("Sequestrian Plant", 6, 2, 150)}')
    print(
        f'Level 6 Sequestrian Plant on Tier 3 Land at 150% efficiency: {get_passive_output("Sequestrian Plant", 6, 3, 150)}')
