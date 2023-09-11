import pygame as pg
from pygame.locals import *

class Controls():
    def __init__(self) -> None:
        ...
    
    def press(self, event_type, *args):
        if event_type == pg.QUIT:
            self.quit_()
        if event_type == pg.KEYDOWN:
            if args[0] == K_ESCAPE:
                self.key_down_esc
            if args[0] == K_r:
                self.key_down_r
        if event_type == pg.MOUSEBUTTONDOWN:
            if args[0] == 1:
                self.mouse_down_1()
        if event_type == pg.MOUSEBUTTONUP:
            if args[0] == 1:
                self.mouse_up_1()  
        
    def quit_(self, env):
        pg.quit()
        quit()
        
        
    def key_down_esc(self, env):
        self.quit_()
        
    def key_down_r(self, env):
        ...
        
    def mouse_down_1(self, env):
        ...
        
    def mouse_up_1(self, env):
        ...
        
class GameControls(Controls):
    
    def mouse_down_1(self, env):
        global MOUSEBUTTONDOWN_PRESSED
        level = env['level']
        if not level.is_ball_moving() and MOUSEBUTTONDOWN_PRESSED:
            ball = level.ball
            ball.speed = ball.position - mouse_position()
            ball.speed = 200*np.min([time.time() - MOUSEBUTTONDOWN_TIME, 2])* ball.speed /np.linalg.norm(ball.speed)
            MOUSEBUTTONDOWN_PRESSED = False
            level.played += 1
            top_sound(SOUND_STRECH) 