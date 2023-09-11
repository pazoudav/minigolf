from controller import *
import utils as ut
from draw import draw_level, set_mode, draw_aim_bar, draw_power_bar
import numpy as np
from collision import new_collision, check_collision
from level import Level

delta = 10

class GameController(Controller):
    def __init__(self, env) -> None:
        super(GameController, self).__init__(env)
        
    def key_down_left(self):
        ut.OFFSET_HORIZONTAL -= delta
    def key_down_right(self):
        ut.OFFSET_HORIZONTAL += delta
    def key_down_up(self):
        ut.OFFSET_VERTICAL += delta
    def key_down_down(self):
        ut.OFFSET_VERTICAL -= delta
    def key_down_plus(self):
        ut.FACTOR_SCALE *= 0.9
    def key_down_minus(self):
        ut.FACTOR_SCALE /= 0.9
        
    def set_keys(self):
        self.keys[pg.KEYDOWN][K_ESCAPE] =   self.env['choose_level_menu'].launch
        self.keys[pg.KEYDOWN][K_r] =        self.level.reset
        self.keys[pg.KEYDOWN][K_LEFT] =     self.key_down_left
        self.keys[pg.KEYDOWN][K_RIGHT] =    self.key_down_right
        self.keys[pg.KEYDOWN][K_UP] =       self.key_down_up
        self.keys[pg.KEYDOWN][K_DOWN] =     self.key_down_down
        self.keys[pg.KEYDOWN][K_EQUALS] =   self.key_down_plus
        self.keys[pg.KEYDOWN][K_MINUS] =    self.key_down_minus
        self.keys[pg.MOUSEBUTTONUP][1] =    self.mouse_up_1
        self.keys[pg.MOUSEBUTTONDOWN][1]  = self.mouse_down_1
        
    def mouse_up_1(self):
        if not self.level.is_ball_moving() and ut.MOUSEBUTTONDOWN_PRESSED:
            ball = self.level.ball
            ball.speed = ball.position - ut.mouse_position()
            ball.speed = 200*np.min([ut.time.time() - ut.MOUSEBUTTONDOWN_TIME, 2])* ball.speed /np.linalg.norm(ball.speed)
            ut.MOUSEBUTTONDOWN_PRESSED = False
            self.level.played += 1
            ut.stop_sound(ut.SOUND_STRECH)    
    
    def mouse_down_1(self):
        if not self.level.is_ball_moving():
            ut.MOUSEBUTTONDOWN_PRESSED = True
            ut.MOUSEBUTTONDOWN_TIME = ut.time.time()
            ut.play_sound(ut.SOUND_STRECH)
            
    def pre_loop(self):
        self.update()
        set_mode()
        draw_level(self.level)
        if not self.level.is_ball_moving():
            draw_aim_bar(self.level.ball.position, ut.mouse_position())
        if ut.MOUSEBUTTONDOWN_PRESSED:
            draw_power_bar(ut.MOUSEBUTTONDOWN_TIME, self.level.ball.position, ut.mouse_position())
        if self.level.is_won():
            
            for i in range(1000):
                d = self.level.hole.position - self.level.ball.position
                d = d/np.linalg.norm(d)
                n = 100*np.array([-d[1], d[0]])
                self.level.ball.speed = n
                self.update()
                set_mode()
                draw_level(self.level)
                pg.display.flip()
            ut.play_sound(ut.SOUND_WIN)
            self.env['end_level_menu'].launch_wrapper(self.level.stars_collected())
            
            # launch_end_level_menu(env)
        
    def launch(self):
        super().launch()
        ut.clock = pg.time.Clock() 
        self.level = Level(self.env['level_name'])
        self.level.load()
        self.env['level'] = self.level
        self.set_keys()
      
    def launch_wrapper(self, level_name):
        self.env['level_name'] = level_name
        return self.launch
        
        
    def update(self):
        time = ut.clock.tick()/1000
        for body in self.level.all_bodies:
            body.updated = False
        
        for body in self.level.statics:
            collision_happened = new_collision(self.level.ball, body, time)
            if collision_happened:
                self.level.ball.updated = True
                ut.play_sound(ut.SOUND_HIT)
                # actions.append(Collision(level.ball.position))
                break
            
        for body in self.level.kinetics:
            collision_happened = new_collision(self.level.ball, body, time)
            if collision_happened:
                self.level.ball.updated = True
                body.updated = True
                ut.play_sound(ut.SOUND_HIT)
                # actions.append(Collision(level.ball.position))
                # break
            else:
                body.update_position(time)
        
        if not self.level.ball.updated:
            self.level.ball.update_position(time)
            self.level.ball.apply_friction(time)
                
        for star in self.level.stars:
            if check_collision(self.level.ball, star, 0)[0]:
                star.collect()
            
        
