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
        # Allocate 64 channels to prevent standard sounds (fire, enemy explosions) from dropping
        pygame.mixer.set_num_channels(64)
        
        # Reserve the first 8 channels for high-priority sounds so they are never interrupted
        pygame.mixer.set_reserved(8)
        
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
            'multiply': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'multiply.mp3')),
        }
        
        # Explicit priority channel mapping
        self.priority_channels = {
            'multiply': 0,        # Multiplier sound
            'boss_kill': 1,         # Regular Boss explosion
            'lose_life': 2,         # Taking damage
            'bonus': 3,             # Gaining life / overshield
            'player_explosion': 4,  # Player blowing up
            'powerup': 5,           # Triple shot activated
            'danger': 6,            # Boss incoming alarm
            'game_over': 7          # Game over state
        }
        self.danger_channel = pygame.mixer.Channel(6)

    def play(self, name, loops=0):
        """Play a sound effect by name, routing priority sounds to their reserved channels"""
        if name in self.priority_channels:
            channel_id = self.priority_channels[name]
            channel = pygame.mixer.Channel(channel_id)
            channel.play(self.sounds[name], loops=loops)
            return channel
        else:
            return self.sounds[name].play(loops=loops)

    def play_danger(self):
        """Play danger sound on loop using its reserved channel"""
        self.danger_channel.play(self.sounds['danger'], loops=-1)

    def stop_danger(self):
        """Stop the danger sound"""
        self.danger_channel.stop()

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