from controller import *
import utils as ut
from draw import draw_menu, set_mode
from button import Button
from material import Texture
from menu import Menu

class MenuController(Controller):
    def __init__(self, env, menu) -> None:
        super(MenuController, self).__init__(env)
        self.menu = menu
        self.keys[pg.KEYDOWN][K_ESCAPE] = quit_
        self.keys[pg.MOUSEBUTTONDOWN][1]  =  self.mouse_down_1
        
    def set_keys(self):
        self.keys[pg.KEYDOWN][K_ESCAPE] = quit_
        self.keys[pg.MOUSEBUTTONDOWN][1]  =  self.mouse_down_1
        
    def mouse_down_1(self):
        success, result = self.menu.click(ut.mouse_position()) 
        if success:
            result()
            
    def pre_loop(self):
        set_mode()
        draw_menu(self.menu) 
        
        
class EndMenuController(MenuController):
    def __init__(self, env) -> None:
        menu = Menu()
        menu.add_button('star1',   Button([200, 400], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: None, Texture(ut.TEXTURE_SAD_STAR)))
        menu.add_button('star2',   Button([400, 400], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: None, Texture(ut.TEXTURE_SAD_STAR)))
        menu.add_button('star3',   Button([600, 400], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: None, Texture(ut.TEXTURE_SAD_STAR)))
        menu.add_button('redo',    Button([500, 200], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['game'].launch(), Texture(ut.TEXTURE_REDO)))
        menu.add_button('home',    Button([300, 200], ut.SIZE_MENU_BUTTON, ut.SIZE_MENU_BUTTON, lambda: env['choose_level_menu'].launch(), Texture(ut.TEXTURE_HOME))) 
        super().__init__(env, menu)
          
    def launch_wrapper(self, n_starts):
        self.menu.buttons['star1'].add_texture(ut.TEXTURE_SAD_STAR)
        self.menu.buttons['star2'].add_texture(ut.TEXTURE_SAD_STAR)
        self.menu.buttons['star3'].add_texture(ut.TEXTURE_SAD_STAR)
        if (n_starts > 0):
            self.menu.buttons['star1'].add_texture(ut.TEXTURE_STAR)
        if (n_starts > 1):
            self.menu.buttons['star2'].add_texture(ut.TEXTURE_STAR)
        if (n_starts > 2):
            self.menu.buttons['star3'].add_texture(ut.TEXTURE_STAR)
        self.launch()
    

