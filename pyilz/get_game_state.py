import requests
import pyilz.get_device_id as get_device_id
import pyilz.refresh_token as refresh_token
import pyilz.get_token as get_token
import os


def get_game_state(api_key=None, device_id=None):
    """
    Returns a dictionary of the game state. Auth required.

    Args:
        api_key (str): API key for authentication. If None, it will be fetched using get_token.get_token().
        device_id (str): Device ID for authentication. If None, it will be fetched using get_device_id.get_device_id().

    Returns:
        dict: A dictionary containing the game state.
    """
    DEVICE_ID = get_device_id.get_device_id() if device_id is None else device_id
    API_KEY = get_token.get_token() if api_key is None else api_key
    url = f'http://api.illuvium-game.io/gamedata/api/zero/gamestate?active_device_id={DEVICE_ID}'

    response = requests.get(url, headers={'Authorization':
                            'Bearer ' + API_KEY})
    if response.status_code == 401:
        API_KEY = refresh_token.refresh_token()
        response = requests.get(url, headers={'Authorization':
                                              'Bearer ' + API_KEY})
        os.environ['API_KEY'] = API_KEY

    return response.json()
