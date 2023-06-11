import json
from pyilz.parse_land import parse_land, get_buildings_and_activities
from pyilz.get_timers import get_timers
from pyilz.get_resources import get_storage
from pyilz.get_plots import get_plot_metadata


def test_e2e():
    # Get list of plots
    with open('./tests/example_game_state.json', 'r') as f:
        plots = json.load(f)['data']

    land = plots[2]['data']
    landId = plots[2]['landId']
    plot_metadata = get_plot_metadata(landId)
    tier = plot_metadata['tier']
    region = plot_metadata['region']
    building_data = parse_land(land)

    paths, buildings, ca, aa, completed = get_buildings_and_activities(
        building_data)

    # Get timers from actions
    timers = get_timers(ca, aa, completed)

    storage = get_storage(building_data, tier)

    # If no exception, test passed
    assert True


if __name__ == '__main__':
    test_e2e()
