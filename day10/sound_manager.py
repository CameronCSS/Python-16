"""
SoundManager handles loading and playing all game sounds
"""
import os
import pygame
from pygame import mixer
from settings import *


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'fire': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, FIRE_SOUND)),
            'enemy_explosion': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, ENEMY_EXPLOSION_SOUND)),
            'player_explosion': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, PLAYER_EXPLOSION_SOUND)),
            'enemy_shot': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, ENEMY_SHOT_SOUND)),
            'success': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, SUCCESS_SOUND)),
            'lose_life': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, LOSE_LIFE_SOUND)),
            'game_over': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, GAME_OVER_SOUND)),
        }

    def play(self, name):
        """Play a sound effect by name"""
        self.sounds[name].play()

    def play_music(self):
        """Start looping background music"""
        mixer.music.load(os.path.join(SOUNDS_PATH, BG_MUSIC))
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    def stop_music(self):
        """Stop background music"""
        mixer.music.stop()