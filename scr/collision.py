import numpy as np
from shape import *
from bodies import *
from copy import deepcopy

def check_collision(a, b, delta):
    if len(b.shape.points) > len(a.shape.points):
        a, b = b, a
    if isinstance(b.shape, Line):
        return ball_line_collision_2(a, b, delta)
    else:
        return collide_SAT(a, b, delta)
    
def ball_line_collision_2(ball, l, time):
    ball.update_position(time)
    line = l.shape.get_outside()
    org_line = deepcopy(line)
    for point in org_line:
        impact_vector = point - ball.position 
        if np.linalg.norm(impact_vector) <= ball.shape.radius:
            ball.update_position(-time)
            return True, [], [point]
        
    p = ball.position.copy()
    delta = line[0].copy()
    line -= delta
    p -= delta
    s = line[1]/np.linalg.norm(line[1])
    z = np.dot(p, s)*s
    d = p - z
    distance = np.linalg.norm(d)
    if distance <= ball.shape.radius and np.dot(z, line[1]-z) >= 0:
        ball.update_position(-time)
        return True, [z+delta], []
    
    ball.update_position(-time)
    return False, [], []

def get_projections(poly, line):
    poly_points = deepcopy(poly.shape.get_outside())
    line_points = deepcopy(line.shape.get_outside())
    offset = deepcopy(line_points[0])
    poly_points -= offset
    line_points -= offset
    line_v = line_points[1]/np.linalg.norm(line_points[1])
    line_projections =  np.array([line_v*x for x in poly_points @ line_v])
    return line_projections + offset


def collide_SAT(a, b, delta):
    a.update_position(delta)
    b.update_position(delta)
    a_points = deepcopy(a.shape.get_outside())
    b_points = deepcopy(b.shape.get_outside())
    a_lines = np.array([ a_points[i] - a_points[i-1] for i in range(len(a_points)) ])
    a_lines = a_lines.T/np.linalg.norm(a_lines, axis=1)
    normals = np.array([-a_lines[1], a_lines[0]])
    projection_a =  a_points @ normals
    projection_b =  b_points @ normals
    min_a = np.min(projection_a,axis=0)
    max_a = np.max(projection_a,axis=0)
    min_b = np.min(projection_b,axis=0)
    max_b = np.max(projection_b,axis=0)
    b_in_a = np.logical_and(min_a <= projection_b, projection_b <= max_a)
    b_in_a = np.sum(b_in_a,axis=1) == b_in_a.shape[1]
    a_in_b = np.logical_and(min_b <= projection_a, projection_a <= max_b)
    a_in_b = np.sum(a_in_b,axis=1) == a_in_b.shape[1]
    a.update_position(-delta)
    b.update_position(-delta)
    return (a_in_b.any() or b_in_a.any()), a_points[a_in_b], b_points[b_in_a]


MAX_COLLISION_ITER = 8

def new_collision(a, b, delta_):
    if a.collision != SOLID or b.collision != SOLID:
        return False
      
    best_time = 0
    delta = delta_  
    t, best_a, best_b = check_collision(a, b, delta)
    time = delta/2
    if not t:
        return False
    
    # print('collision', a, b)
    last_t = t
    count = 0
    while count <= MAX_COLLISION_ITER: 
        t, a_points, b_points = check_collision(a, b, time)
        delta /= 2
        if t: 
            # best_time = time
            time -= delta 
            best_a, best_b = a_points, b_points
        else:
            best_time = time
            time += delta 
        # print(best_a, best_b)
        count += 1
    
    a_mean = np.mean(best_a, axis=0)
    b_mean = np.mean(best_b, axis=0)
    if np.isnan(a_mean).any():
        contact_point = b_mean
    elif np.isnan(b_mean).any():
        contact_point = a_mean
    else:
        contact_point = np.mean(np.vstack([a_mean, b_mean]),axis=0)
    a.update_position(best_time)
    b.update_position(best_time)
    # print(check_collision(a,b,0))

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
        a.speed[0] = b.speed[0] if (b.speed[0] <= 0 and a.speed[0] <= 0 and b.speed[0] <= a.speed[0]) or (b.speed[0] >= 0 and a.speed[0] >= 0 and b.speed[0] >= a.speed[0]) else a.speed[0]
        a.speed[1] = b.speed[1] if (b.speed[1] <= 0 and a.speed[1] <= 0 and b.speed[1] <= a.speed[1]) or (b.speed[1] >= 0 and a.speed[1] >= 0 and b.speed[1] >= a.speed[1]) else a.speed[1]
    elif isinstance(a, DynamicBody) and isinstance(b, StaticBody):
        if np.dot(a_vector, a.speed) >= 0:
            a.speed -= 2*a_vector*np.dot(a_vector, a.speed)
    
    a.update_position(delta_ - best_time)
    b.update_position(delta_ - best_time)      
    return True
            
    
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


# def ball_polygon_collision(ball, rect):
#     if not isinstance(ball, DynamicBody) and isinstance(rect, DynamicBody):
#         return False
#     diff = ball.position - rect.position
#     diff_size = np.linalg.norm(diff)
#     # if diff_size > ball.shape.radius + np.linalg.norm([rect.shape.side_a/2, rect.shape.side_b/2]):
#         # return False
#     points = rect.shape.get_outside()
#     for i in range(len(points)):
#         if ball_line_collision(ball, [points[i-1],points[i]]):
#             if np.linalg.norm(rect.speed) != 0:
#                 ball.speed[0] = rect.speed[0] if (rect.speed[0] <= 0 and ball.speed[0] <= 0 and rect.speed[0] <= ball.speed[0]) or (rect.speed[0] >= 0 and ball.speed[0] >= 0 and rect.speed[0] >= ball.speed[0]) else ball.speed[0]
#                 ball.speed[1] = rect.speed[1] if (rect.speed[1] <= 0 and ball.speed[1] <= 0 and rect.speed[1] <= ball.speed[1]) or (rect.speed[1] >= 0 and ball.speed[1] >= 0 and rect.speed[1] >= ball.speed[1]) else ball.speed[1]
    
#                 # ball.speed += rect.speed*2
                
#             return True
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
        

# def ball_ball_collision(a, b):
#     diff = a.position - b.position
#     diff_size = np.linalg.norm(diff)
#     if diff_size <= a.shape.radius + b.shape.radius:
#         diff /= diff_size 
#         if isinstance(a, DynamicBody) and isinstance(b, DynamicBody):
#             a.speed += diff*np.dot(diff, b.speed) - diff*np.dot(diff, a.speed)
#             b.speed += diff*np.dot(diff, a.speed) - diff*np.dot(diff, b.speed)
#         elif isinstance(a, DynamicBody) and (isinstance(b, StaticBody) or isinstance(b, KineticBody)):
#             a.speed -= 2*diff*np.dot(diff, a.speed)
#         elif isinstance(b, DynamicBody) and (isinstance(a, StaticBody) or isinstance(a, KineticBody)):
#             b.speed -= 2*diff*np.dot(diff, b.speed)
#         return True
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