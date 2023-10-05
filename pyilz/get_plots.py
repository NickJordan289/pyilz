import requests
import os
import pyilz.refresh_token as refresh_token
import pyilz.get_token as get_token


def get_my_plots(api_key=None):
    """
    Returns a list of all plots owned by the user. Auth required.

    Args:
        api_key (str, optional): API key for authentication. Defaults to None.

    Returns:
        list: A list of all plots owned by the user.
    """
    API_KEY = get_token.get_token() if api_key is None else api_key
    url = f'http://api.illuvium-game.io/gamedata/api/zero/plots'

    response = requests.get(url, headers={'Authorization':
                            'Bearer ' + API_KEY})
    if response.status_code == 401:
        print('Token expired, refreshing...')
        API_KEY = refresh_token.refresh_token()
        response = requests.get(url, headers={'Authorization':
                                              'Bearer ' + API_KEY})
        os.environ['API_KEY'] = API_KEY

    return response.json()


def get_plot_metadata(land_id):
    """
    Returns a dictionary of metadata for the specified plot.

    Args:
        land_id (int): The ID of the plot to retrieve metadata for.

    Returns:
        dict: A dictionary containing metadata for the specified plot.
    """
    url = f'http://api.illuvium-game.io/gamedata/api/zero/plots/{land_id}/metadata'
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    print(get_plot_metadata(53721))
