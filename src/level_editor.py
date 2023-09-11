import sys
sys.path.append('C:/Users/pazou/Documents/CVUT/CGR/2D_game/engine')
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
import numpy as np
from shape import *
from bodies import *
from draw import draw_level, draw_body, draw_menu, set_mode
import utils as ut
from level import Level
from button import *
from menu import *

clock = pg.time.Clock() 
MODE = None
EMPTY_MEMORY = []
STATIC = 0
KINETIC = 1
DELTA = 10
SCALE_DELTA = 0.9

def move(event):
    if event.key == K_DOWN:
        ut.OFFSET_VERTICAL -= DELTA
    elif event.key == K_UP:
        ut.OFFSET_VERTICAL += DELTA
    elif event.key == K_LEFT:
        ut.OFFSET_HORIZONTAL -= DELTA
    elif event.key == K_RIGHT:
        ut.OFFSET_HORIZONTAL += DELTA
    elif event.key == 61: #plus
        ut.FACTOR_SCALE *= SCALE_DELTA
    elif event.key == 45: # minus
        ut.FACTOR_SCALE /= SCALE_DELTA

class LevelEditor():
    def __init__(self):
        self.level = Level('')
        self.level.size = np.array([ut.WIDTH,ut.HEIGHT])
        self.level.add_background()
        self.main_menu = Menu()
        # self.main_buttons = BodyCollection()
        self.main_menu.add_button('golfball',   Button([ut.OFFSET_BUTTON,540], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_ball, Texture(ut.TEXTURE_GOLFBALL)))
        self.main_menu.add_button('hole',       Button([ut.OFFSET_BUTTON,480], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_hole, Texture(ut.TEXTURE_HOLE)))
        self.main_menu.add_button('barrier',    Button([ut.OFFSET_BUTTON,420], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_barrier_launcher, Texture(ut.TEXTURE_BARRIER)))
        self.main_menu.add_button('static',     Button([ut.OFFSET_BUTTON,360], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_static_launcher, Texture(ut.TEXTURE_STATIC))) 
        self.main_menu.add_button('star',       Button([ut.OFFSET_BUTTON,300], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_star, Texture(ut.TEXTURE_STAR))) # star
        self.main_menu.add_button('save',       Button([ut.OFFSET_BUTTON,240], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.save, Texture(ut.TEXTURE_SAVE))) 
        # self.main_menu.add_button('delete',     Button([ut.OFFSET_BUTTON,180], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.basic_loop, Texture(ut.TEXTURE_TRASHCAN))) # delete
        self.main_menu.add_button('home',       Button([ut.OFFSET_BUTTON,180], ut.SIZE_BUTTON, ut.SIZE_BUTTON, None, Texture(ut.TEXTURE_HOME))) # back to menu
        
        self.shape_menu = Menu()
        self.shape_menu.add_button('line',      Button([ut.OFFSET_BUTTON,570], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_Line, Texture(ut.TEXTURE_LINE)))
        self.shape_menu.add_button('triangle',  Button([ut.OFFSET_BUTTON,510], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_Triangle, Texture(ut.TEXTURE_TRIANGLE)))
        self.shape_menu.add_button('quad',      Button([ut.OFFSET_BUTTON,450], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_Quad, Texture(ut.TEXTURE_QUAD)))
        self.shape_menu.add_button('ball',      Button([ut.OFFSET_BUTTON,390], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_Ball, Texture(ut.TEXTURE_BALL)))
        self.shape_menu.add_button('polygon',   Button([ut.OFFSET_BUTTON,330], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.add_Polygon, Texture(ut.TEXTURE_POLYGON)))
        self.shape_menu.add_button('back',      Button([ut.OFFSET_BUTTON,270], ut.SIZE_BUTTON, ut.SIZE_BUTTON, self.select_shape, Texture(ut.TEXTURE_BACK)))
        self.shape_menu.add_button('style',     Switch([ut.OFFSET_BUTTON,210], ut.SIZE_BUTTON, ut.SIZE_BUTTON, Texture(ut.TEXTURE_HOME), Texture(ut.TEXTURE_GOLFBALL)))
        self.shape_menu.deactivate_button('style')
        
        self.memory = EMPTY_MEMORY
        self.new_body_type = EMPTY_MEMORY
        
        self.next_loop = self.basic_loop
        
    def run(self):
        loop = self.basic_loop
        while self.next_loop is not None:
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
                    success, result = self.main_menu.click(ut.mouse_screen_position())    
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
                    self.level.add_ball(ut.mouse_world_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(ut.mouse_world_position()), OutlineColor([(0.1, 0.9, 0.2)], width=ut.SIZE_BALL*2/ut.FACTOR_SCALE)))


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
                    self.level.add_hole(ut.mouse_world_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(ut.mouse_world_position()), OutlineColor([(0.1, 0.3, 0.2)], width=ut.SIZE_HOLE*2/ut.FACTOR_SCALE)))


    def add_barrier_launcher(self):
        self.memory = []
        self.next_loop = self.add_barrier

    def add_barrier(self):
        self.next_loop = self.add_barrier
        res = 20
        mouse_pos = ut.mouse_world_position()//res * res + res/2
        draw_body(BasicBody(Point(mouse_pos), OutlineColor([(0.2, 0.3, 1)], width=10)))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.next_loop = self.basic_loop
                elif event.key == K_RETURN:
                    # print(self.memory)
                    self.level.add_barrier(deepcopy(self.memory))
                    self.next_loop = self.basic_loop
                else:
                    move(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    # print(list(mouse_pos))
                    self.memory.append(list(mouse_pos))
                    # print(self.memory)
        
        if len(self.memory) > 0:
            self.memory.append(mouse_pos)
            draw_body(StaticBody(Polygon([0,0], self.memory), OutlineColor([ut.COLOR_BARRIER])))
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
                    self.level.add_star(ut.mouse_world_position())
                    self.next_loop = self.basic_loop
        draw_body(BasicBody(Point(ut.mouse_world_position()), OutlineColor([(0.5, 0.5, 0.1)], width=ut.SIZE_STAR*2/ut.FACTOR_SCALE)))
                              
                        
    def add_static_launcher(self):
        self.new_body_type = STATIC
        self.memory = []
        self.next_loop = self.select_shape
        
    def add_static(self, shape):
        self.level.add_static_body(StaticBody(shape, Texture(ut.TEXTURE_STATIC_BODY)))
        
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
                    success, result = self.shape_menu.click(ut.mouse_screen_position()) 
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
                        self.memory = ut.mouse_world_position()
                    else:
                        shape = Line(self.memory, ut.mouse_world_position())
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
        if len(self.memory) > 0 :             
            draw_body(StaticBody(Line(self.memory, ut.mouse_world_position()), OutlineColor([ut.COLOR_BARRIER])))

    
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
                        self.memory = [ut.mouse_world_position()]
                    elif len(self.memory) == 1:
                        self.memory.append(ut.mouse_world_position())
                    elif len(self.memory) == 2:
                        shape = Triangle(ut.mouse_world_position(), self.memory)
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) == 1:
            draw_body(StaticBody(Line(self.memory[0], ut.mouse_world_position()), OutlineColor([ut.COLOR_BARRIER])))
        elif len(self.memory) == 2:
            draw_body(StaticBody(Triangle(ut.mouse_world_position(), self.memory), OutlineColor([ut.COLOR_BARRIER])))
    
    
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
                        self.memory = ut.mouse_world_position()
                    else:
                        shape = Quad(self.memory, np.abs(ut.mouse_world_position() - self.memory)*2)
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) > 0:
            draw_body(StaticBody(Quad(self.memory, np.abs(ut.mouse_world_position() - self.memory)*2), Texture(ut.TEXTURE_STATIC_BODY))) 

    
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
                        self.memory = ut.mouse_world_position()
                    else:
                        shape = Ball(self.memory, [np.linalg.norm(ut.mouse_world_position() - self.memory), 32])
                        if self.new_body_type == STATIC:
                            self.add_static(shape)
                        else:
                            self.add_kinetic(shape)
                        self.next_loop = self.basic_loop
                        
        if len(self.memory) > 0:
            draw_body(StaticBody(Ball(self.memory, [np.linalg.norm(ut.mouse_world_position() - self.memory), 32]), Texture(ut.TEXTURE_STATIC_BODY))) 

    
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
                    self.memory.append(ut.mouse_world_position())
                        
        if len(self.memory) > 0:
            self.memory.append(ut.mouse_world_position())
            draw_body(StaticBody(Polygon([0,0], self.memory), Texture(ut.TEXTURE_STATIC_BODY)))
            self.memory.pop()

                        
    def save(self):
        success = self.level.save('level_custom')
        print(f'save : {success}')
        self.next_loop = self.basic_loop

