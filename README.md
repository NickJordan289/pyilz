# Pyilz - An Illuvium Zero Python library

[![build-status-image]][build-status]
[![pypi-version]][pypi]
[![coverage-status-image]][codecov]

# Overview
This package hopes to make automation and management of Illuvium Zero Land a little easier by allowing you to interact with the gamestate APIs.

As the current Alpha version has no server-side authority the methods implemented only perform reads as to not break your gamestate.

This library **CAN** be used while you have the game running as it uses your local machines **[device_id](/pyilz/get_device_id.py)**, without this your game client would log-out due to different devices running the same plot.

*Currently only supports Windows as replicating the **[get_device_id](/pyilz/get_device_id.py)** implementation from the Unity game engine requires WMI.*

# Installation

Install using `pip`...

    pip install pyilz


# Requirements

* Python 3.7+
* Your Cognito access_token or refresh_token [*See below*](#acquiring-a-cognito-access_token)

Tokens can either be passed into the [**get_game_state**](/pyilz/get_game_state.py) function or pulled from the environment variables if available.

## Environment Variables
```
REFRESH_TOKEN=...
ACCESS_TOKEN=...
```

### Acquiring your Cognito tokens
---
At the time of writing this there is no way of generating application scoped access tokens so the only way to authenticate against the gamestate APIs is by logging into https://play.illuvium.io/ and retrieving the tokens from local storage.

**DO NOT** share your refresh_token or access_token, the refresh_token can generate new access_tokens for up to 30 days.

### Example of tokens in Chromium Local Storage
![access_tokens.png](/images/access_tokens.png)


# Example
```py
from pyilz.get_token import get_token
from pyilz.get_game_state import get_game_state
from pyilz.parse_land import parse_land, get_buildings_and_activities
from pyilz.get_timers import get_timers
from pyilz.get_buildings import get_building_storage, get_active_output, get_passive_output
from pyilz.get_plots import get_plot_metadata

# Load ACCESS_TOKEN and REFRESH_TOKEN env vars
import dotenv
dotenv.load_dotenv()

# Get access token
token = get_token()

# Get list of plots
plots = get_game_state(token)['data']

# Get the second plot in game state
plot = plots[2]['data']
landId = plots[2]['landId']

# Look up metadata to get region and tier
metadata = get_plot_metadata(landId)
tier = metadata['tier']
region = metadata['region']

# Get Paths, Buildings, Current, Automatic and Completed Actions
building_data = parse_land(plot)
paths, buildings, ca, aa, completed = get_buildings_and_activities(building_data)

# Get timers from actions
timers = get_timers(ca, aa, completed)

# Get total storage
storage = get_storage(building_data, tier)

# Get the output from active and passive actions
hydrogen_pump_5_active = get_active_output("Hydrogen Pump", level=5, tier=tier, efficiency=150)
sequestrian_plant_5_passive = get_passive_output("Sequestrian Plant", level=5, tier=tier, efficiency=150)
```

# Package management
### Build
```ps
py -m pip install --upgrade build
py -m build
```

### Release
```ps
py -m pip install --upgrade twine
py -m twine upload --repository pypi dist/*
```

[build-status-image]: https://github.com/nickjordan289/pyilz/actions/workflows/main.yml/badge.svg
[build-status]: https://github.com/nickjordan289/pyilz/actions/workflows/main.yml
[coverage-status-image]: https://img.shields.io/codecov/c/github/nickjordan289/pyilz/master.svg
[codecov]: https://codecov.io/github/nickjordan289/pyilz?branch=main
[pypi-version]: https://img.shields.io/pypi/v/pyilz.svg
[pypi]: https://pypi.org/project/pyilz/