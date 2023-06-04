import json
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
            cost = detail['cost']
            for c in cost:
                resource = c['resource']
                amount = c['amount']


import code; code.interact(local=dict(globals(), **locals()))