import math
from get_buildings import get_building_dimensions, get_building_starting_efficiency, get_building_radius


def calculate_efficiency(building_a_pos, building_a_wxh, building_b_pos, building_b_wxh, base_efficiency=80, power=20, radius=7, debuff=False):
    """
    Calculates the efficiency of a building based on its position, size, and distance from another building.

    Args:
        building_a_pos (tuple): The position of the first building as a tuple of (x, y) coordinates.
        building_a_wxh (tuple): The width and height of the first building as a tuple of (width, height).
        building_b_pos (tuple): The position of the second building as a tuple of (x, y) coordinates.
        building_b_wxh (tuple): The width and height of the second building as a tuple of (width, height).
        base_efficiency (int, optional): The base efficiency of the building. Defaults to 80.
        power (int, optional): The power of the building. Defaults to 20.
        radius (int, optional): The radius of the building. Defaults to 7.
        debuff (bool, optional): Whether the building has a debuff. Defaults to False.

    Returns:
        int: The efficiency of the building as an integer.
    """
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
    """
    Calculates the minimum distance between two buildings given their positions and shapes.

    Args:
        building_a_pos (tuple): The position of the first building as a tuple of (x, y) coordinates.
        building_a_shape (list): A list of tuples representing the shape of the first building.
        building_b_pos (tuple): The position of the second building as a tuple of (x, y) coordinates.
        building_b_shape (list): A list of tuples representing the shape of the second building.
        radius (int, optional): The radius within which to search for points. Defaults to 6.

    Returns:
        float: The minimum distance between the two buildings, or None if the minimum points are not within the radius of building_a.
    """
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
    """
    Returns a list of unique points within a given radius of an origin point, 
    taking into account the shape of the object being measured.

    Args:
    - origin (tuple): A tuple containing the x and y coordinates of the origin point.
    - shape (list): A list of tuples containing the x and y coordinates of each point in the shape.
    - radius (int): The radius within which to search for points. Default is 6.

    Returns:
    - list: A list of unique points within the given radius of the origin point.
    """
    x0, y0 = origin
    points = set()
    for dx in range(-radius, radius+1):
        for dy in range(-radius, radius+1):
            for x, y in shape:
                point = (x0 + x + dx, y0 + y + dy)
                points.add(point)
    return list(points)


def get_building_points(building_pos, building_shape):
    """
    Returns a list of points representing the building's shape, given its position and shape.

    Args:
        building_pos (tuple): The (x, y) position of the building.
        building_shape (list): A list of (x, y) tuples representing the shape of the building.

    Returns:
        list: A list of (x, y) tuples representing the points that make up the building's shape.
    """
    x0, y0 = building_pos
    points = [(x0 + x, y0 + y) for x, y in building_shape]
    return points


