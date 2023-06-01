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
