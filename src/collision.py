import numpy as np
from shape import *
from bodies import *
from copy import deepcopy

def check_collision(a, b, delta):
    a.update_position(delta)
    b.update_position(delta)
    if len(b.shape.points) > len(a.shape.points):
        a, b = b, a
    if isinstance(b.shape, Line):
        ret = ball_line_collision_2(a, b.shape)
    elif isinstance(b.shape, Ball):
        ret = ball_ball_collision(a, b)
    else:
        ret = ball_polygon_collision(a, b)
    a.update_position(-delta)
    b.update_position(-delta)
    return ret
 
def ball_polygon_collision(ball, rect):

    # diff = ball.position - rect.position
    # if diff_size > ball.shape.radius + np.linalg.norm([rect.shape.side_a/2, rect.shape.side_b/2]):
        # return False
    points = rect.shape.get_outside()
    for i in range(len(points)):
        collided, point, normal = ball_line_collision_2(ball, Line(points[i-1],points[i]))
        if collided:
            return collided, point, normal 
    return False, [], []

def ball_ball_collision(a, b):
    diff =  b.position - a.position
    diff_size = np.linalg.norm(diff)
    if diff_size <= a.shape.radius + b.shape.radius:
        norm_diff = diff/diff_size 
        return True, a.position + norm_diff*a.shape.radius, norm_diff
    return False, [], [] 
   
def ball_line_collision_2(ball, l):
    line = l.get_outside()
    org_line = deepcopy(line)
    for point in org_line:
        impact_vector = point - ball.position 
        norm_impact_vector = impact_vector/np.linalg.norm(impact_vector)
        if np.linalg.norm(impact_vector) <= ball.shape.radius:
            return True, point, norm_impact_vector
        
    p = ball.position.copy()
    delta = line[0].copy()
    line -= delta
    p -= delta
    s = line[1]/np.linalg.norm(line[1])
    z = np.dot(p, s)*s
    d = p - z
    distance = np.linalg.norm(d)
    if distance <= ball.shape.radius and np.dot(z, line[1]-z) >= 0:
        normal = line[0] - line[1]
        normal = np.array([normal[1], -normal[0]])
        normal = normal/np.linalg.norm(normal)
        # if np.dot(normal, ball.speed)  < 0:
        #     normal = -normal
        return True, z+delta, normal
    
    return False, [], []

MAX_COLLISION_ITER = 8

def new_collision(a, b, delta_):
    if a.collision != SOLID or b.collision != SOLID:
        return False
      
    best_time = 0
    delta = delta_  
    collided, best_contact_point, best_normal = check_collision(a, b, delta)
    if not collided:
        return False
    time = delta/2
    # print('collision', a, b)
    last_t = collided
    count = 0
    while count <= MAX_COLLISION_ITER: 
        t, contact_point, normal = check_collision(a, b, time)
        delta /= 2
        if t: 
            time -= delta 
            best_normal
            best_contact_point = contact_point
        else:
            best_time = time
            time += delta 
        count += 1
    
    a.update_position(best_time)
    b.update_position(best_time)
    contact_point = best_contact_point 
    normal = best_normal
    a_vector = contact_point - a.position
    a_vector /= np.linalg.norm(a_vector) 
    b_vector = contact_point - b.position
    b_vector /= np.linalg.norm(b_vector) 
    if isinstance(a, DynamicBody) and isinstance(b, DynamicBody):
        a.speed += b_vector*np.dot(b_vector, b.speed) - a_vector*np.dot(a_vector, a.speed)
        b.speed += a_vector*np.dot(a_vector, a.speed) - b_vector*np.dot(b_vector, b.speed)
    elif isinstance(a, DynamicBody) and  isinstance(b, KineticBody):
        if np.dot(a_vector, a.speed) >= 0:
            a.speed = a.speed - 2*a_vector*np.dot(a_vector, a.speed) # + b.speed/np.linalg.norm(b.speed)*np.dot(b_vector, b.speed)
        acting_speed = normal*np.dot(b.speed, normal)
        a.speed[0] = acting_speed[0] if (acting_speed[0] <= 0 and a.speed[0] <= 0 and acting_speed[0] <= a.speed[0]) or (acting_speed[0] >= 0 and a.speed[0] >= 0 and acting_speed[0] >= a.speed[0]) else a.speed[0]
        a.speed[1] = acting_speed[1] if (acting_speed[1] <= 0 and a.speed[1] <= 0 and acting_speed[1] <= a.speed[1]) or (acting_speed[1] >= 0 and a.speed[1] >= 0 and acting_speed[1] >= a.speed[1]) else a.speed[1]
    elif isinstance(a, DynamicBody) and isinstance(b, StaticBody):
        if np.dot(a_vector, a.speed) >= 0:
            a.speed -= 2*normal*np.dot(normal, a.speed)
    
    a.update_position(delta_ - best_time)
    b.update_position(delta_ - best_time)      
    return True
            
    
