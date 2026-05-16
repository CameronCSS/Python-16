"""
Settings stores all the settings for the game
"""
import os

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font (path and size — can't create Font object before pygame.init())
FONT_PATH = 'Score.ttf'
FONT_SIZE_SM = 24
FONT_SIZE_MD = 32
FONT_SIZE_LG = 64

# Speed
PLAYER_SPEED = 6
ENEMY_SPEED = 6
FIREBALL_SPEED = 25
LASER_SPEED = 15

# Number of enemies (difficulty)
NUM_ENEMIES = 5

# Timers
EXPLOSION_DURATION = 20
INVINCIBLE_DURATION = 60
LASER_INTERVAL_MIN = 40
LASER_INTERVAL_MAX = 150

# Paths
IMAGES_PATH = os.path.join(os.getcwd(), 'images')
SOUNDS_PATH = os.path.join(os.getcwd(), 'sounds')

# Image filenames
PLAYER_IMG = 'ship.png'
PLAYER_LIVES_IMG = 'ship_smaller.png'
PLAYER_REDX_IMG = 'redx.png'
PLAYER_EXPLODE_IMG = 'Explode.png'
ENEMY_VARIANTS = [
    {
        'ship': 'enemy1.png', 'explode': 'enemyexplode1.png', 'laser': 'laser1.png',
        'speed_mult': 1.0, 'fire_mult': 1.0, 'spawn_weight': 70
    },
    {
        'ship': 'enemy2.png', 'explode': 'enemyexplode2.png', 'laser': 'laser2.png',
        'speed_mult': 1.5, 'fire_mult': 0.5, 'spawn_weight': 20
    },
    {
        'ship': 'enemy3.png', 'explode': 'enemyexplode3.png', 'laser': 'laser3.png',
        'speed_mult': 2.0, 'fire_mult': 0.3, 'spawn_weight': 10
    },
]
FIREBALL_IMG = 'fireball.png'
ICON_IMG = 'ufo.png'
BG_IMG = 'BG.jpg'

# Sound filenames
FIRE_SOUND = 'fire_shot.mp3'
ENEMY_EXPLOSION_SOUND = 'explosion_1.mp3'
PLAYER_EXPLOSION_SOUND = 'explosion_2.mp3'
ENEMY_SHOT_SOUND = 'enemy_shot.mp3'
SUCCESS_SOUND = 'success.mp3'
LOSE_LIFE_SOUND = 'lose_life.mp3'
GAME_OVER_SOUND = 'game_over.mp3'
BG_MUSIC = 'bg_music.mp3'