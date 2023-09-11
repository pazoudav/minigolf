import numpy as np
from math import *
   
   
def list_to_float(l):
    return [float(x) for x in l]
        
def list_list_to_float(ll):
    return [list_to_float(l) for l in ll]     
        
class Shape:
    
    def __init__(self, position): 
        self.pos = np.array(position, dtype=np.float64)
        self.points = []
        
    def set_position(self, new_pos):
        delta = new_pos - self.pos
        self.points += delta
        self.pos = new_pos
    
    def rotate(self, rad):
        # rad = rad * 2*pi
        self.points -= self.pos
        self.points = np.matmul([[cos(rad), sin(rad)], [-sin(rad), cos(rad)]], self.points.T).T
        self.points += self.pos
        
    def get_outside(self):
        return np.array(self.points)
    
    def __dict__(self):
        d = {}
        d['type'] = 'general'
        d['position'] = list_to_float(self.pos)
        d['parameters'] = list_list_to_float(self.points)
        return d
        
class Point(Shape):
    def __init__(self, position):
        super(Point, self).__init__(position)
        self.points = [position]

class Line(Shape):
    
    def __init__(self, point_a, point_b):
        super(Line, self).__init__(point_a)
        self.points.append(point_a)
        self.points.append(point_b)
        
    def __dict__(self):
        d = super().__dict__()
        d['type'] = 'Line'
        d['parameters'] = list_to_float(self.points[1])
        return d

class Triangle(Shape):
    def __init__(self, point_a, point_bc):
        super(Triangle, self).__init__(point_a)
        self.points.append(point_a)
        self.points.append(point_bc[0])
        self.points.append(point_bc[1])
        
    def __dict__(self):
        d = super().__dict__()
        d['type'] = 'Triangle'
        d['parameters'] = list_list_to_float([self.points[1], self.points[2]])
        return d

class Quad(Shape):
    
    def __init__(self, position, size):
        super(Quad, self).__init__(position)
        self.side_a, self.side_b = size
        self.points.append([self.pos[0] - self.side_a/2, self.pos[1] - self.side_b/2])
        self.points.append([self.pos[0] + self.side_a/2, self.pos[1] - self.side_b/2])
        self.points.append([self.pos[0] + self.side_a/2, self.pos[1] + self.side_b/2])
        self.points.append([self.pos[0] - self.side_a/2, self.pos[1] + self.side_b/2])
        
    def get_corners(self):
        return np.array(self.points)
    
    def __dict__(self):
        d = super().__dict__()
        d['type'] = 'Quad'
        d['parameters'] = list_to_float([self.side_a, self.side_b])
        return d


class Polygon(Shape):
    
    def __init__(self, position, points):
        super(Polygon, self).__init__(position)
        self.points = np.array(points)
        
    def get_corners(self):
        return self.points
    
    def __dict__(self):
        d = super().__dict__()
        d['type'] = 'Polygon'
        return d


class Ball(Shape):
    
    def __init__(self, position, size):
        super(Ball, self).__init__(position)
        self.center = position
        self.radius, self.resolution = size
        self.points.append(self.center)
        self.texture_points = [[0.5, 0.5]]
        step = 2*pi/self.resolution
        radius_t = 0.3
        for i in range(int(self.resolution)):
            if self.resolution % 2 == 0:
                self.points.append([self.pos[0] + self.radius*sin(i*step + step/2), self.pos[1] + self.radius*cos(i*step + step/2)])
            else:  
                self.points.append( [self.pos[0] + self.radius*cos(i*step + pi/2), self.pos[1] + self.radius*sin(i*step + pi/2)])
                
    def get_outside(self):
        return np.array(self.points[1:])
    
    def set_position(self, new_pos):
        super().set_position(new_pos)
        self.center = new_pos
    
    def __dict__(self):
        d = super().__dict__()
        d['type'] = 'Ball'
        d['parameters'] = list_to_float([self.radius, self.resolution])
        return d
    
    
                                
