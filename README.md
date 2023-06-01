# pyilz

[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

**Illuvium Zero python library**

# Overview
# Requirements

* Python 3.7+
# Installation

Install using `pip`...

    pip install pyilz


# Example
```py
from pyilz import get_token, get_game_state, parse_land, get_timers

# Load ACCESS_TOKEN and REFRESH_TOKEN env vars
import dotenv
dotenv.load_dotenv()

# Get access token
token = get_token.get_token()

# Get list of plots
plots = get_game_state.get_game_state(token)

# Get Current, Automatic and Completed Actions
land = plots[2]['data']
_, _, ca, aa, completed = parse_land.parse_land(land)

# Get timers from actions
timers = get_timers.get_timers(ca, aa, completed)
print(timers)
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