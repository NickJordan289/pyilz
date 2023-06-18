from itertools import product
import math
import time


def calculate_efficiency(building_a_pos, building_a_wxh, building_b_pos, building_b_wxh, base_efficiency=80, power=20, radius=7, debuff=False):
    if power < 0:
        debuff = True
    building_a_shape = [(i, j) for i in range(building_a_wxh[0])
                        for j in range(building_a_wxh[1])]
    building_b_shape = [(i, j) for i in range(building_b_wxh[0])
                        for j in range(building_b_wxh[1])]
    dist_min = get_minimum_distance_between_buildings(
        building_a_pos, building_a_shape, building_b_pos, building_b_shape, radius)

    if dist_min is None:
        return base_efficiency

    radius_diagonal = math.dist((0, 0), (radius, radius))
    dist_factor = power / radius_diagonal

    efficiency = power - (dist_min - 1) * dist_factor
    if not debuff and efficiency > power:
        efficiency = power
    efficiency += base_efficiency

    if not debuff and efficiency < base_efficiency:
        return base_efficiency
    return efficiency


def get_minimum_distance_between_buildings(building_a_pos, building_a_shape, building_b_pos, building_b_shape, radius=6):
    # Pre-calculate shape positions
    a_positions = get_building_points(building_a_pos, building_a_shape)
    b_positions = get_building_points(building_b_pos, building_b_shape)

    # Initialize variables
    min_distance = float('inf')
    min_a = (0, 0)
    min_b = (0, 0)

    # Calculate all points within radius for both buildings
    p_a = get_points_in_radius(building_a_pos, building_a_shape, radius)
    p_b = get_points_in_radius(building_b_pos, building_b_shape, radius)

    # Find minimum distance between buildings
    for a in a_positions:
        for b in b_positions:
            distance = math.dist(a, b)
            if distance < min_distance and a != b:
                min_distance = distance
                min_a = a
                min_b = b

    # print(f'\t\t{min_distance} {min_a} {min_b}')
    # Check if minimum points are within radius of building_a
    if min_a in p_a and min_b in p_b and min_b in p_a:
        return min_distance
    return None


def get_points_in_radius(origin, shape, radius=6):
    x0, y0 = origin
    points = set()
    for dx in range(-radius, radius+1):
        for dy in range(-radius, radius+1):
            for x, y in shape:
                point = (x0 + x + dx, y0 + y + dy)
                points.add(point)
    return list(points)


def get_building_points(building_pos, building_shape):
    x0, y0 = building_pos
    points = [(x0 + x, y0 + y) for x, y in building_shape]
    return points


# define the influence values for each building combination
# anything not defined is assumed 0
influence_values = {
    # POWER STATION DOES NOT HAVE EFFICIENCY
    ('POWER_STATION', 'SEQUESTRIAN_PLANT'): 0,

    ('SEQUESTRIAN_PLANT', 'POWER_STATION'): 20,  # POWER
    ('SEQUESTRIAN_PLANT', 'SEQUESTRIAN_PLANT'): -40,  # SELF
    ('SEQUESTRIAN_PLANT', 'PHOTODISINTEGRATION_PLANT'): -10,  # OTHER CONVERTER
    ('SEQUESTRIAN_PLANT', 'CONDENSER_PLANT'): -10,  # OTHER CONVERTER
    ('SEQUESTRIAN_PLANT', 'OUTCROP'): 30,  # MATCHING RESOURCE
    ('SEQUESTRIAN_PLANT', 'SEDIMENT_EXCAVATOR'): 30,  # MATCHING RESOURCE

    ('PHOTODISINTEGRATION_PLANT', 'POWER_STATION'): 20,  # POWER
    ('PHOTODISINTEGRATION_PLANT', 'PHOTODISINTEGRATION_PLANT'): -40,  # SELF
    ('PHOTODISINTEGRATION_PLANT', 'SEQUESTRIAN_PLANT'): -10,  # OTHER CONVERTER
    ('PHOTODISINTEGRATION_PLANT', 'CONDENSER_PLANT'): -10,  # OTHER CONVERTER
    ('PHOTODISINTEGRATION_PLANT', 'SILICON_MOUND'): 30,  # MATCHING RESOURCE
    ('PHOTODISINTEGRATION_PLANT', 'MINE'): 30,  # MATCHING RESOURCE

    ('CONDENSER_PLANT', 'POWER_STATION'): 20,  # POWER
    ('CONDENSER_PLANT', 'CONDENSER_PLANT'): -40,  # SELF
    ('CONDENSER_PLANT', 'SEQUESTRIAN_PLANT'): -10,  # OTHER CONVERTER
    ('CONDENSER_PLANT', 'PHOTODISINTEGRATION_PLANT'): -10,  # OTHER CONVERTER
    ('CONDENSER_PLANT', 'LAKE'): 30,  # MATCHING RESOURCE
    ('CONDENSER_PLANT', 'HYDROGEN_PUMP'): 30,  # MATCHING RESOURCE

    ('HYDROGEN_PUMP', 'POWER_STATION'): 20,  # POWER
    ('SEDIMENT_EXCAVATOR', 'POWER_STATION'): 20,  # POWER
    ('MINE', 'POWER_STATION'): 20,  # POWER
}

