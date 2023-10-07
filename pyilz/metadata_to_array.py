from pyilz.get_game_state import get_game_state
from pyilz.parse_land import parse_land
from pyilz.get_plots import get_plot_metadata
import json
import importlib.resources

with importlib.resources.open_text("pyilz", "reference_data.json") as file:
    reference_data = json.load(file)

def nft_to_iz(x, y):
    """
    Converts NFT coordinates to Iz dimensions.

    Args:
        x (int): The x-coordinate of the NFT.
        y (int): The y-coordinate of the NFT.

    Returns:
        tuple: A tuple containing the x and y coordinates in Iz dimensions.
    """
    x = int(x)
    y = int(y)
    num = x - 24
    num2 = -(y-25)
    num3 = -num
    x = num2 + 24
    y = num3 + 25
    return x, y


def get_building_reference_data(building_name):
    """
    Returns the width, height, and image of a building from the reference data.

    Args:
        building_name (str): The name of the building to retrieve data for.

    Returns:
        tuple: A tuple containing the width (int), height (int), and image (str or None) of the building.
    """
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


def metadata_to_array(gamestate):
    """
    Converts gamestate metadata to an array of building data.

    Args:
        gamestate (dict): The gamestate metadata.

    Returns:
        str: A string representation of the array of building data.
    """
    state = parse_land(gamestate)
    output = ""
    for k, v in state.iterrows():
        x, y = nft_to_iz(v['position']['@x'], v['position']['@y'])
        w, h, img = get_building_reference_data(v['buildingTypeString'][:-2])
        x = x-(h-2)
        y = y-(w-2)
        output += f"[\"{v['buildingTypeString']}\",{y},{x}],"
    output = f'[{output[:-1]}]'
    return output


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()
    print(metadata_to_array(get_game_state()['data'][1]['data']))
