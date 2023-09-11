import utils as ut
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from level_editor import LevelEditor
from menu import Menu
from button import *
from material import *
from menuController import*
from gameController import GameController

def init_game():
    pg.display.init()
    pg.display.set_mode((ut.WIDTH, ut.HEIGHT), DOUBLEBUF|OPENGL)
    glClearColor(0.15, 0.46, 0.23, 0)
    glLineWidth(ut.LINE_WIDTH)
    glPointSize(ut.POINT_SIZE)
    ut.play_sound(ut.SOUND_BACKGROUND)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                
                      
def launch_level_editor(env):
    ut.reset_camera()
    editor = LevelEditor()
    editor.run()
    ut.reset_camera()
    env['start_menu'].launch()   
          
                      
if __name__ == '__main__':
    init_game()
    env = {}
      
    env['end_level_menu'] = EndMenuController(env)
    
    env['game'] = GameController(env)
    
    choose_level_menu = Menu()
    choose_level_menu.add_button('level1',          Button([300, 500], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch_wrapper('level_2')(),     Texture(ut.TEXTURE_LEVEL_1)))
    choose_level_menu.add_button('level2',          Button([500, 500], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch_wrapper('level_3')(),     Texture(ut.TEXTURE_LEVEL_2)))
    choose_level_menu.add_button('level3',          Button([300, 300], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch_wrapper('level_4')(),     Texture(ut.TEXTURE_LEVEL_3)))
    choose_level_menu.add_button('level4',          Button([500, 300], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch_wrapper('level_1')(),     Texture(ut.TEXTURE_LEVEL_4)))
    choose_level_menu.add_button('custom_level',    Button([400, 100], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch_wrapper('level_custom')(),Texture(ut.TEXTURE_LEVEL_CUSTOM)))   
    env['choose_level_menu'] = MenuController(env, choose_level_menu)
    env['choose_level_menu'].keys[pg.KEYDOWN][K_ESCAPE] = lambda: env['start_menu'].launch()
    
    start_menu = Menu()
    start_menu.add_button('choose_level',   Button([300, 300], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['choose_level_menu'].launch(),  Texture(ut.TEXTURE_CHOOSE_LEVEL)))
    start_menu.add_button('level_editor',   Button([500, 300], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: launch_level_editor(env),       Texture(ut.TEXTURE_LEVEL_EDITOR)))
    env['start_menu'] = MenuController(env, start_menu)
    env['start_menu'].launch()
    
    while True:
        env['context'].pre_loop()
        env['context'].event_loop()
        # post_loop(env)
        pg.display.flip()
