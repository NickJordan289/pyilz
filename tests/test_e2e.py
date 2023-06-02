import json
from pyilz.parse_land import parse_land
from pyilz.get_timers import get_timers

# Get list of plots
with open('example_game_state.json', 'r') as f:
    plots = json.load(f)['data']

# Get Current, Automatic and Completed Actions
land = plots[2]['data']
_, _, ca, aa, completed = parse_land(land)

# Get timers from actions
timers = get_timers(ca, aa, completed)
print(timers)