# define the influence values for each building combination
# anything not defined is assumed 0
influence_values = {
    ('CONDENSER_PLANT', 'HYDROGEN_PUMP'): 30,  # MATCHING RESOURCE
    ('CONDENSER_PLANT', 'LAKE'): 30,  # MATCHING RESOURCE
    ('CONDENSER_PLANT', 'POWER_STATION'): 20,  # POWER
    ('CONDENSER_PLANT', 'SEQUESTRIAN_PLANT'): -10,  # OTHER CONVERTER
    ('CONDENSER_PLANT', 'PHOTODISINTEGRATION_PLANT'): -10,  # OTHER CONVERTER
    ('CONDENSER_PLANT', 'CONDENSER_PLANT'): -40,  # SAME BUILDING

    ('SEQUESTRIAN_PLANT', 'SEDIMENT_EXCAVATOR'): 30,  # MATCHING RESOURCE
    ('SEQUESTRIAN_PLANT', 'OUTCROP'): 30,  # MATCHING RESOURCE
    ('SEQUESTRIAN_PLANT', 'POWER_STATION'): 20,  # POWER
    ('SEQUESTRIAN_PLANT', 'PHOTODISINTEGRATION_PLANT'): -10,  # OTHER CONVERTER
    ('SEQUESTRIAN_PLANT', 'CONDENSER_PLANT'): -10,  # OTHER CONVERTER
    ('SEQUESTRIAN_PLANT', 'SEQUESTRIAN_PLANT'): -40,  # BUILDING

    ('PHOTODISINTEGRATION_PLANT', 'MINE'): 30,  # MATCHING RESOURCE
    ('PHOTODISINTEGRATION_PLANT', 'SILICON_MOUND'): 30,  # MATCHING RESOURCE
    ('PHOTODISINTEGRATION_PLANT', 'POWER_STATION'): 20,  # POWER
    ('PHOTODISINTEGRATION_PLANT', 'SEQUESTRIAN_PLANT'): -10,  # OTHER CONVERTER
    ('PHOTODISINTEGRATION_PLANT', 'CONDENSER_PLANT'): -10,  # OTHER CONVERTER
    ('PHOTODISINTEGRATION_PLANT', 'PHOTODISINTEGRATION_PLANT'): -40,  # BUILDING

    ('ANTI-SOLON_INVERTER', 'SOLON_DREDGE'): 30,  # MATCHING RESOURCE
    ('ANTI-SOLON_INVERTER', 'SOLON_TRENCH'): 30,  # MATCHING RESOURCE
    ('ANTI-SOLON_INVERTER', 'POWER_STATION'): 10,  # POWER
    ('ANTI-SOLON_INVERTER', 'L-CRYPTON_COLLIDER'): -30,  # OTHER CONVERTER
    ('ANTI-SOLON_INVERTER', 'HYPERION_LATHE'): -30,  # OTHER CONVERTER
    ('ANTI-SOLON_INVERTER', 'ANTI-SOLON_INVERTER'): -60,  # SAME BUILDING

    ('L-CRYPTON_COLLIDER', 'CRYPTON_GATE'): 30,  # MATCHING RESOURCE
    ('L-CRYPTON_COLLIDER', 'CRYPTON_RIFT'): 30,  # MATCHING RESOURCE
    ('L-CRYPTON_COLLIDER', 'POWER_STATION'): 10,  # POWER
    ('L-CRYPTON_COLLIDER', 'HYPERION_LATHE'): -30,  # OTHER CONVERTER
    ('L-CRYPTON_COLLIDER', 'ANTI-SOLON_INVERTER'): -30,  # OTHER CONVERTER
    ('L-CRYPTON_COLLIDER', 'L-CRYPTON_COLLIDER'): -60,  # SAME BUILDING

    ('HYPERION_LATHE', 'HYPERION_RESERVOIR'): 30,  # MATCHING RESOURCE
    ('HYPERION_LATHE', 'HYPERION_EXTRACTOR'): 30,  # MATCHING RESOURCE
    ('HYPERION_LATHE', 'POWER_STATION'): 10,  # POWER
    ('HYPERION_LATHE', 'ANTI-SOLON_INVERTER'): -30,  # OTHER CONVERTER
    ('HYPERION_LATHE', 'L-CRYPTON_COLLIDER'): -30,  # OTHER CONVERTER
    ('HYPERION_LATHE', 'HYPERION_LATHE'): -60,  # SAME BUILDING

    ('MARKETPLACE', 'POWER_STATION'): 20,

    ('HYDROGEN_PUMP', 'POWER_STATION'): 20,  # POWER
    ('SEDIMENT_EXCAVATOR', 'POWER_STATION'): 20,  # POWER
    ('MINE', 'POWER_STATION'): 20,  # POWER

    ('MATERIALS_LAB', 'DATA_BANK'): 30,
    ('MATERIALS_LAB', 'POWER_STATION'): 20,
    ('MATERIALS_LAB', 'MATERIALS_LAB'): -10,

    ('ZERO_POINT_TRANSDUCER', 'POWER_STATION'): 20,
    ('SINGULARITY_SCANNER', '*'): -10,
}

# get the other building's influence on this building


def get_power_influence(this, other):
    """
    Calculates the power influence between two buildings based on their building types.

    Args:
        this (dict): A dictionary containing information about the first building.
        other (dict): A dictionary containing information about the second building.

    Returns:
        float: The power influence between the two buildings.
    """
    inf = influence_values.get(
        (this['buildingTypeString'][:-2], other['buildingTypeString'][:-2]), None)
    if not inf:
        inf = influence_values.get((this['buildingTypeString'][:-2], '*'), 0)
    return inf


def import_string_to_array(string):
    """
    Converts a string representation of an array of building types and their coordinates
    into a list of dictionaries, where each dictionary represents a building type and its coordinates.

    Args:
    string (str): A string representation of an array of building types and their coordinates.
                  The string should be in the format '[buildingTypeString1, X1, Y1, buildingTypeString2, X2, Y2, ...]'

    Returns:
    list: A list of dictionaries, where each dictionary represents a building type and its coordinates.
          Each dictionary has the keys 'buildingTypeString', 'X', and 'Y'.
    """
    s = string.replace('[', '').replace(']', '').replace(
        '"', '').replace(' ', '').split(',')
    return [{'buildingTypeString': s[i], 'X':int(s[i+1]), 'Y':int(s[i+2])} for i in range(0, len(s), 3)]


