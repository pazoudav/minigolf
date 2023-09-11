import numpy as np
from shape import *
from math import pi
from material import *
import utils as ut

GHOST = 0
SOLID = 1

IGNORE = -1
ALLOWED = 0

LOWEST_SPEED = 0.01
STOP_SPEED = np.array([0.0, 0.0])

class BasicBody():
    def __init__(self, shape, material):
        self.shape = shape
        self.visible = True
        self.collision = SOLID
        self.material = material
        self.position = self.shape.pos
        if isinstance(self.material, Texture):
            self.material.map(self.shape.points)
        self.updated = False
        
    def update_position(self):
        raise Exception("BasicBody cant update position")
    
    def set_speed(self, new_speed):
        raise Exception("BasicBody cant update speed")
    
    def add_texture(self, filename, scale=1, offset=[0,0]):
        self.material = Texture(filename, scale, offset)
        self.material.map(self.shape.points)
        return self
        
    def __dict__(self):
        return self.shape.__dict__()
        
class StaticBody(BasicBody):
    def __init__(self, shape, material):
        super(StaticBody, self).__init__(shape, material)
        self.shape = shape
        self.speed = 0
        self.rotation = 0
        
    def set_speed(self, new_speed):
        ...
        
    def update_position(self, time):
        ...


class KineticBody(BasicBody):
    def __init__(self, shape, equation, material):
        super(KineticBody,  self).__init__(shape, material)
        self.shape = shape
        self.equation = equation
        self.time = 0.0
        self.speed = [0,0]
        self.rotation = 0
        
    def update_position(self, delta_t):
        if delta_t == 0:
            return
        self.time += delta_t
        vx, vy, r = self.equation(self.time)
        self.speed = np.array([vx,vy])
        self.rotation = r
        self.shape.set_position(self.shape.pos + self.speed*delta_t)
        self.shape.rotate(r*delta_t)
        self.position = self.shape.pos
        
    def set_speed(self, new_speed):
        ...
        
    def __dict__(self):
        d = super().__dict__()
        d['program'] = ""
        return d
        
        
class DynamicBody(BasicBody):
    def __init__(self, shape, material):
        super(DynamicBody, self).__init__(shape, material)
        self.shape = shape
        self.speed = STOP_SPEED
        self.rotation = 0.0
        self.friction = 0.0
        
    def apply_friction(self, delta_t):
        self.speed = self.speed*(1 - 2*self.friction*delta_t) if np.linalg.norm(self.speed) < 200 else self.speed*(1 - self.friction*delta_t)
        if np.linalg.norm(self.speed) < 10:
            self.speed = STOP_SPEED

    def update_position(self, delta_t):
        if (self.speed != 0).any():
            self.shape.set_position(self.shape.pos + self.speed*delta_t)
        if self.rotation != 0:
            self.shape.rotate(self.rotation*delta_t)
        self.position = self.shape.pos
        
    def set_speed(self, new_speed):
        self.speed = np.array(new_speed)


class Hole(StaticBody):
    def __init__(self, position):
        super(Hole, self).__init__(Ball(position, [ut.SIZE_HOLE, ut.RESOLUTION_HOLE]), Texture(ut.TEXTURE_HOLE)) # SolidColor([COLOR_HOLE_IN, COLOR_HOLE_OUT]))
        self.collision = GHOST


class Golfball(DynamicBody):
    def __init__(self, position):
        super(Golfball, self).__init__(Ball(position, [ut.SIZE_BALL, ut.RESOLUTION_BALL]), Texture(ut.TEXTURE_GOLFBALL))
        self.friction = ut.FRICTION_GOLF
        
        
class Star(StaticBody):
    def __init__(self, position):
        super(Star, self).__init__(Ball(position, [ut.SIZE_STAR, ut.RESOLUTION_STAR]), Texture(ut.TEXTURE_STAR))
        self.collision = GHOST
        self.collected = False
        
    def collect(self):
        self.visible = False
        self.collected = True


# class BodyCollection():
#     def __init__(self):
#         self.bodies = []
#         self.named_bodies = {}
#         self.counter = 0
        
#     def add(self, body):
#         self.bodies.append(body)           
    
#     def remove(self, body):
#         self.bodies.remove(body)
        
#     def name(self, body, name):
#         self.named_bodies[name] = body
        
#     def __iter__(self):
#         self.counter = 0
#         return self

#     def __next__(self):
#         if self.counter < len(self.bodies):
#             self.counter += 1
#             return self.bodies[self.counter-1]
#         else:
#             raise StopIteration
        
