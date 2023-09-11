
LEFT = -1
TOP = -1
CENTER = 0
RIGHT = 1
UP = 1

class Menu():
    def __init__(self, grid = [], v_alignment=CENTER, h_alignment=CENTER):
        self.grid = grid
        self.v_alignment = v_alignment
        self.h_alignment = h_alignment
        self.buttons = {}
    
    def add_button(self, id, button):
        self.buttons[id] = button
        
    def click(self, mouse_pos):
        for button in self.buttons.values():
            if button.is_selected(mouse_pos):
                return True, button.click()
        return False, None
            
    def activate_button(self, id):
        self.buttons[id].visible = True
        self.buttons[id].active = True
    
    def deactivate_button(self, id):
        self.buttons[id].visible = False
        self.buttons[id].active = False
        
    def remove(self, id):
        self.buttons.pop(id)
        

    