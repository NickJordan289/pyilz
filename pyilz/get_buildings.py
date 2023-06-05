import json
import math
with open('./pyilz/buildings.json', 'r') as f:
    buildings = json.load(f)['buildings']

def find_missing_activities():
    IGNORE_LIST = ['Nexus','Engineering Workshop','Quantum Fabricant','Power Station','Carbon Matter Silo','Silicon Matter Silo','Hydrogen Matter Silo','Crypton Containment Unit','Crypton Containment Unit','Solon Containment Unit','Zero Point Transducer','Data Bank','Holographic Statue','Marketplace']
    for building in buildings:
        if building['name'] in IGNORE_LIST:
            continue
        details = building['details']
        for detail in details:
            level = detail['level']
            time = detail['time']
            image = detail['image']
            requires = detail['requires']
            activities = detail['activities'] if 'activities' in detail else {}
            if 'passive' not in activities:
                print(building['name'],level,'NO PASSIVE')
            else:
                passive = activities['passive']
                if passive:
                    amount = passive['amount']
                    if not amount:
                        print(building['name'],level,'NO PASSIVE')
                else:
                    print(building['name'],level,'NO PASSIVE')
            if 'active' not in activities:
                print(building['name'],level,'NO ACTIVE')
            else:
                active = activities['active']
                if active:
                    amount = active['amount']
                    if not amount:
                        print(building['name'],level,'NO ACTIVE')
                else:
                    print(building['name'],level,'NO ACTIVE')
            cost = detail['cost']
            for c in cost:
                resource = c['resource']
                amount = c['amount']

def get_active_output(name, level, tier, efficiency=100):
    name = name.lower().replace(' ','').replace('_','')
    land_tier_bonus_multiplier_percent = [0,0,33.33333333333,100,300,900]
    for building in buildings: # This should probably be a dict
        if building['nameId'] == name:
            details = building['details']
            for detail in details:
                if detail['level'] == level:
                    activities = detail['activities']
                    active = activities['active']
                    amount = int(active['amount'])                    
                    return math.ceil((amount * efficiency / 100) * (1 + (land_tier_bonus_multiplier_percent[tier] / 100)))

if __name__ == '__main__':
    find_missing_activities()
    #hydrogen_pump = get_active_output('Hydrogen Pump', 5, 2, 150)
    #seq = get_active_output('Sequestrian Plant', 6, 2, 150)
    #import code; code.interact(local=dict(globals(), **locals()))