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
            'fail': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, FAIL_SOUND)),
            'bonus': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, BONUS_SOUND)),
            'boss_kill': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'boss_kill.mp3')),
            'boss_hit': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'boss_hit.mp3')),
            'danger': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'danger.mp3')),
            'powerup': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'powerup.mp3')),
            'explosion2': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'explosion2.mp3')),
        }
        self.danger_channel = None

    def play(self, name, loops=0):
        """Play a sound effect by name"""
        return self.sounds[name].play(loops=loops)

    def play_danger(self):
        """Play danger sound on loop"""
        if not self.danger_channel:
            self.danger_channel = self.play('danger', loops=-1)

    def stop_danger(self):
        """Stop the danger sound"""
        if self.danger_channel:
            self.danger_channel.stop()
            self.danger_channel = None

    def play_music(self):
        """Start looping regular background music"""
        mixer.music.load(os.path.join(SOUNDS_PATH, BG_MUSIC))
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    def stop_music(self):
        """Stop background music"""
        mixer.music.stop()

    def stop_all_sfx(self):
        """Stop all sound effect channels (not music)"""
        pygame.mixer.stop()