import json
import math
import importlib.resources
import json

with importlib.resources.open_text("pyilz", "buildings.json") as file:
    buildings = json.load(file)['buildings']


def get_active_output(name, level, tier, efficiency=100):
    name = name.lower().replace(' ', '').replace('_', '')
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
    name = name.lower().replace(' ', '').replace('_', '')
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
