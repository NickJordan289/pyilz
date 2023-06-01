import pandas as pd
import pytz
import pyilz.parse_land as parse_land


def get_timers_from_state(gamestate):
    _, _, ca, aa, completed = parse_land.parse_land(gamestate)
    return get_timers(ca, aa, completed)


def get_timers(ca, aa, completed, init=False):
    timers = {}
    if ca is not None:
        for i, row in ca.iterrows():
            end_time = row['currentActivity.EndTime'].replace(
                tzinfo=pytz.utc)
            cur_time = pd.Timestamp.now(tz='utc')
            diff_minutes = (end_time - cur_time).total_seconds() / 60

            # Calculate percentage based on currentActivity.StartTime and currentActivity.EndTime
            start_time = row['currentActivity.StartTime'].replace(
                tzinfo=pytz.utc)
            total_time = (end_time - start_time).total_seconds() / 60
            elapsed_time = (cur_time - start_time).total_seconds() / 60
            percentage = elapsed_time / total_time * 100

            notified = False
            if init and diff_minutes <= 0:
                notified = True
            timers[f'{row["uid"]}-current'] = {'uid': row['uid'], 'name': row['buildingTypeString'],
                                               'type': row['currentActivity.Type'], 'minutes': diff_minutes, 'notified': notified, 'percentage': percentage}

    if aa is not None:
        for i, row in aa.iterrows():
            end_time = row['autoActivity.EndTime'].replace(tzinfo=pytz.utc)
            cur_time = pd.Timestamp.now(tz='utc')
            diff_minutes = (end_time - cur_time).total_seconds() / 60

            # Calculate percentage based on currentActivity.StartTime and currentActivity.EndTime
            start_time = row['autoActivity.StartTime'].replace(
                tzinfo=pytz.utc)
            total_time = (end_time - start_time).total_seconds() / 60
            elapsed_time = (cur_time - start_time).total_seconds() / 60
            percentage = elapsed_time / total_time * 100

            # if row['buildingTypeString'] in ['SEQUESTRIAN_PLANT_4', 'PHOTODISINTEGRATION_PLANT_4', 'CONDENSER_PLANT_4']:
            #    percentage = (int(row['autoActivity.GeneratedResources']) / 7500) * 100

            notified = False
            if init and diff_minutes <= 0:
                notified = True
            timers[f'{row["uid"]}-auto'] = {'uid': row['uid'], 'name': row['buildingTypeString'],
                                            'type': row['autoActivity.Type'], 'minutes': diff_minutes, 'notified': notified, 'percentage': percentage}

    if completed is not None:
        for i, row in completed.iterrows():
            end_time = row['completedActivity.EndTime'].replace(
                tzinfo=pytz.utc)
            cur_time = pd.Timestamp.now(tz='utc')
            diff_minutes = (end_time - cur_time).total_seconds() / 60

            # Calculate percentage based on currentActivity.StartTime and currentActivity.EndTime
            start_time = row['completedActivity.StartTime'].replace(
                tzinfo=pytz.utc)
            total_time = (end_time - start_time).total_seconds() / 60
            elapsed_time = (cur_time - start_time).total_seconds() / 60
            percentage = elapsed_time / total_time * 100

            # if row['buildingTypeString'] in ['SEQUESTRIAN_PLANT_4', 'PHOTODISINTEGRATION_PLANT_4', 'CONDENSER_PLANT_4']:
            #    percentage = (int(row['completedActivity.GeneratedResources']) / 7500) * 100

            notified = False
            if init and diff_minutes <= 0:
                notified = True
            timers[f'{row["uid"]}-current'] = {'uid': row['uid'], 'name': row['buildingTypeString'],
                                               'type': row['completedActivity.Type'], 'minutes': diff_minutes, 'notified': notified, 'percentage': percentage}

    # sort by minutes
    timers = {k: v for k, v in sorted(
        timers.items(), key=lambda item: item[1]['minutes'])}
    return timers
