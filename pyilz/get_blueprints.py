import importlib.resources
import json
with importlib.resources.open_text("pyilz", "reference_data.json") as file:
    biodata_mapping = json.load(file)['biodata']

def _name_to_common(name):
    return biodata_mapping.get(name, None)

def _name_to_dict(name):
    name = name.split('_')
    type = name[0]
    tier = int(name[1])
    stage = int(name[2])
    illuvial_name = _name_to_common('_'.join(name[3:]))
    return {'name': illuvial_name, 'type': type, 'tier': tier, 'stage': stage}
    
def _clean_biodata(biodata):
    data = []
    for bio in biodata:
        bio = bio['value']['BiodataData']['biodataTypeId']
        data.append(_name_to_common(bio))
    return data

def _clean_blueprint_collection(blueprint_collection):
    blueprints = []
    for blueprint in blueprint_collection:
        blueprint = blueprint['value']['BlueprintData']['blueprintTypeId']
        blueprints.append(_name_to_dict(blueprint))
    return blueprints