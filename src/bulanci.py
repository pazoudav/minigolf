from controller import *
import utils as ut
from draw import draw_level, set_mode, draw_aim_bar, draw_power_bar
import numpy as np
from collision import new_collision, check_collision
from level import Level
from bodies import *
from shape import Quad, Point
from material import Texture

delta = 10
RIGHT = np.array([1,0])
LEFT = np.array([-1,0])
UP = np.array([0,1])
DOWN = np.array([0,-1])

class Bulanek(DynamicBody):
    def __init__(self, pos):
        super().__init__(Ball(pos, [50, 4]), Texture('one-one.png'))
        self.weapon = 'pistol'
        self.amo = 100
        self.view = RIGHT
        self.moving = False
        
    def update_position(self, delta_t):
        new_pos = self.shape.pos + 200*self.view*delta_t
        self.shape.set_position(new_pos)
        self.position = new_pos
        
class Bullet(KineticBody):
    def __init__(self, pos, dir_v):
        super().__init__(Ball(pos, [5,10]), lambda t: [500*dir_v[0], 500*dir_v[1],0], Texture(ut.TEXTURE_HOLE))

class BulanekController(Controller):
    def __init__(self, env) -> None:
        super(BulanekController, self).__init__(env)
        self.bulanek = Bulanek([100,100])
        self.level = Level('bulanek')
        self.level.load()
        self.level.ball = self.bulanek
        
    def change_direction(self, dir_v):
        self.bulanek.view = dir_v
        self.bulanek.moving = True
            
    def stop(self, dir_v):
        if self.bulanek.moving and (self.bulanek.view == dir_v).all():
            self.bulanek.moving = False
            
    def key_down_left(self):
        self.change_direction(LEFT)
    def key_down_right(self):
        self.change_direction(RIGHT)
    def key_down_up(self):
        self.change_direction(UP)
    def key_down_down(self):
        self.change_direction(DOWN)
    def key_up_left(self):
        self.stop(LEFT)
    def key_up_right(self):
        self.stop(RIGHT)
    def key_up_up(self):
        self.stop(UP)
    def key_up_down(self):
        self.stop(DOWN)
        
    def key_down_space(self):
        self.level.add_kinetic_body(Bullet(self.bulanek.position + 60*self.bulanek.view, self.bulanek.view))
        
        
    def set_keys(self):
        self.keys[pg.KEYDOWN][K_ESCAPE] =   lambda: self.env['choose_level_menu'].launch()
        self.keys[pg.KEYDOWN][K_r] =        lambda: self.level.reset()
        self.keys[pg.KEYDOWN][K_LEFT] =     self.key_down_left
        self.keys[pg.KEYDOWN][K_RIGHT] =    self.key_down_right
        self.keys[pg.KEYDOWN][K_UP] =       self.key_down_up
        self.keys[pg.KEYDOWN][K_DOWN] =     self.key_down_down
        self.keys[pg.KEYDOWN][K_SPACE] =    self.key_down_space
        self.keys[pg.KEYUP][K_LEFT] =       self.key_up_left
        self.keys[pg.KEYUP][K_RIGHT] =      self.key_up_right
        self.keys[pg.KEYUP][K_UP] =         self.key_up_up
        self.keys[pg.KEYUP][K_DOWN] =       self.key_up_down
        

        
    def pre_loop(self):
        self.update()
        draw_level(self.level)

        
    def launch(self):
        super().launch()
        ut.clock = pg.time.Clock() 
      
    def launch_wrapper(self, level_name):
        # self.env['level_name'] = level_name
        return self.launch
        
        
    def update(self):
        time = ut.clock.tick()/1000
        for body in self.level.all_bodies:
            body.updated = False
        
        for kinetic_body in self.level.kinetics:
            kinetic_body.update_position(time)
            
            for static_body in self.level.statics:
                if check_collision(kinetic_body, static_body, 0)[0]:
                    self.level.remove(kinetic_body)
                    ut.play_sound(ut.SOUND_HIT)
            if check_collision(kinetic_body, self.bulanek, 0)[0]:
                    self.level.remove(kinetic_body)
                    ut.play_sound(ut.SOUND_HIT)
                    print('hit!!!!!!!!')
                    
        if self.bulanek.moving:
            self.bulanek.update_position(time)
            for static_body in self.level.statics:
                if check_collision(self.bulanek, static_body, 0)[0]:
                    self.bulanek.update_position(-time)
        
            