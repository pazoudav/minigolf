import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
import numpy as np
from shape import *
from bodies import *
import time
from level import *
from draw import draw_level, draw_power_bar, draw_menu
from action import *
from utils import *
from collision import new_collision, check_collision
from menu import *
from button import *
from level_editor import LevelEditor


clock = pg.time.Clock() 
actions = []


def init_game():
    pg.display.init()
    pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    glClearColor(0.3, 0.5, 0.2, 1.0)
    glLineWidth(LINE_WIDTH)
    glPointSize(POINT_SIZE)
    play_sound(SOUND_BACKGROUND)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    

def set_mode():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glViewport(0, 0, WIDTH, HEIGHT)
    
    glClear(GL_COLOR_BUFFER_BIT)
                        

    
def update(level):
    global actions
    time = clock.tick()/1000
    for body in level.all_bodies:
        body.updated = False
    
    for body in level.statics:
        collision_happened = new_collision(level.ball, body, time)
        if collision_happened:
            level.ball.updated = True
            actions.append(Collision(level.ball.shape.pos))
            break
        
    for body in level.kinetics:
        collision_happened = new_collision(level.ball, body, time)
        if collision_happened:
            level.ball.updated = True
            body.updated = True
            actions.append(Collision(level.ball.shape.pos))
            break
        else:
            body.update_position(time)
      
    if not level.ball.updated:
        level.ball.update_position(time)
    level.ball.apply_friction(time)
            
    for star in level.stars:
        if check_collision(level.ball, star, 0)[0]:
            star.collect()
            
    


def action_handler():
    global actions
    for action in actions:
        if isinstance(action, Collision):
            play_sound(SOUND_HIT)
    actions = []


def display(level):
    set_mode()
    draw_level(level)
    if MOUSEBUTTONDOWN_PRESSED:
        draw_power_bar(MOUSEBUTTONDOWN_TIME, level.ball.shape.pos)
        
    pg.display.flip()


def game_loop(level):     
    global LAST_UPDATE, MOUSEBUTTONDOWN_TIME, MOUSEBUTTONDOWN_PRESSED
    
    update(level)
    action_handler()
    
    display(level)
    
    if level.is_won():
        play_sound(SOUND_WIN)
        level.reset()
        return False
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            elif event.key == K_r:
                level.reset()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and not level.is_ball_moving() and MOUSEBUTTONDOWN_PRESSED:
                ball = level.ball
                ball.speed = ball.shape.pos - mouse_position()
                ball.speed = 200*np.min([time.time() - MOUSEBUTTONDOWN_TIME, 2])* ball.speed /np.linalg.norm(ball.speed)
                MOUSEBUTTONDOWN_PRESSED = False
                level.played += 1
                stop_sound(SOUND_STRECH)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not level.is_ball_moving():
                MOUSEBUTTONDOWN_PRESSED = True
                MOUSEBUTTONDOWN_TIME = time.time()
                play_sound(SOUND_STRECH)                    
      
    
    return True
    
def choose_level():
    level_menu = Menu()
    level_menu.add_button('level1',   Button([370, 300], SIZE_BUTTON, SIZE_BUTTON, 'temp_name', Texture(TEXTURE_GOLFBALL)))
    level_menu.add_button('level2',   Button([430, 300], SIZE_BUTTON, SIZE_BUTTON, 'config2', Texture(TEXTURE_GOLFBALL)))
    
    choosing = True
    while choosing:
        
        set_mode()
        draw_menu(level_menu)
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    choosing = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    success, result = level_menu.click(mouse_position()) 
                    if success:
                        launch_level(result) 
        
                         
         
    
def level_editor_launcher():
    editor = LevelEditor()
    editor.run()

def start_loop(start_menu):
    
    draw_menu(start_menu) 
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 :
                success, result = start_menu.click(mouse_position()) 
                if success:
                     result() 
    


def launch_level(name):
    global clock 
    clock = pg.time.Clock() 
    level = Level(name)
    level.load()
    play = True
    while play:
        play = game_loop(level)


if __name__ == "__main__":
    
    init_game()
    
    start_menu = Menu()
    start_menu.add_button('choose_level',   Button([370, 300], SIZE_BUTTON, SIZE_BUTTON, choose_level, Texture(TEXTURE_GOLFBALL)))
    start_menu.add_button('level_editor',   Button([430, 300], SIZE_BUTTON, SIZE_BUTTON, level_editor_launcher, Texture(TEXTURE_BARRIER)))
    
    while True:
        set_mode()
        start_loop(start_menu)
        pg.display.flip()
    
    