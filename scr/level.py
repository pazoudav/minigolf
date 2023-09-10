import json
from bodies import *
from material import *
from utils import *
import os


class Level():
    
    def __init__(self, name):
        self.set_name(name)
        self.played = 0
        self.size = []
        self.ball = None
        self.hole = None
        self.background = []
        self.barrier = []
        self.statics = []
        self.kinetics = []
        self.stars = []
        self.all_bodies = []
        
    def set_name(self, name):
        self.filename = '../levels/' + name + '.json'
        self.name = name
    
    def load(self):
        with open(self.filename) as f:
            data = json.load(f)
            self.size = np.array(data['size'])
            ball_data = data['ball']
            hole_data = data['hole']
            barrier_data = data['barrier']
            statics_data = data['statics']
            kinetics_data = data['kinetics']   
            stars_data = data['stars']  
            
        self.add_background()
        self.add_hole(hole_data['position'])
        self.add_ball(ball_data['position'])
        self.add_barrier(barrier_data)
        
        for star_pos in stars_data:
            self.add_star(star_pos)
          
        for body in kinetics_data:
            if body['type'] == "Quad":
                shape_class = Quad
            elif body['type'] == "Ball":
                shape_class = Ball
            elif body['type'] == "Line":
                shape_class = Line
            elif body['type'] == "Triangle":
                shape_class = Triangle
            elif body['type'] == "Polygon":
                shape_class = Polygon
                
            k = KineticBody(
                        shape_class(
                            body['position'], 
                            body['parameters']), 
                        eval(body['program']), 
                        Texture(TEXTURE_KINETIC_BODY))
            self.add_kinetic_body(k)
            
        for body in statics_data:
            if body['type'] == "Quad":
                shape_class = Quad
            elif body['type'] == "Ball":
                shape_class = Ball
            elif body['type'] == "Line":
                shape_class = Line
            elif body['type'] == "Triangle":
                shape_class = Triangle
            elif body['type'] == "Polygon":
                shape_class = Polygon
                
            k = StaticBody(
                        shape_class(
                            body['position'], 
                            body['parameters']), Texture(TEXTURE_STATIC_BODY))
            self.add_static_body(k)
              
              
    def save(self, name):
        self.set_name(name)
        # if os.path.isfile(self.filename):
        #     return 'file already exists'
        with open(self.filename, 'w') as f:
            data = {}
            data['size'] = [int(x) for x in self.size]
            data['ball'] = {"position": list(self.ball.shape.pos)}
            data['hole'] = {"position": list(self.hole.shape.pos)}
            data['barrier'] = [list(p.shape.pos) for p in self.barrier] 
            data['statics'] = [st.__dict__() for st in self.statics if st not in self.barrier]
            data['kinetics'] = [ki.__dict__() for ki in self.kinetics]
            data['stars'] = [list(star.shape.pos) for star in self.stars]
            print(data)
            json.dump(data, f, indent=4)
            # try: 
            #     json.dump(data, f, indent=4)
            #     return 'save successful'
            # except:
            #     return 'save failed'
                  
    def stars_collected(self):
        count = 0
        for star in self.stars:
            if star.collected:
                count += 1
        return count   
                     
    def add_background(self):
        grass = StaticBody(Quad(self.size/2, SCALE_BACKGROUND*self.size), Texture(TEXTURE_BACKGROUND, scale=SCALE_BACKGROUND**2))
        grass.collision = GHOST
        self.background.append(grass)
        self.all_bodies.append(grass)
        
        
    def add_hole(self, position):
        self.remove(self.hole)
        self.hole = Hole(position)
        self.all_bodies.append(self.hole)
    
    
    def add_ball(self, position):
        self.remove(self.ball)
        self.ball = Golfball(position)
        self.all_bodies.append(self.ball)
        
        
    def add_static_body(self, body):
        self.statics.append(body)
        self.all_bodies.append(body)
        
        
    def add_kinetic_body(self, body):
        self.kinetics.append(body)
        self.all_bodies.append(body)
        
        
    #TODO remove barrier if present
    def add_barrier(self, points):
        for body in self.barrier:
            self.remove(body)
        for i in range(len(points)):
            body = StaticBody(Line(points[i-1], points[i]), OutlineColor([COLOR_BARRIER], width=WIDTH_BARRIER))
            self.barrier.append(body)
            self.all_bodies.append(body)
            self.statics.append(body)
        
        
    def add_star(self, position):
        star = Star(position)
        self.stars.append(star)
        self.all_bodies.append(star)
        
        
    def is_won(self):
        return np.linalg.norm(self.ball.shape.pos-self.hole.shape.pos) < SIZE_HOLE
            
            
    def reset(self):
        self.ball = None
        self.hole = None
        self.background = []
        self.barrier = []
        self.barrier = []
        self.statics = []
        self.kinetics = []
        self.stars = []
        self.all_bodies = []
        self.load()
        self.played = 0
        
        
    def remove(self, body):
        if body == self.ball:
            self.ball = None
        if body == self.hole:
            self.hole = None
        if body in self.background:
            self.background.remove(body)
        if body in self.barrier:
            self.barrier.remove(body)
        if body in self.barrier:
            self.barrier.remove(body)
        if body in self.statics:
            self.statics.remove(body)
        if body in self.kinetics:
            self.kinetics.remove(body)
        if body in self.stars:
            self.stars.remove(body)
        if body in self.all_bodies:
            self.all_bodies.remove(body)
        
        
    def is_ball_moving(self):
        return np.linalg.norm(self.ball.speed) > 0
    
    # def get_body(self, name):
    #     if name in self.all_bodies.named_bodies.keys():
    #         return self.all_bodies.named_bodies[name]
    #     else: 
    #         return False
        
