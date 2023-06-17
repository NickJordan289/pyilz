from pyilz.get_game_state import get_game_state
from pyilz.parse_land import parse_land
from pyilz.get_plots import get_plot_metadata
import dotenv
import json

dotenv.load_dotenv()
def nft_to_iz(x,y):
    x = int(x)
    y = int(y)
    num = x - 24
    num2 = -(y-25)
    num3 = -num
    x = num2 + 24
    y = num3 + 25
    return x,y
#plot = get_plot_metadata("16263")
reference_data = json.load(open('reference_data.json', 'r'))
def get_building_reference_data(building_name):
    buildings = reference_data['buildings']
    if building_name in buildings:
        building = buildings[building_name]
        img = None
        if 'img' in building:
            img = building['img']
        return building['w'], building['h'], img
    else:
        print(building_name, 'not in reference data')
        return 2, 2, None
state = parse_land(get_game_state()['data'][1]['data'])
output = ""
for k, v in state.iterrows():
    x,y = nft_to_iz(v['position']['@x'],v['position']['@y'])
    w,h,img = get_building_reference_data(v['buildingTypeString'][:-2])
    x = x-(h-2)
    y = y-(w-2)
    output += f"[\"{v['buildingTypeString']}\",{y},{x}],"
output = f'[{output[:-1]}]'
print(output)
#import code; code.interact(local=dict(globals(), **locals()))