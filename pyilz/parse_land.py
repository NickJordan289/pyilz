# Import the required modules
import pandas as pd
import xmltodict


def parse_land(data):
    '''Returns a pandas dataframe of the land.'''
    data = xmltodict.parse(data)
    building_data = data['SaveGameData']['Buildings']['BuildingData']
    building_data = pd.DataFrame(building_data)
    return building_data


def get_buildings_and_activities(df):
    '''Returns a tuple of paths, buildings, current activities, auto activities, and completed activities.

    These are all pandas dataframes.
    '''
    # convert position column from {'@x': '38', '@y': '17'} to '38,17'
    df['position'] = df['position'].apply(lambda x: x['@x'] + ',' + x['@y'])
    # split position column into x and y columns
    df[['x', 'y']] = df['position'].str.split(',', expand=True)
    # set x and y to int
    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)
    df = df.drop(columns=['position'])

    paths = df[df['buildingTypeString'] == 'PATH']
    # drop all columns except for position
    paths = paths[['x', 'y']]

    # Drop all rows where buildingTypeString is PATH
    buildings = df[df['buildingTypeString'] != 'PATH']

    if 'currentActivity' in buildings.columns:
        # get rows where currentActivity is not null
        ca = buildings[buildings['currentActivity'].notnull()]

        # unpack json column currentActivity
        current_activity_cols = pd.json_normalize(
            ca['currentActivity']).set_index(ca.index)
        ca = ca.join(current_activity_cols.add_prefix(
            'currentActivity.'), how='outer')
        ca = ca.drop(columns=['currentActivity'])
        # convert currentActivity.StartTime and currentActivity.EndTime to datetime
        ca['currentActivity.StartTime'] = pd.to_datetime(
            ca['currentActivity.StartTime'])
        ca['currentActivity.EndTime'] = pd.to_datetime(
            ca['currentActivity.EndTime'])
        # remove _{number} from currentActivity.Type and put into column currentActivity.Level
        ca['currentActivity.Level'] = ca['currentActivity.Type'].str.extract(
            r'_(\d+)', expand=False).fillna(0).astype(int)
        ca['currentActivity.Type'] = ca['currentActivity.Type'].str.replace(
            r'_(\d+)', '', regex=True)

    else:
        ca = None

    if 'autoActivity' in buildings.columns:
        # get rows where autoActivity is not null
        aa = buildings[buildings['autoActivity'].notnull()]

        # unpack json column autoActivity
        auto_activity_cols = pd.json_normalize(
            aa['autoActivity']).set_index(aa.index)
        aa = aa.join(auto_activity_cols.add_prefix(
            'autoActivity.'), how='outer')
        aa = aa.drop(columns=['autoActivity'])
        # convert autoActivity.StartTime and autoActivity.EndTime to datetime
        aa['autoActivity.StartTime'] = pd.to_datetime(
            aa['autoActivity.StartTime'])
        aa['autoActivity.EndTime'] = pd.to_datetime(aa['autoActivity.EndTime'])
        # remove _{number} from autoActivity.Type and put into column autoActivity.Level
        aa['autoActivity.Level'] = buildings['buildingTypeString'].str.extract(
            r'(\d+)$', expand=False).fillna(0).astype(int)
        aa['autoActivity.Type'] = buildings['buildingTypeString'].str.extract(
            r'(.+?)\d+$', expand=False).str.rstrip('_') + '_AUTOMATIC'
        # aa['autoActivity.GeneratedResources'] = buildings['fractionalGeneratedResources']
    else:
        aa = None

    if 'completedActivity' in buildings.columns:
        # get rows where completedActivity is not null
        completed = buildings[buildings['completedActivity'].notnull()]

        # unpack json column completedActivity
        auto_activity_cols = pd.json_normalize(
            completed['completedActivity']).set_index(completed.index)
        completed = completed.join(auto_activity_cols.add_prefix(
            'completedActivity.'), how='outer')
        completed = completed.drop(columns=['completedActivity'])
        # convert completedActivity.StartTime and completedActivity.EndTime to datetime
        completed['completedActivity.StartTime'] = pd.to_datetime(
            completed['completedActivity.StartTime'])
        completed['completedActivity.EndTime'] = pd.to_datetime(
            completed['completedActivity.EndTime'])
        # remove _{number} from completedActivity.Type and put into column completedActivity.Level
        completed['completedActivity.Level'] = buildings['buildingTypeString'].str.extract(
            r'(\d+)$', expand=False).fillna(0).astype(int)
        completed['completedActivity.Type'] = buildings['buildingTypeString'].str.extract(
            r'(.+?)\d+$', expand=False).str.rstrip('_') + '_AUTOMATIC'
        # completed['completedActivity.GeneratedResources'] = buildings['fractionalGeneratedResources']
    else:
        completed = None

    # drop columns uid, state, startTime
    buildings = buildings.drop(columns=[
        'uid', 'state', 'startTime',
    ])

    # convert generatedResources to int
    if 'generatedResources' in buildings.columns:
        buildings['generatedResources'] = buildings['generatedResources'].astype(
            int)

    # create column that is the last number of the buildingTypeString
    buildings['level'] = buildings['buildingTypeString'].str.extract(r'(\d+)$',
                                                                     expand=False)

    buildings['name'] = buildings['buildingTypeString'].str.extract(
        r'(.+?)\d+$', expand=False).str.rstrip('_')

    # if name is nan set name to buildingTypeString
    buildings['name'] = buildings['name'].fillna(
        buildings['buildingTypeString'])
    buildings['level'] = buildings['level'].fillna(0)

    buildings = buildings.drop(columns=['buildingTypeString'])

    return paths, buildings, ca, aa, completed
