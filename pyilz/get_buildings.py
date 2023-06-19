import json
import math
import importlib.resources
import json
with importlib.resources.open_text("pyilz", "buildings.json") as file:
    buildings = json.load(file)['buildings']


def get_building_dimensions(name):
    '''Returns the width and height of the specified building.'''
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            return building['width'], building['height']
    return 2, 2


def get_building_starting_efficiency(name):
    '''Returns the starting efficiency of the specified building.'''
    name = name.lower().replace(' ', '').replace('_', '').replace('-', '')
    for building in buildings:  # This should probably be a dict
        if building['nameId'] == name:
            return building['efficiency'] if 'efficiency' in building else 100
    return 100


def get_building_radius(name):
    radius = 6
    if name == 'CONDENSER_PLANT' or name == 'PHOTODISINTEGRATION_PLANT' or name == 'SEQUESTRIAN_PLANT' or name == 'lcryptoncollider' or name == 'antisoloninverter' or name == 'hyperionlathe':
        radius = 7
    if name == 'MATERIALS_LAB':
        radius = 8
    if name == 'MARKETPLACE':
        radius = 12
    return radius


def get_building_storage(name, level, tier):
    '''Returns the storage capacity of the specified building at the specified level and tier.'''
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


def get_active_output(name, level, tier, efficiency=100):
    '''Returns the active output of the specified building at the specified level and tier. Efficiency is a percentage.'''
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


def get_passive_output(name, level, tier, efficiency=100):
    '''Returns the passive output of the specified building at the specified level and tier. Efficiency is a percentage.'''
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
