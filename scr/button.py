from bodies import StaticBody
from shape import *


class BasicButton(StaticBody):
    def __init__(self, shape, material):
        super(StaticBody, self).__init__(shape, material)
        self.active = True
    
    def click(self):
        ...
    
    def is_selected(self, mouse_pos):
        if not self.active:
            return False
        ld_corner = self.shape.pos - [self.shape.side_a/2, self.shape.side_b/2]
        ru_corner = ld_corner + [self.shape.side_a, self.shape.side_b]
        return (mouse_pos > ld_corner).all() and (mouse_pos < ru_corner).all()


class Button(BasicButton):
    def __init__(self, position, a, b, function, material):
        super(Button, self).__init__(Quad(position, [a,b]), material)
        self.function = function
    
    def click(self):
        return self.function
          
          
class Switch(BasicButton):
    def __init__(self, position, center, radius, material_0, material_1, start_state=False):
        super(Switch, self).__init__(Ball(position, [center, radius]), material_0)
        self.state = start_state
        self.material_0 = material_0
        self.material_1 = material_1
        self.set_material()

    def set_material(self):
        if self.state:
            self.material = self.material_1
        else:
            self.material = self.material_0

    def click(self):
        self.state = not self.state
        self.material
    
