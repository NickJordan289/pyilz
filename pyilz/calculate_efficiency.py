import math


def calculate_efficiency(building_a_pos, building_a_wxh, building_b_pos, building_b_wxh, base_efficiency=80, power=20, radius=7, debuff=False):
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
            if distance < min_distance:
                min_distance = distance
                min_a = a
                min_b = b
    
    # Check if minimum points are within radius of building_a
    if min_a in p_a and min_b in p_b:
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
#def get_minimum_distance_between_buildings(building_a_pos, building_a_shape, building_b_pos, building_b_shape, radius=6):
#    # pre-calculate shape positions
#    a_positions = [(building_a_pos[0] + x, building_a_pos[1] + y)
#                   for (x, y) in building_a_shape]
#    b_positions = [(building_b_pos[0] + x, building_b_pos[1] + y)
#                   for (x, y) in building_b_shape]
#
#    # sort the shapes by x-coordinate
#    a_positions.sort(key=lambda pos: pos[0])
#    b_positions.sort(key=lambda pos: pos[0])
#
#    # initialize variables
#    min_distance = float('inf')
#    min_a = (0, 0)
#    min_b = (0, 0)
#
#    # loop over the shapes
#    a_idx = 0
#    b_idx = 0
#    while a_idx < len(a_positions) and b_idx < len(b_positions):
#        # check x-coordinate difference
#        x_diff = b_positions[b_idx][0] - a_positions[a_idx][0]
#        if x_diff >= min_distance:
#            break
#
#        # calculate distance
#        distance = math.dist(a_positions[a_idx], b_positions[b_idx])
#
#        # update minimum distance and points
#        if distance < min_distance:
#            min_distance = distance
#            min_a = a_positions[a_idx]
#            min_b = b_positions[b_idx]
#
#        # move to next shape
#        if a_positions[a_idx][0] < b_positions[b_idx][0]:
#            a_idx += 1
#        else:
#            b_idx += 1
#
#    # check if minimum points are within radius of building_a
#    p = get_points_in_radius(building_a_pos, building_a_shape, radius)
#    import pdb;pdb.set_trace()
#    if min_a in p and min_b in p:
#        return min_distance
#    return None



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
}

# get the other building's influence on this building


def get_power_influence(this, other):
    building_types = (this['buildingTypeString'][:-2],
                      other['buildingTypeString'][:-2])
    return influence_values.get(building_types, 0)

def import_string_to_array(string):
    s = string.replace('[','').replace(']','').replace('"','').replace(' ','').split(',')
    return [{'buildingTypeString':s[i],'X':int(s[i+1]),'Y':int(s[i+2])} for i in range(0,len(s),3)]
    

if __name__ == '__main__':
    import_string = import_string_to_array('[["HYDROGEN_PUMP_2",6,23],["CONDENSER_PLANT_1",7,26],["POWER_STATION_1",9,23],["POWER_STATION_1",4,26]]')
    for building in import_string:
        name = building['buildingTypeString']
        default_efficiency = 80
        wxh = (2,2)
        radius = 6
        if name == 'HYDROGEN_PUMP_2':
            default_efficiency = 100
        if name == 'CONDENSER_PLANT_1':
            wxh = (3,3)
            radius = 7
        eff = default_efficiency
        for building2 in import_string:
            name2 = building2['buildingTypeString']
            wxh2 = (2,2)
            if name == 'CONDENSER_PLANT_1':
                wxh = (3,3)
            if building != building2:
                infl = get_power_influence(building, building2)
                diff = calculate_efficiency((building['X'], building['Y']), wxh,
                                             (building2['X'], building2['Y']), (2, 2),base_efficiency=default_efficiency,power=infl,radius=radius)-default_efficiency
                eff += diff
                #code.interact(local=dict(globals(), **locals()))
                #code.interact(local=dict(globals(), **locals()))
                #print(name,name2,diff)
                #print(diff)
        if name != 'POWER_STATION_1':
            print(name,eff, default_efficiency)
    
    # print('Running tests')
    # assert math.floor(calculate_efficiency((42, 19), (2, 2),
    #                  (33, 10), (3, 3))) == 82  # Furthest Diagonal
    # assert math.floor(calculate_efficiency((33, 19), (2, 2),
    #                  (33, 10), (3, 3))) == 87  # Furthest Vertical
    # assert math.floor(calculate_efficiency((33, 20), (2, 2),
    #                  (33, 10), (3, 3))) == 80  # Out of range Vertical
    # assert math.floor(calculate_efficiency((33, 13), (2, 2),
    #                  (33, 10), (3, 3))) == 100  # Adjacent Vertical
    # assert math.floor(calculate_efficiency((31, 8), (2, 2),
    #                  (33, 10), (3, 3))) == 99  # Adjacent Diagonal
    # assert math.floor(calculate_efficiency((43, 20), (2, 2),
    #                  (33, 10), (3, 3))) == 80  # Out of range Diagonal
    # Multi Power Station Test
    # power_stations = [(34, 13), (34, 15)]
    # target = (33, 10)
    # power = 80
    # for ps in power_stations:
    #    power = calculate_efficiency(ps, (2, 2), target, (3, 3), power)
    # assert math.floor(power) == 115
    # print('All tests passed')
