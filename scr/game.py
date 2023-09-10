from collision import new_collision, check_collision
from utils import *
from action import *

# global actions

# def action_handler():
#     global actions
#     for a in actions:
#         if isinstance(a, Collision):
#             play_sound(SOUND_HIT)
#     actions = []

def update(level, clock):
    # global actions
    time = clock.tick()/1000
    for body in level.all_bodies:
        body.updated = False
    
    for body in level.statics:
        collision_happened = new_collision(level.ball, body, time)
        if collision_happened:
            level.ball.updated = True
            play_sound(SOUND_HIT)
            # actions.append(Collision(level.ball.shape.pos))
            break
        
    for body in level.kinetics:
        collision_happened = new_collision(level.ball, body, time)
        if collision_happened:
            level.ball.updated = True
            body.updated = True
            play_sound(SOUND_HIT)
            # actions.append(Collision(level.ball.shape.pos))
            break
        else:
            body.update_position(time)
      
    if not level.ball.updated:
        level.ball.update_position(time)
    level.ball.apply_friction(time)
            
    for star in level.stars:
        if check_collision(level.ball, star, 0)[0]:
            star.collect()