# def collide_SAT(a, b):
#     a_points = deepcopy(a.shape.get_outside())
#     b_points = deepcopy(b.shape.get_outside())
#     a_lines = np.array([ a_points[i] - a_points[i-1] for i in range(len(a_points)) ])
#     a_lines = a_lines.T/np.linalg.norm(a_lines, axis=1)
#     normals = np.array([-a_lines[1], a_lines[0]])
#     projection_a =  a_points @ normals
#     projection_b =  b_points @ normals
#     min_a = np.min(projection_a,axis=0)
#     max_a = np.max(projection_a,axis=0)
#     min_b = np.min(projection_b,axis=0)
#     max_b = np.max(projection_b,axis=0)
#     b_in_a = np.logical_and(min_a <= projection_b, projection_b <= max_a)
#     b_in_a = np.sum(b_in_a,axis=1) == b_in_a.shape[1]
#     a_in_b = np.logical_and(min_b <= projection_a, projection_a <= max_b)
#     a_in_b = np.sum(a_in_b,axis=1) == a_in_b.shape[1]
#     return (a_in_b.any() or b_in_a.any()), a_points[a_in_b], b_points[b_in_a], []

    
    
# def collision(a, b):
#     if a.collision is not SOLID or b.collision is not SOLID:
#         return False
#     if isinstance(a.shape, Ball) and isinstance(b.shape, Ball):
#         return ball_ball_collision(a, b)
#     if isinstance(a.shape, Ball) and (isinstance(b.shape, Quad) or isinstance(b.shape, Polygon)):
#         return ball_polygon_collision(a, b)
#     if (isinstance(a.shape, Quad) or isinstance(a.shape, Polygon)) and isinstance(b.shape, Ball):
#         return ball_polygon_collision(b, a)
#     if isinstance(a.shape, Ball) and isinstance(b.shape, Line):
#         return ball_line_collision(a, np.array([b.shape.points[0], b.shape.points[1]]))
#     if isinstance(a.shape, Line) and isinstance(b.shape, Ball):
#         return ball_line_collision(b, np.array([a.shape.points[0], a.shape.points[1]]))
#     return False



# def ball_line_collision(ball, line):
#     org_line = deepcopy(line)
#     p = ball.position.copy()
#     delta = line[0].copy()
#     line -= delta
#     p -= delta
#     s = line[1]/np.linalg.norm(line[1])
#     z = np.dot(p, s)*s
#     d = p - z
#     distance = np.linalg.norm(d)
#     if distance <= ball.shape.radius and np.dot(z, line[1]-z) >= 0:
#         ball.speed -= 2*np.dot(ball.speed, d/distance)*d/distance
#         return True
#     for point in org_line:
#         impact_vector = ball.position - point
#         if np.linalg.norm(impact_vector) <= ball.shape.radius and np.dot(impact_vector, ball.speed) >= 0:
#             norm = (impact_vector)/np.linalg.norm(impact_vector)
#             ball.speed = np.array(ball.speed) - 2*np.dot(norm, ball.speed)*norm
#             return True
#     return False
        





# def line_collide(poly, line, delta):
    
#     if isinstance(poly.shape, Ball):
#         for p in line.shape.get_outside():
#             # print(p, np.linalg.norm(p - poly.shape.center))
#             if np.linalg.norm(p - poly.position) <= poly.shape.radius:
#                 print('point collision')
#                 return True, [], p
       
#     projections_before = get_projections(poly, line)
#     diff_before = projections_before - poly.shape.get_outside()    
#     poly.update_position(delta)
#     line.update_position(delta)
#     projections_after = get_projections(poly, line)
#     diff_after = projections_after - poly.shape.get_outside() 
#     poly.update_position(-delta)
#     line.update_position(-delta)
#     # print(diff_after)
#     sign_change = np.sum(diff_before * diff_after, axis=1) <= 0
#     p0, p1 = line.shape.get_outside()
#     on_line_before = np.sum((projections_before - p0) * (p1 - projections_before), axis=1) >=0
#     on_line_after = np.sum((projections_after - p0) * (p1 - projections_after), axis=1) >=0
#     on_line = np.logical_or(on_line_before, on_line_after)
#     crossed_line = np.logical_and(on_line, sign_change)
#     return crossed_line.any(), poly.shape.get_outside()[crossed_line], []

# def get_projections(poly, line):
#     poly_points = deepcopy(poly.shape.get_outside())
#     line_points = deepcopy(line.shape.get_outside())
#     offset = deepcopy(line_points[0])
#     poly_points -= offset
#     line_points -= offset
#     line_v = line_points[1]/np.linalg.norm(line_points[1])
#     line_projections =  np.array([line_v*x for x in poly_points @ line_v])
#     return line_projections + offset