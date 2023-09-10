import numpy as np
from PIL import Image, ImageOps
from OpenGL.GL import *
from copy import deepcopy
from math import *

MODE_LOOP = 0
MODE_EXTEND = 1

class Material():
    def __init__(self, mode) -> None:
        self.mode = mode
        self.counter = 0
        self.data = []
        
    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if self.counter < len(self.data):
            ret = self.data[self.counter]
        elif self.mode == MODE_LOOP:
            self.counter = 0
            ret = self.data[self.counter]
        elif self.mode == MODE_EXTEND:
            ret = self.data[-1]
        self.counter += 1
        return ret
    
    def __getitem__(self, key):
        if key < len(self.data):
            ret = self.data[key]
        elif self.mode == MODE_LOOP:
            ret = self.data[key % len(self.data)]
        elif self.mode == MODE_EXTEND:
            ret = self.data[-1]
        return ret
        
class Solid(Material):
    def __init__(self, mode) -> None:
        super(Solid, self).__init__(mode)
        
class SolidColor(Solid):
    def __init__(self, color, mode=MODE_EXTEND) -> None:
        super(SolidColor, self).__init__(mode)
        self.color = color
        self.data = self.color
        
class Texture(Solid):
    def __init__(self, filename, scale=1, offset=[0,0], mode=MODE_LOOP):
        super(Texture, self).__init__(mode)
        self.load(filename)
        self.scale = scale
        self.offset = offset
        # self.map(np.array(texture_points), scale, offset)
    
    def map(self, points):
        p = np.array(deepcopy(points))
        min_x = np.min(p.T[0])
        min_y = np.min(p.T[1])
        p = p - [min_x, min_y] 
        max_x = np.max(p.T[0])
        max_y = np.max(p.T[1])
        max_ = max(max_x, max_y)
        p = p/max_ 
        p = p*self.scale + self.offset
        self.texture_points = p 
        self.data = self.texture_points
        
        
    def load(self, filename):
        im = Image.open(f'textures/{filename}').convert('RGBA')
        im = im.rotate(180)
        im = ImageOps.mirror(im)
        data = np.asarray(im, dtype=np.uint8)
        # data = data*[1,1,1,0.5]
        # print(data)
        # print(data)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) 
        # if len(data[0][0]) == 3:
        #     t = GL_RGB
        # elif len(data[0][0]) == 4:
        #     t = GL_RGBA
        t = GL_RGBA
        glTexImage2D(GL_TEXTURE_2D, 0, t, im.width, im.height, 0, t, GL_UNSIGNED_BYTE, data)
        im.close()
        
        
class Outline(Material):
    def __init__(self, width, mode) -> None:
        super(Outline, self).__init__(mode)
        self.width = width
        
class OutlineColor(Outline):
    def __init__(self, color, width=3, mode=MODE_LOOP) -> None:
        super(OutlineColor, self).__init__(width, mode)  
        self.color = color
        self.data = self.color
    
