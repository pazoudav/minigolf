from utils import *
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from draw import draw_level, draw_power_bar, draw_menu, draw_aim_bar
from level import Level
from level_editor import LevelEditor
from menu import Menu
from button import *
from material import *
from game import update

def quit_(env):
    pg.quit()
    quit()

def nothing(env):
    ...

keys = {}
clock = pg.time.Clock()

def reset_keys(env):
    global keys
    keys[pg.QUIT] = quit_
    keys[pg.KEYDOWN] = {}
    keys[pg.KEYDOWN][K_ESCAPE] = nothing
    keys[pg.KEYDOWN][K_r] = nothing
    keys[pg.KEYDOWN][K_LEFT] = nothing
    keys[pg.KEYDOWN][K_RIGHT] = nothing
    keys[pg.KEYDOWN][K_UP] = nothing
    keys[pg.KEYDOWN][K_DOWN] = nothing
    keys[pg.KEYDOWN][K_MINUS] = nothing # minus
    keys[pg.KEYDOWN][K_EQUALS] = nothing # plus
    keys[pg.KEYUP] = {}
    keys[pg.MOUSEBUTTONUP] = {}
    keys[pg.MOUSEBUTTONUP][1] = nothing
    keys[pg.MOUSEBUTTONDOWN] = {}
    keys[pg.MOUSEBUTTONDOWN][1] = nothing

def reset_camera():
    global OFFSET_HORIZONTAL, OFFSET_VERTICAL, FACTOR_SCALE
    OFFSET_HORIZONTAL = 0
    OFFSET_VERTICAL = 0
    FACTOR_SCALE = 1

def mouse_position():
    return np.array([pg.mouse.get_pos()[0]*FACTOR_SCALE + OFFSET_HORIZONTAL, (HEIGHT-pg.mouse.get_pos()[1])*FACTOR_SCALE + OFFSET_VERTICAL])


def init_game():
    pg.display.init()
    pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    glClearColor(0.15, 0.46, 0.23, 0)
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
    
    gluOrtho2D(FACTOR_SCALE*OFFSET_HORIZONTAL, 
               FACTOR_SCALE*(WIDTH+OFFSET_HORIZONTAL), 
               FACTOR_SCALE*OFFSET_VERTICAL, 
               FACTOR_SCALE*(HEIGHT+ OFFSET_VERTICAL))
    glViewport(0, 0, WIDTH, HEIGHT)
    
    glClear(GL_COLOR_BUFFER_BIT)

def main_loop(env):
    
    for event in pg.event.get():               
        if event.type == pg.QUIT:
            keys[pg.QUIT](env)
        elif event.type == pg.KEYDOWN:
            if event.key in keys[pg.KEYDOWN]:
                keys[pg.KEYDOWN][event.key](env)
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button in keys[pg.MOUSEBUTTONUP]:
                keys[pg.MOUSEBUTTONUP][event.button](env)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button in keys[pg.MOUSEBUTTONDOWN]:
                keys[pg.MOUSEBUTTONDOWN][event.button](env) 
                
def launch_game_loop(env):
    global clock
    reset_keys(env)
    reset_camera()
    clock = pg.time.Clock() 
    level = Level(env['level_name'])
    level.load()
    env['level'] = level
    set_game_loop(env)
                
def set_game_loop(env):
    global keys, pre_loop, clock
    def pre_loop_(env):
        level = env['level']
        update(level, clock)
        set_mode()
        draw_level(level)
        if not level.is_ball_moving():
            draw_aim_bar(level.ball.position, mouse_position())
        if MOUSEBUTTONDOWN_PRESSED:
            draw_power_bar(MOUSEBUTTONDOWN_TIME, level.ball.position, mouse_position())
        if level.is_won():
            
            for i in range(1000):
                d = level.hole.position - level.ball.position
                d = d/np.linalg.norm(d)
                n = 100*np.array([-d[1], d[0]])
                level.ball.speed = n
                update(level, clock)
                set_mode()
                draw_level(level)
                pg.display.flip()
            play_sound(SOUND_WIN)
            launch_end_level_menu(env)
            
    delta = 10
    def key_down_left(env):
        global OFFSET_HORIZONTAL
        OFFSET_HORIZONTAL -= delta
    def key_down_right(env):
        global OFFSET_HORIZONTAL
        OFFSET_HORIZONTAL += delta
    def key_down_up(env):
        global OFFSET_VERTICAL
        OFFSET_VERTICAL += delta
    def key_down_down(env):
        global OFFSET_VERTICAL
        OFFSET_VERTICAL -= delta
    def key_down_plus(env):
        global FACTOR_SCALE
        FACTOR_SCALE *= 0.9
    def key_down_minus(env):
        global FACTOR_SCALE
        FACTOR_SCALE /= 0.9
                
    def mouse_1_up(env):
        global MOUSEBUTTONDOWN_PRESSED
        level = env['level']
        if not level.is_ball_moving() and MOUSEBUTTONDOWN_PRESSED:
            ball = level.ball
            ball.speed = ball.position - mouse_position()
            ball.speed = 200*np.min([time.time() - MOUSEBUTTONDOWN_TIME, 2])* ball.speed /np.linalg.norm(ball.speed)
            MOUSEBUTTONDOWN_PRESSED = False
            level.played += 1
            stop_sound(SOUND_STRECH)    
    
    def mouse_1_down(env):
        global MOUSEBUTTONDOWN_PRESSED, MOUSEBUTTONDOWN_TIME
        if not env['level'].is_ball_moving():
            MOUSEBUTTONDOWN_PRESSED = True
            MOUSEBUTTONDOWN_TIME = time.time()
            play_sound(SOUND_STRECH)   
            
    
    pre_loop = pre_loop_
    keys[pg.KEYDOWN][K_r] = lambda env : env['level'].reset()
    keys[pg.KEYDOWN][K_ESCAPE] = launch_choose_level_menu
    keys[pg.KEYDOWN][K_LEFT] = key_down_left
    keys[pg.KEYDOWN][K_RIGHT] = key_down_right
    keys[pg.KEYDOWN][K_UP] = key_down_up
    keys[pg.KEYDOWN][K_DOWN] = key_down_down
    keys[pg.KEYDOWN][K_EQUALS] = key_down_plus
    keys[pg.KEYDOWN][K_MINUS] = key_down_minus
    keys[pg.MOUSEBUTTONUP][1] = mouse_1_up
    keys[pg.MOUSEBUTTONDOWN][1] =  mouse_1_down
    
    
