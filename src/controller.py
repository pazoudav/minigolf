import pygame as pg
from pygame.locals import *
import utils as ut
from draw import set_mode

def quit_():
    pg.quit()
    quit()

def nothing():
    ...


class Controller():
    def __init__(self, env) -> None:
        self.keys = {}
        self.env = env
        self.reset_keys()
        self.set_keys()
    
    def event_loop(self):
        for event in pg.event.get():               
            if event.type == pg.QUIT:
                self.keys[pg.QUIT]()
            elif event.type == pg.KEYDOWN:
                if event.key in self.keys[pg.KEYDOWN]:
                    self.keys[pg.KEYDOWN][event.key]()
            elif event.type == pg.KEYUP:
                if event.key in self.keys[pg.KEYUP]:
                    self.keys[pg.KEYUP][event.key]()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button in self.keys[pg.MOUSEBUTTONUP]:
                    self.keys[pg.MOUSEBUTTONUP][event.button]()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button in self.keys[pg.MOUSEBUTTONDOWN]:
                    self.keys[pg.MOUSEBUTTONDOWN][event.button]()
                    
    def reset_keys(self):
        self.keys[pg.QUIT] = quit_
        self.keys[pg.KEYDOWN] = {}
        self.keys[pg.KEYDOWN][K_ESCAPE] = nothing
        self.keys[pg.KEYDOWN][K_r] = nothing
        self.keys[pg.KEYDOWN][K_LEFT] = nothing
        self.keys[pg.KEYDOWN][K_RIGHT] = nothing
        self.keys[pg.KEYDOWN][K_UP] = nothing
        self.keys[pg.KEYDOWN][K_DOWN] = nothing
        self.keys[pg.KEYDOWN][K_MINUS] = nothing
        self.keys[pg.KEYDOWN][K_EQUALS] = nothing # plus
        self.keys[pg.KEYUP] = {}
        self.keys[pg.KEYUP][K_LEFT] =       nothing 
        self.keys[pg.KEYUP][K_RIGHT] =      nothing 
        self.keys[pg.KEYUP][K_UP] =         nothing 
        self.keys[pg.KEYUP][K_DOWN] =       nothing 
        self.keys[pg.MOUSEBUTTONUP] = {}
        self.keys[pg.MOUSEBUTTONUP][1] = nothing
        self.keys[pg.MOUSEBUTTONDOWN] = {}
        self.keys[pg.MOUSEBUTTONDOWN][1] = nothing 
        
    def set_keys(self):
        self.reset_keys()
        
    def pre_loop(self):
        ...
        
    def launch(self):
        ut.reset_camera()
        set_mode()
        self.env['context'] = self
        
    # def mouse_up_1(self, env):
    #     ...
        
    # def mouse_down_1(self, env):
    #     ...