# def launch_game_loop(env):
#     reset_keys(env)
#     ut.reset_camera()
#     ut.clock = pg.time.Clock() 
#     level = Level(env['level_name'])
#     level.load()
#     env['level'] = level
#     set_game_loop(env)
                
# def set_game_loop(env):
#     global pre_loop, keys
#     def pre_loop_(env):
#         level = env['level']
#         update(level, ut.clock)
#         set_mode()
#         draw_level(level)
#         if not level.is_ball_moving():
#             draw_aim_bar(level.ball.position, ut.mouse_position())
#         if ut.MOUSEBUTTONDOWN_PRESSED:
#             draw_power_bar(ut.MOUSEBUTTONDOWN_TIME, level.ball.position, ut.mouse_position())
#         if level.is_won():
            
#             for i in range(1000):
#                 d = level.hole.position - level.ball.position
#                 d = d/np.linalg.norm(d)
#                 n = 100*np.array([-d[1], d[0]])
#                 level.ball.speed = n
#                 update(level, ut.clock)
#                 set_mode()
#                 draw_level(level)
#                 pg.display.flip()
#             ut.play_sound(ut.SOUND_WIN)
#             launch_end_level_menu(env)
            
#     delta = 10
#     def key_down_left(env):
         
#         ut.OFFSET_HORIZONTAL -= delta
#     def key_down_right(env):
         
#         ut.OFFSET_HORIZONTAL += delta
#     def key_down_up(env):
         
#         ut.OFFSET_VERTICAL += delta
#     def key_down_down(env):
         
#         ut.OFFSET_VERTICAL -= delta
#     def key_down_plus(env):
         
#          ut.FACTOR_SCALE *= 0.9
#     def key_down_minus(env):
         
#          ut.FACTOR_SCALE /= 0.9
                
#     def mouse_1_up(env):
         
#         level = env['level']
#         if not level.is_ball_moving() and ut.MOUSEBUTTONDOWN_PRESSED:
#             ball = level.ball
#             ball.speed = ball.position - ut.mouse_position()
#             ball.speed = 200*np.min([ut.time.time() - ut.MOUSEBUTTONDOWN_TIME, 2])* ball.speed /np.linalg.norm(ball.speed)
#             ut.MOUSEBUTTONDOWN_PRESSED = False
#             level.played += 1
#             ut.stop_sound(ut.SOUND_STRECH)    
    
#     def mouse_1_down(env):
         
#         if not env['level'].is_ball_moving():
#             ut.MOUSEBUTTONDOWN_PRESSED = True
#             ut.MOUSEBUTTONDOWN_TIME = ut.time.time()
#             ut.play_sound(ut.SOUND_STRECH)   
            
    
#     pre_loop = pre_loop_
#     keys[pg.KEYDOWN][K_r] = lambda env : env['level'].reset()
#     keys[pg.KEYDOWN][K_ESCAPE] = launch_choose_level_menu
#     keys[pg.KEYDOWN][K_LEFT] = key_down_left
#     keys[pg.KEYDOWN][K_RIGHT] = key_down_right
#     keys[pg.KEYDOWN][K_UP] = key_down_up
#     keys[pg.KEYDOWN][K_DOWN] = key_down_down
#     keys[pg.KEYDOWN][K_EQUALS] = key_down_plus
#     keys[pg.KEYDOWN][K_MINUS] = key_down_minus
#     keys[pg.MOUSEBUTTONUP][1] = mouse_1_up
#     keys[pg.MOUSEBUTTONDOWN][1] =  mouse_1_down
    
    