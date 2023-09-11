


class Action():
     
    def __init__(self):
        ... 
        
class Collision(Action):
    
    def __init__(self, position, direction=[0,0]):
        super(Collision).__init__()
        self.position = position
        self.direction = direction
