from math import sqrt, acos, sin, cos

def transform_vertex_list(dx, dy, primitive):
    i = 0
    for v in primitive.vertices:
        if not i % 2:
            v += dx
            primitive.vertices[i] = v
        else:
            v += dy
            primitive.vertices[i] = v
        i += 1

def get_distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_angle_in_radians(origin, destination):
    return acos((origin[0]-destination[0])/get_distance(destination, origin))
    
def get_xy_from_vector(angle, distance):
    return distance * cos(angle), distance * sin(angle)
    
def one_step_toward_destination(destination, origin, distance):
    approach_angle = get_angle_in_radians(origin, destination)
    dx, dy = get_xy_from_vector(approach_angle, distance)
    if destination[1] < origin[1]:
        dy *= -1
    return -dx, dy
    
def find_units_in_circle(center, radius, unit_list):
    units = []
    for u in unit_list:
        if get_distance(center, (u.x, u.y)) < radius:
            units.append(u)
    return units