def compute(import_string, printing=False):
    """
    Computes the efficiency of each building in the import_string based on its power influence and proximity to other buildings.

    Args:
        import_string (list): A list of dictionaries containing information about each building.
        printing (bool, optional): Whether to print the intermediate steps of the computation. Defaults to False.

    Returns:
        list: A list of dictionaries containing the name and efficiency of each building.
    """
    IGNORE_LIST = ['POWER_STATION', 'HYDROGEN_MATTER_SILO', 'ENGINEERING_WORKSHOP',
                   'NEXUS', 'SILICON_MATTER_SILO', 'QUANTUM_FABRICANT', 'CARBON_MATTER_SILO']
    IGNORE_LIST_2 = ['HYDROGEN_MATTER_SILO', 'ENGINEERING_WORKSHOP',
                     'NEXUS', 'SILICON_MATTER_SILO', 'QUANTUM_FABRICANT', 'CARBON_MATTER_SILO']
    output = []
    for building in import_string:
        name = building['buildingTypeString']
        if name[:-2] in IGNORE_LIST:
            continue
        w, h = get_building_dimensions(name[:-2])
        wxh = (w, h)
        eff = default_efficiency = get_building_starting_efficiency(name[:-2])
        radius = get_building_radius(name[:-2])
        if printing and name != 'POWER_STATION_1':
            print(f'--- {name} - {eff} -{w}x{h}---')
        for building2 in import_string:
            name2 = building2['buildingTypeString']
            if name2[:-2] in IGNORE_LIST_2:
                continue
            w2, h2 = get_building_dimensions(name2[:-2])
            wxh2 = (w2, h2)
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
        '[["SOLON_CONTAINMENT_UNIT_1",35,18],["POWER_STATION_1",10,16],["HYDROGEN_MATTER_SILO_5",27,5],["HYDROGEN_PUMP_5",31,31],["MINE_5",35,27],["SEDIMENT_EXCAVATOR_4",35,31],["NEXUS_7",42,22],["ENGINEERING_WORKSHOP_5",25,11],["HYDROGEN_MATTER_SILO_5",24,2],["CARBON_MATTER_SILO_5",24,5],["PHOTODISINTEGRATION_PLANT_4",35,23],["CARBON_MATTER_SILO_5",24,8],["POWER_STATION_1",2,22],["SILICON_MATTER_SILO_5",21,8],["SEQUESTRIAN_PLANT_5",9,28],["CONDENSER_PLANT_4",27,39],["QUANTUM_FABRICANT_4",22,11],["POWER_STATION_1",15,22],["POWER_STATION_1",6,29],["CARBON_MATTER_SILO_5",32,11],["POWER_STATION_1",32,28],["SILICON_MATTER_SILO_5",29,11],["SEQUESTRIAN_PLANT_4",34,34],["POWER_STATION_1",13,32],["POWER_STATION_1",13,22],["L-CRYPTON_COLLIDER_3",9,19],["CONDENSER_PLANT_5",5,21],["PHOTODISINTEGRATION_PLANT_5",13,25],["POWER_STATION_1",32,26],["POWER_STATION_1",9,22],["POWER_STATION_1",11,22],["POWER_STATION_1",6,18],["POWER_STATION_1",11,32],["CARBON_MATTER_SILO_5",27,8],["HYDROGEN_MATTER_SILO_5",30,8],["ANTI-SOLON_INVERTER_2",38,31],["L-CRYPTON_COLLIDER_2",28,28],["CARBON_MATTER_SILO_5",18,8],["SINGULARITY_SCANNER_1",23,45],["CARBON_MATTER_SILO_5",21,5],["CARBON_MATTER_SILO_5",19,11],["CONDENSER_PLANT_5",13,18],["CRYPTON_CONTAINMENT_UNIT_2",35,14],["HYPERION_CONTAINMENT_UNIT_2",39,18],["SEQUESTRIAN_PLANT_4",31,22],["CARBON_MATTER_SILO_5",16,11],["POWER_STATION_1",28,25],["MATERIALS_LAB_1",13,29],["HYPERION_RESERVOIR_1",9,25],["HYPERION_LATHE_1",6,25]]')
    compute(import_string, printing=True)
    import timeit
    print('Original Method Finished:', timeit.timeit('compute(import_string, printing=True)',
                                                     setup='from __main__ import compute, import_string', number=1))
