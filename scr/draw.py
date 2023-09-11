from OpenGL.GL import *
from PIL import Image
import numpy as np
from material import *
from shape import *
from utils import *


    

def draw_level(level):
    # glClear(GL_COLOR_BUFFER_BIT) 
    for body in level.background:
        draw_body(body)
    if level.hole is not None:
        draw_body(level.hole)
    if level.ball is not None:
        draw_body(level.ball)
    for body in level.barrier:
        draw_body(body)
    for body in level.statics:
        draw_body(body)
    for body in level.stars:
        draw_body(body)
    for body in level.kinetics:
        draw_body(body)
        
def draw_menu(menu):
    for button in menu.buttons.values():
        draw_body(button)
    
def draw_power_bar(time_, ball_position, mouse_pos):
    t = np.min([2,time.time() - time_])/2
    diff = ball_position - mouse_pos
    diff /= np.linalg.norm(diff)
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.0,1,0.0)
    glVertex2f(*(ball_position + 50*diff))
    glColor3f(1.0, (1-t)*1, (1-t)*1)
    glVertex2f(*(ball_position + (50*(1.5*t+1))*diff))
    glEnd()
    glLineWidth(LINE_WIDTH)
    
def draw_aim_bar(ball_position, mouse_pos): 
    diff = ball_position - mouse_pos
    diff /= np.linalg.norm(diff)
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    glVertex2f(*(ball_position + 50*diff))
    glColor3f(1,1,1)
    glVertex2f(*(ball_position + (50*(2.5))*diff))
    glEnd()
    glLineWidth(LINE_WIDTH)

def draw_body(body):
    if not body.visible:
        return
    
    if isinstance(body.material, OutlineColor):
        draw_outside(body)
        return
    
    if isinstance(body.shape, Polygon):
        draw_polygon(body)
    elif isinstance(body.shape, Quad):  
        draw_quad(body)
    elif isinstance(body.shape, Ball):
        draw_ball(body)
    elif isinstance(body.shape, Triangle):
        draw_triangle(body)
    elif isinstance(body.shape, Line):
        draw_line(body)    
    elif isinstance(body.shape, Point):
        draw_outside(body)
        
    if isinstance(body.material, Texture):
        glDisable(GL_TEXTURE_2D)


def draw_outside(body):
    points = body.shape.get_outside()
    if isinstance(body.shape, Point):
        glPointSize(body.material.width)
        glBegin(GL_POINTS)
        glColor3f(*body.material[0])
        glVertex2f(*points[0])
        glEnd()
        glPointSize(POINT_SIZE)
    else:
        glLineWidth(body.material.width)
        glBegin(GL_LINE_LOOP)
        for i in range(len(points)):
            glColor3f(*body.material[i])
            glVertex2f(*points[i])
        glEnd()  
        glLineWidth(LINE_WIDTH)  


def draw_full_shape_helper(material):
    if isinstance(material, Texture):
        glBindTexture(GL_TEXTURE_2D, material.texture)
        glEnable(GL_TEXTURE_2D)
        return glTexCoord2f
    else: 
        return glColor3f


def draw_ball(ball):    
    vertex_param_func = draw_full_shape_helper(ball.material)
    glBegin(GL_TRIANGLE_FAN)
    points = ball.shape.points
    for i, point in enumerate(points):
        vertex_param_func(*ball.material[i])
        glVertex2f(*point)
    vertex_param_func(*ball.material[1])    
    glVertex2f(*points[1])
    glEnd()
        
    # glBegin(GL_LINES)
    # glColor3f(0.8, 0.1, 0.8)
    # glVertex2f(*ball.position)
    # glVertex2f(*(ball.position + ball.speed))
    # glEnd()
    
def draw_quad(quad):
    vertex_param_func = draw_full_shape_helper(quad.material)
    glBegin(GL_QUADS)
    points = quad.shape.get_outside()
    for i, point in enumerate(points):
        vertex_param_func(*quad.material[i])
        glVertex2f(*point)
    glEnd()

    
def draw_polygon(polygon):
    vertex_param_func = draw_full_shape_helper(polygon.material)
    glBegin(GL_TRIANGLE_STRIP)
    points = polygon.shape.get_outside()
    for i, point in enumerate(points):
        vertex_param_func(*polygon.material[i])
        glVertex2f(*point)
    glEnd()
    
def draw_triangle(triangle):
    draw_polygon(triangle)
    
def draw_line(line):
    vertex_param_func = draw_full_shape_helper(line.material)
    glBegin(GL_LINES)
    points = line.shape.get_outside()
    for i, point in enumerate(points):
        vertex_param_func(*line.material[i])
        glVertex2f(*point)
    glEnd()


    
# def draw_point(point):
#     vertex_param_func = draw_full_shape_helper(point.material)
#     glBegin(GL_POINTS)
#     points = point.shape.get_outside()
#     for i, point in enumerate(points):
#         vertex_param_func(*point.material[i])
#         glVertex2f(*point)
#     glEnd()