def launch_end_level_menu(env):
    reset_keys(env)  
    reset_camera()
    level = env['level']
    n_star = level.stars_collected()
    # print(OFFSET_HORIZONTAL, OFFSET_VERTICAL, FACTOR_SCALE)
    end_level_menu = Menu()
    end_level_menu.add_button('star1',   Button([200, 400], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, nothing, Texture(TEXTURE_STAR if n_star > 0 else TEXTURE_SAD_STAR)))
    end_level_menu.add_button('star2',   Button([400, 400], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, nothing, Texture(TEXTURE_STAR if n_star > 1 else TEXTURE_SAD_STAR)))
    end_level_menu.add_button('star3',   Button([600, 400], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, nothing, Texture(TEXTURE_STAR if n_star > 2 else TEXTURE_SAD_STAR)))
    end_level_menu.add_button('redo',    Button([500, 200], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, launch_game_loop, Texture(TEXTURE_REDO)))
    end_level_menu.add_button('home',    Button([300, 200], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, launch_choose_level_menu, Texture(TEXTURE_HOME)))   
    env['end_level_menu'] = end_level_menu
    set_end_level_menu(env)
    
def set_end_level_menu(env):
    global pre_loop, keys 
    
    def pre_loop_(env):
        # set_mode()
        draw_menu(env['end_level_menu']) 
    
    def mouse_1_down(env):
        success, result = env['end_level_menu'].click(mouse_position()) 
        if success:
            result(env)
     
    pre_loop = pre_loop_
    keys[pg.KEYDOWN][K_ESCAPE] = launch_choose_level_menu
    keys[pg.MOUSEBUTTONDOWN][1] =  mouse_1_down

def launch_start_menu(env):    
    reset_keys(env) 
    reset_camera()
    start_menu = Menu()
    start_menu.add_button('choose_level',   Button([300, 300], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, launch_choose_level_menu, Texture(TEXTURE_CHOOSE_LEVEL)))
    start_menu.add_button('level_editor',   Button([500, 300], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, launch_level_editor, Texture(TEXTURE_LEVEL_EDITOR)))
    env['start_menu'] = start_menu
    set_start_menu(env)
    
def set_start_menu(env):
    global pre_loop, keys 
    
    def pre_loop_(env):
        set_mode()
        draw_menu(env['start_menu']) 
    
    def mouse_1_down(env):
        success, result = env['start_menu'].click(mouse_position()) 
        if success:
            result(env)
      
    pre_loop = pre_loop_
    keys[pg.KEYDOWN][K_ESCAPE] = quit_
    keys[pg.MOUSEBUTTONDOWN][1] =  mouse_1_down


    
def launch_choose_level_menu(env):
    reset_keys(env)  
    reset_camera()
    # print(OFFSET_HORIZONTAL, OFFSET_VERTICAL, FACTOR_SCALE)
    choose_level_menu = Menu()
    choose_level_menu.add_button('level1',   Button([300, 500], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, 'level_2', Texture(TEXTURE_LEVEL_1)))
    choose_level_menu.add_button('level2',   Button([500, 500], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, 'level_3', Texture(TEXTURE_LEVEL_2)))
    choose_level_menu.add_button('level3',   Button([300, 300], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, 'level_4', Texture(TEXTURE_LEVEL_3)))
    choose_level_menu.add_button('level4',   Button([500, 300], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, 'level_1', Texture(TEXTURE_LEVEL_4)))
    choose_level_menu.add_button('custom_level',   Button([400, 100], SIZE_MENU_BUTTON, SIZE_MENU_BUTTON, 'level_custom', Texture(TEXTURE_LEVEL_CUSTOM)))   
    env['choose_level_menu'] = choose_level_menu
    set_choose_level_menu(env)
    
def set_choose_level_menu(env):
    global pre_loop, keys 
    
    def pre_loop_(env):
        set_mode()
        draw_menu(env['choose_level_menu']) 
    
    def mouse_1_down(env):
        success, result = env['choose_level_menu'].click(mouse_position()) 
        if success:
            env['level_name'] = result
            launch_game_loop(env)
     
    pre_loop = pre_loop_
    keys[pg.KEYDOWN][K_ESCAPE] = set_start_menu
    keys[pg.MOUSEBUTTONDOWN][1] =  mouse_1_down
    
       
                      
def launch_level_editor(env):
    reset_camera()
    editor = LevelEditor()
    editor.run()
    reset_camera()
    launch_start_menu(env)
          
          
                      
if __name__ == '__main__':
    env = {}
    pre_loop = launch_start_menu
    post_loop = nothing
    reset_keys(None)
    init_game()
    while True:
        pre_loop(env)
        main_loop(env)
        post_loop(env)
        pg.display.flip()
