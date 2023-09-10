import pygame as pg
import time
import numpy as np

SOUND_DIR = 'sounds/'

pg.mixer.init()
SOUND_HIT = pg.mixer.Sound(SOUND_DIR + 'hit01.wav')
SOUND_HIT.set_volume(0.2)
SOUND_WIN = pg.mixer.Sound(SOUND_DIR + 'yeah2.wav')
SOUND_WIN.set_volume(2)
SOUND_BACKGROUND = pg.mixer.Sound(SOUND_DIR + 'background1.wav')
SOUND_BACKGROUND.set_volume(0.4)
SOUND_STRECH = pg.mixer.Sound(SOUND_DIR + 'strech.wav')
SOUND_STRECH.set_volume(0.4)

def play_sound(sound):
    sound.play()
    
def stop_sound(sound):
    sound.stop()

WIDTH = 800
HEIGHT = 600
OFFSET_HORIZONTAL = 0
OFFSET_VERTICAL = 0
FACTOR_SCALE = 1

    
TEXTURE_BACKGROUND = 'grass.jpg' 
TEXTURE_HOLE = 'hole4.png' 
TEXTURE_GOLFBALL = 'golfball.png'  
TEXTURE_KINETIC_BODY = 'plank.jpg' 
TEXTURE_STATIC_BODY = 'brickwall.jpg' 
TEXTURE_TRASHCAN = 'trashcan.png'
TEXTURE_SAVE = 'save.png'
TEXTURE_HOME = 'home.png'
TEXTURE_BARRIER = 'barrier.jpg'
TEXTURE_STATIC = 'static.png'
TEXTURE_KINETIC = 'kinetic.png'
TEXTURE_GAME = 'game_grass.png'
TEXTURE_LINE = 'line.png'
TEXTURE_TRIANGLE = 'triangle.png'
TEXTURE_QUAD = 'quad.png'
TEXTURE_BALL = 'ball.png'
TEXTURE_POLYGON = 'polygon.png'
TEXTURE_BACK = 'back.png'
TEXTURE_STAR = 'gold_star2.png'
TEXTURE_LEVEL_EDITOR = 'level_editor.jpg'
TEXTURE_CHOOSE_LEVEL = 'choose_level.jpg'
TEXTURE_LEVEL_1 = 'level_01.jpg'
TEXTURE_LEVEL_2 = 'level_02.jpg'
TEXTURE_LEVEL_3 = 'level_03.jpg'
TEXTURE_LEVEL_4 = 'level_04.jpg'

COLOR_BARRIER = [0.3, 0.2, 0.1]
COLOR_1 = (0.3, 0.8, 0.1)
COLOR_HOLE_IN = (0.3, 0.3, 0.3)
COLOR_HOLE_OUT = (0.0, 0.0, 0.0)
    
FRICTION_GOLF = 0.3    
    
W = 16
H = 9
SIZE = 100
SIZE_BALL = 20
SIZE_HOLE = 30
SIZE_STAR = 30
SIZE_BUTTON = 50
SIZE_MENU_BUTTON = 150

RESOLUTION_BALL = 32
RESOLUTION_HOLE = 16
RESOLUTION_STAR = 8

OFFSET_BUTTON = 35

SCALE_BACKGROUND = 10

LAST_UPDATE = time.time()
FRAMERATE = 0.01
MOUSEBUTTONDOWN_TIME = 0
MAX_MOUSEBUTTONDOWN_TIME = 2
MOUSEBUTTONDOWN_PRESSED = False

LINE_WIDTH = 5
POINT_SIZE = 5
WIDTH_BARRIER = 5



