from math import sqrt, acos, sin, cos
from random import randint

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
    
def get_distance_bt_units(unit, other):
    a = unit.x, unit.y
    b = other.x, other.y
    return get_distance(a, b)

def get_angle_in_radians(origin, destination):
    d = get_distance(destination, origin)
    if not d:
        return 0
    else:
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

def get_equilateral_vertices(origin, radius):
    # the sides of a 30 degree right triangle are 1 : sqrt(3) : 2
    x, y = origin
    a = radius/2
    bottom_left = [x - a*sqrt(3), y - a]
    bottom_right = [x + a*sqrt(3), y - a]
    top_center = [x, y + radius]
    return bottom_left + bottom_right + top_center
    
def apply_point_rotation_matrix(d_theta, point, origin):
    x, y = point
    a, b = origin
    return (x*cos(d_theta) - y*sin(d_theta)) + a, (x*sin(d_theta) + y*cos(d_theta)) + b

def rotate_triangle(origin, radius, rotation, location):
    original_vertices = get_equilateral_vertices(origin, radius)
    v1 = original_vertices[0], original_vertices[1]
    v2 = original_vertices[2], original_vertices[3]
    v3 = original_vertices[4], original_vertices[5]
    old_vertices = [v1, v2, v3]
    new_vertices = []
    for v in old_vertices:
        new_vertices.extend(list(apply_point_rotation_matrix(rotation, v, location)))
    return new_vertices
    
def get_rand_RGBs(lower=0, upper=255):
    return (randint(lower, upper), randint(lower, upper), randint(lower, upper))

def get_dot_product(V1, V2):
    return V1[0]*V2[0] + V1[1]*V2[1]
    
def get_average_location(unit_list):
    a, b = 0, 0
    for u in unit_list:
        a += u.x
        b += u.y
    return a/len(unit_list), b/len(unit_list)
    