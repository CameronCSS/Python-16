"""
Settings stores all the settings for the game
"""
import os

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font (path and size — can't create Font object before pygame.init())
FONT_PATH = 'Score.ttf'
FONT_SIZE_XS = 18
FONT_SIZE_SM = 24
FONT_SIZE_MD = 32
FONT_SIZE_LG = 64

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (100, 150, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (150, 150, 150)

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
        'ship': 'enemy1.png', 'explode': 'enemyexplosion1.png', 'laser': 'laser1.png',
        'speed_mult': 1.0, 'fire_mult': 1.0, 'spawn_weight': 70, 'points': 100
    },
    {
        'ship': 'enemy2.png', 'explode': 'enemyexplosion2.png', 'laser': 'laser2.png',
        'speed_mult': 1.5, 'fire_mult': 0.5, 'spawn_weight': 20, 'points': 200
    },
    {
        'ship': 'enemy3.png', 'explode': 'enemyexplosion3.png', 'laser': 'laser3.png',
        'speed_mult': 2.0, 'fire_mult': 0.25, 'spawn_weight': 10, 'points': 300
    },
]
FIREBALL_IMG = 'fireball.png'
BLUE_FIREBALL_IMG = 'bluefireball.png'
BOSS_IMG = 'boss.png'
MEGA_BOSS_IMG = 'mega_boss.png'
ICON_IMG = 'alien.png'
BG_IMG = 'BG.jpg'

# Sound filenames
FIRE_SOUND = 'fire_shot.mp3'
ENEMY_EXPLOSION_SOUND = 'explosion_1.mp3'
PLAYER_EXPLOSION_SOUND = 'explosion_2.mp3'
ENEMY_SHOT_SOUND = 'enemy_shot.mp3'
SUCCESS_SOUND = 'success.mp3'
LOSE_LIFE_SOUND = 'lose_life.mp3'
GAME_OVER_SOUND = 'game_over.mp3'
FAIL_SOUND = 'fail.mp3'
BONUS_SOUND = 'bonus.mp3'
BG_MUSIC = 'bg_music.mp3'