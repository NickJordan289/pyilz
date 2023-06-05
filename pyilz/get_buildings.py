import json
import math
with open('./pyilz/buildings.json', 'r') as f:
    buildings = json.load(f)['buildings']

def list_buildings():
    for building in buildings:
        details = building['details']
        for detail in details:
            level = detail['level']
            time = detail['time']
            image = detail['image']
            requires = detail['requires']
            activities = detail['activities'] if 'activities' in detail else {}
            if 'passive' not in activities:
                print(building['name'],level,'NO PASSIVE')
            if 'active' not in activities:
                print(building['name'],level,'NO ACTIVE')
            cost = detail['cost']
            for c in cost:
                resource = c['resource']
                amount = c['amount']

def get_active_output(name, level, tier, efficiency=100):
    land_tier_bonus_multiplier_percent = [0,0,33.33333333333,100,300,900]
    for building in buildings:
        if building['name'] == name:
            details = building['details']
            for detail in details:
                if detail['level'] == level:
                    activities = detail['activities']
                    active = activities['active']
                    amount = int(active['amount'])                    
                    return math.ceil((amount * efficiency / 100) * (1 + (land_tier_bonus_multiplier_percent[tier] / 100)))

if __name__ == '__main__':
    #list_buildings()
    hydrogen_pump = get_active_output('Hydrogen Pump', 5, 2, 150)
    seq = get_active_output('Sequestrian Plant', 6, 2, 150)
    
    import code; code.interact(local=dict(globals(), **locals()))