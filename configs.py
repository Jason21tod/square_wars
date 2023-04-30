from pygame import init, color, display, sprite


init()
white = color.Color(40, 50, 40)
red = color.Color(255,0,0)
blue =  color.Color(0,0,255)
bullet_collor = color.Color(0,180,0)
window = display.set_mode()


SIZE = width, height = display.Info().current_w, display.Info().current_h

SQUARE_SIZES = 20
NORMAL_BULLET_SIZE = 7
MIN_DISTANCE = 200
BULLET_SIZE = 20
SEE_COORDINATES = False

