import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageOps
import numpy as np

WIDTH = 800
HEIGHT = 600

pg.display.init()
pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)

glLineWidth(4)
glPointSize(4)
# glEnable(GL_BLEND)
# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
# glBlendEquationSeparate(GL_FUNC_SUBTRACT, GL_FUNC_SUBTRACT)
# glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()    

gluOrtho2D(0, WIDTH, 0, HEIGHT)
glViewport(0, 0, WIDTH, HEIGHT)


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glClearColor(0.4, 0.4, 0.4, 1)
glClear(GL_COLOR_BUFFER_BIT)

filename = 'back.png'

im = Image.open(f'../textures/{filename}') #.convert('RGBA')
im = im.rotate(180)
im = ImageOps.mirror(im)
# data = list(im.getdata())
# print(list(im.getchannel('A').getdata()))
print(im.apply_transparency())
data = np.asarray(im)#, dtype=np.uint8)
# data = data / [1,1,1,255]
# print(data)
# exit(0)
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, im.width, im.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
im.close()

glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, texture)



glBegin(GL_QUADS)

# glColor3f(1, 0.7, 0.5)
glTexCoord2f(0,0)
glVertex2f(100,100)

glTexCoord2f(1,0)
glVertex2f(200,100)

glTexCoord2f(1,1)
glVertex2f(200,200)

glTexCoord2f(0,1)
glVertex2f(100,200)


glTexCoord2f(0,0)
glVertex2f(120,150)

glTexCoord2f(1,0)
glVertex2f(250,150)

glTexCoord2f(1,1)
glVertex2f(250,250)

glTexCoord2f(0,1)
glVertex2f(120,250)
glEnd()
pg.display.flip()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                quit()