# get the other building's influence on this building


def get_power_influence(this, other):
    building_types = (this['buildingTypeString'][:-2],
                      other['buildingTypeString'][:-2])
    return influence_values.get(building_types, 0)


def import_string_to_array(string):
    s = string.replace('[', '').replace(']', '').replace(
        '"', '').replace(' ', '').split(',')
    return [{'buildingTypeString': s[i], 'X':int(s[i+1]), 'Y':int(s[i+2])} for i in range(0, len(s), 3)]


def compute(import_string, printing=False):
    IGNORE_LIST = ['POWER_STATION', 'HYDROGEN_MATTER_SILO', 'ENGINEERING_WORKSHOP',
                   'NEXUS', 'SILICON_MATTER_SILO', 'QUANTUM_FABRICANT', 'CARBON_MATTER_SILO']
    IGNORE_LIST_2 = ['HYDROGEN_MATTER_SILO', 'ENGINEERING_WORKSHOP',
                     'NEXUS', 'SILICON_MATTER_SILO', 'QUANTUM_FABRICANT', 'CARBON_MATTER_SILO']
    output = []
    for building in import_string:
        name = building['buildingTypeString']
        if name[:-2] in IGNORE_LIST:
            continue
        default_efficiency = 80
        wxh = (2, 2)
        radius = 6
        if 'HYDROGEN_PUMP' in name or 'MINE' in name or 'SEDIMENT_EXCAVATOR' in name:
            default_efficiency = 100
        if name == 'CONDENSER_PLANT_1' or name == 'PHOTODISINTEGRATION_PLANT_1' or name == 'SEQUESTRIAN_PLANT_1':
            wxh = (3, 3)
            radius = 7
        eff = default_efficiency
        if printing and name != 'POWER_STATION_1':
            print(f'--- {name} - {eff} ---')
        for building2 in import_string:
            name2 = building2['buildingTypeString']
            if name2[:-2] in IGNORE_LIST_2:
                continue
            wxh2 = (2, 2)
            if name2 == 'CONDENSER_PLANT_1' or name == 'PHOTODISINTEGRATION_PLANT_1' or name == 'SEQUESTRIAN_PLANT_1':
                wxh2 = (3, 3)
            if building != building2:
                infl = get_power_influence(building, building2)
                diff = calculate_efficiency((building['X'], building['Y']), wxh,
                                            (building2['X'], building2['Y']), wxh2, base_efficiency=default_efficiency, power=infl, radius=radius)-default_efficiency
                eff += diff
                if printing and diff > 0:
                    print(f'\t{diff} from {name2}')
        if eff > 150:
            eff = 150
        output.append({
            'name': name,
            'efficiency': eff
        })
        if printing and name != 'POWER_STATION_1':
            print(f'Final Efficiency: {eff:.0f}\n')
    return output


if __name__ == '__main__':
    import_string = import_string_to_array(
        '[["CRYSTAL_LUMITERN_1",2,24],["HYDROGEN_MATTER_SILO_5",14,13],["HYPERION_EXTRACTOR_1",9,25],["HYDROGEN_PUMP_4",31,31],["MINE_3",35,27],["SEDIMENT_EXCAVATOR_3",35,31],["NEXUS_5",27,9],["ENGINEERING_WORKSHOP_5",23,12],["HYDROGEN_MATTER_SILO_5",17,13],["SILICON_MATTER_SILO_4",20,13],["HYDROGEN_MATTER_SILO_5",18,16],["PHOTODISINTEGRATION_PLANT_4",34,23],["HYDROGEN_MATTER_SILO_5",21,16],["HYDROGEN_MATTER_SILO_5",15,16],["SILICON_MATTER_SILO_4",24,16],["SEQUESTRIAN_PLANT_4",8,28],["CONDENSER_PLANT_4",27,33],["QUANTUM_FABRICANT_2",24,8],["POWER_STATION_1",32,28],["POWER_STATION_1",9,22],["ANTI-SOLON_INVERTER_1",15,29],["CARBON_MATTER_SILO_5",24,19],["POWER_STATION_1",6,25],["SILICON_MATTER_SILO_4",21,19],["SEQUESTRIAN_PLANT_4",34,34],["POWER_STATION_1",31,34],["POWER_STATION_1",12,29],["L-CRYPTON_COLLIDER_1",9,19],["CONDENSER_PLANT_4",5,21],["PHOTODISINTEGRATION_PLANT_4",12,25],["POWER_STATION_1",6,18],["POWER_STATION_1",31,26],["POWER_STATION_1",13,22],["POWER_STATION_1",31,36],["POWER_STATION_1",11,22],["HYDROGEN_MATTER_SILO_5",18,19],["HYDROGEN_MATTER_SILO_3",15,19]]')
    import timeit
    print('Original Method Finished:', timeit.timeit('compute(import_string, printing=False)',
                                                     setup='from __main__ import compute, import_string', number=1))
