import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
import numpy as np
from shape import *
from bodies import *
import time
from draw import draw_level, draw_body, draw_menu
from utils import *
from level import *
from button import *
from menu import *

clock = pg.time.Clock() 
MODE = None
EMPTY_MEMORY = []
STATIC = 0
KINETIC = 1
DELTA = 10
SCALE_DELTA = 0.9

def mouse_position():
    return np.array([pg.mouse.get_pos()[0]*FACTOR_SCALE + OFFSET_HORIZONTAL, (HEIGHT-pg.mouse.get_pos()[1])*FACTOR_SCALE + OFFSET_VERTICAL])

def move(event):
    global OFFSET_HORIZONTAL, OFFSET_VERTICAL, FACTOR_SCALE
    if event.key == K_DOWN:
        OFFSET_VERTICAL -= DELTA
    elif event.key == K_UP:
        OFFSET_VERTICAL += DELTA
    elif event.key == K_LEFT:
        OFFSET_HORIZONTAL -= DELTA
    elif event.key == K_RIGHT:
        OFFSET_HORIZONTAL += DELTA
    elif event.key == 61: #plus
        FACTOR_SCALE *= SCALE_DELTA
    elif event.key == 45: # minus
        FACTOR_SCALE /= SCALE_DELTA

class LevelEditor():
    def __init__(self):
        self.level = Level('')
        self.level.size = np.array([WIDTH,HEIGHT])
        self.level.add_background()
        self.main_menu = Menu()
        # self.main_buttons = BodyCollection()
        self.main_menu.add_button('golfball',   Button([OFFSET_BUTTON,540], SIZE_BUTTON, SIZE_BUTTON, self.add_ball, Texture(TEXTURE_GOLFBALL)))
        self.main_menu.add_button('hole',       Button([OFFSET_BUTTON,480], SIZE_BUTTON, SIZE_BUTTON, self.add_hole, Texture(TEXTURE_HOLE)))
        self.main_menu.add_button('barrier',    Button([OFFSET_BUTTON,420], SIZE_BUTTON, SIZE_BUTTON, self.add_barrier_launcher, Texture(TEXTURE_BARRIER)))
        self.main_menu.add_button('static',     Button([OFFSET_BUTTON,360], SIZE_BUTTON, SIZE_BUTTON, self.add_static_launcher, Texture(TEXTURE_STATIC))) 
        self.main_menu.add_button('star',       Button([OFFSET_BUTTON,300], SIZE_BUTTON, SIZE_BUTTON, self.add_star, Texture(TEXTURE_STAR))) # star
        self.main_menu.add_button('save',       Button([OFFSET_BUTTON,240], SIZE_BUTTON, SIZE_BUTTON, self.save, Texture(TEXTURE_SAVE))) 
        # self.main_menu.add_button('delete',     Button([OFFSET_BUTTON,180], SIZE_BUTTON, SIZE_BUTTON, self.basic_loop, Texture(TEXTURE_TRASHCAN))) # delete
        self.main_menu.add_button('home',       Button([OFFSET_BUTTON,180], SIZE_BUTTON, SIZE_BUTTON, None, Texture(TEXTURE_HOME))) # back to menu
        
        self.shape_menu = Menu()
        self.shape_menu.add_button('line',      Button([OFFSET_BUTTON,570], SIZE_BUTTON, SIZE_BUTTON, self.add_Line, Texture(TEXTURE_LINE)))
        self.shape_menu.add_button('triangle',  Button([OFFSET_BUTTON,510], SIZE_BUTTON, SIZE_BUTTON, self.add_Triangle, Texture(TEXTURE_TRIANGLE)))
        self.shape_menu.add_button('quad',      Button([OFFSET_BUTTON,450], SIZE_BUTTON, SIZE_BUTTON, self.add_Quad, Texture(TEXTURE_QUAD)))
        self.shape_menu.add_button('ball',      Button([OFFSET_BUTTON,390], SIZE_BUTTON, SIZE_BUTTON, self.add_Ball, Texture(TEXTURE_BALL)))
        self.shape_menu.add_button('polygon',   Button([OFFSET_BUTTON,330], SIZE_BUTTON, SIZE_BUTTON, self.add_Polygon, Texture(TEXTURE_POLYGON)))
        self.shape_menu.add_button('back',      Button([OFFSET_BUTTON,270], SIZE_BUTTON, SIZE_BUTTON, self.select_shape, Texture(TEXTURE_BACK)))
        self.shape_menu.add_button('style',     Switch([OFFSET_BUTTON,210], SIZE_BUTTON, SIZE_BUTTON, Texture(TEXTURE_HOME), Texture(TEXTURE_GOLFBALL)))
        self.shape_menu.deactivate_button('style')
        
        self.memory = EMPTY_MEMORY
        self.new_body_type = EMPTY_MEMORY
        
        self.next_loop = self.basic_loop
        
    def run(self):
        loop = self.basic_loop
        while self.next_loop is not None:
            set_mode()
            draw_level(self.level)
            self.next_loop()  
            pg.display.flip()

    def basic_loop(self):
        self.next_loop = self.basic_loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = None
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    success, result = self.main_menu.click(mouse_position())    
                    if success:
                        self.next_loop = result                       
        draw_menu(self.main_menu)


    def add_ball(self):
        self.next_loop = self.add_ball
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    self.level.add_ball(mouse_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(mouse_position()), OutlineColor([(0.1, 0.9, 0.2)], width=SIZE_BALL*2)))


    def add_hole(self):
        self.next_loop = self.add_hole
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    self.level.add_hole(mouse_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(mouse_position()), OutlineColor([(0.1, 0.3, 0.2)], width=SIZE_HOLE*2)))


    def add_barrier_launcher(self):
        self.memory = []
        self.next_loop = self.add_barrier

    def add_barrier(self):
        self.next_loop = self.add_barrier
        res = 20
        mouse_pos = mouse_position()//res * res + res/2
        draw_body(BasicBody(Point(mouse_pos), OutlineColor([(0.2, 0.3, 1)], width=10)))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                elif event.key == K_RETURN:
                    print(self.memory)
                    self.level.add_barrier(deepcopy(self.memory))
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    print(list(mouse_pos))
                    self.memory.append(list(mouse_pos))
                    print(self.memory)
        
        if len(self.memory) > 0:
            self.memory.append(mouse_pos)
            draw_body(StaticBody(Polygon([0,0], self.memory), OutlineColor([COLOR_BARRIER])))
            self.memory.pop()
       
    def add_star(self):
        self.next_loop = self.add_star
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    self.level.add_star(mouse_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(mouse_position()), OutlineColor([(0.5, 0.5, 0.1)], width=SIZE_STAR*2)))
                              
                        
    def add_static_launcher(self):
        self.new_body_type = STATIC
        self.memory = []
        self.next_loop = self.select_shape
        
    def add_static(self, shape):
        self.level.add_static_body(StaticBody(shape, Texture(TEXTURE_STATIC_BODY)))
        
    def add_kinetic(self, shape):
        ...
    
    def select_shape(self):
        self.next_loop = self.select_shape
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    success, result = self.shape_menu.click(mouse_position()) 
                    if success:
                        self.memory = []
                        self.next_loop = result  
        draw_menu(self.shape_menu) 

                        
    def add_Line(self):
        self.next_loop = self.add_Line
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.select_shape
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.memory == EMPTY_MEMORY:
                        self.memory = mouse_position()
                    else:
                        shape = Line(self.memory, mouse_position())
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
        if len(self.memory) > 0 :             
            draw_body(StaticBody(Line(self.memory, mouse_position()), OutlineColor([COLOR_BARRIER])))

    
    def add_Triangle(self):
        self.next_loop = self.add_Triangle
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.memory) == 0:
                        self.memory = [mouse_position()]
                    elif len(self.memory) == 1:
                        self.memory.append(mouse_position())
                    elif len(self.memory) == 2:
                        shape = Triangle(mouse_position(), self.memory)
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) == 1:
            draw_body(StaticBody(Line(self.memory[0], mouse_position()), OutlineColor([COLOR_BARRIER])))
        elif len(self.memory) == 2:
            draw_body(StaticBody(Triangle(mouse_position(), self.memory), OutlineColor([COLOR_BARRIER])))
    
    
    def add_Quad(self):
        self.next_loop = self.add_Quad
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.memory) == 0:
                        self.memory = mouse_position()
                    else:
                        shape = Quad(self.memory, np.abs(mouse_position() - self.memory)*2)
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) > 0:
            draw_body(StaticBody(Quad(self.memory, np.abs(mouse_position() - self.memory)*2), Texture(TEXTURE_STATIC_BODY))) 

    
    def add_Ball(self):
        self.next_loop = self.add_Ball
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.memory) == 0:
                        self.memory = mouse_position()
                    else:
                        shape = Ball(self.memory, [np.linalg.norm(mouse_position() - self.memory), 32])
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) > 0:
            draw_body(StaticBody(Ball(self.memory, [np.linalg.norm(mouse_position() - self.memory), 32]), Texture(TEXTURE_STATIC_BODY))) 

    
    def add_Polygon(self):
        self.next_loop = self.add_Polygon
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                elif event.key == K_RETURN:
                    shape = Polygon(self.memory[0], self.memory)
                    if self.new_body_type == STATIC:
                        self.add_static(shape)
                    else:
                        self.add_kinetic(shape)
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.memory.append(mouse_position())
                        
        if len(self.memory) > 0:
            self.memory.append(mouse_position())
            draw_body(StaticBody(Polygon([0,0], self.memory), OutlineColor([COLOR_BARRIER])))
            self.memory.pop()

                        
    def save(self):
        success = self.level.save('level_custom')
        print(f'save : {success}')
        self.next_loop = self.basic_loop


def init_game():
    pg.display.init()
    pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    glClearColor(0.3, 0.5, 0.2, 1.0)
    glLineWidth(LINE_WIDTH)
    glPointSize(4)
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
                        

if __name__ == "__main__":
    init_game()
    editor = LevelEditor()
    editor.run()