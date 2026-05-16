"""
Enemy class handles enemy ships, their movement, and explosions
"""
import os
import random
import pygame
from settings import *


class Enemy:
    def __init__(self):
        self.x = random.randint(10, 720)
        self.y = random.randint(50, 200)
        self.x_change = ENEMY_SPEED
        self.y_change = 50
        self._load_variant()

        # Explosion
        self.explosion_visible = False
        self.explosion_timer = 0
        self.explosion_duration = EXPLOSION_DURATION
        self.explosion_x = 0
        self.explosion_y = 0
        self.active_explode_img = None

    def update(self):
        """Update enemy position and explosion timer each frame"""
        self.x += self.x_change

        if self.x <= 5:
            self.x = 5
            self.x_change *= -1
            self.y += self.y_change
        if self.x >= 730:
            self.x = 730
            self.x_change *= -1
            self.y += self.y_change

        # Explosion timer
        if self.explosion_visible:
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_duration:
                self.explosion_visible = False

    def draw(self, screen):
        """Draw the enemy ship and any active explosion"""
        screen.blit(self.img, (self.x, self.y))

        if self.explosion_visible:
            screen.blit(self.active_explode_img, (self.explosion_x, self.explosion_y))

    def explode(self, sound_manager):
        """Trigger explosion at current position (call before respawn)"""
        self.active_explode_img = self.explode_img
        self.explosion_visible = True
        self.explosion_timer = 0
        self.explosion_x = self.x - 32
        self.explosion_y = self.y - 32
        sound_manager.play('enemy_explosion')

    def respawn(self):
        """Move enemy to a new random position with a new random variant"""
        self._load_variant()
        self.x = random.randint(10, 720)
        self.y = random.randint(50, 200)

    def _load_variant(self):
        """Pick an enemy variant based on frequency weights — ship, explosion and laser images that match"""
        # Extract weights from settings
        weights = [v['spawn_weight'] for v in ENEMY_VARIANTS]
        variant = random.choices(ENEMY_VARIANTS, weights=weights, k=1)[0]
        
        self.img = pygame.image.load(os.path.join(IMAGES_PATH, variant['ship']))
        self.explode_img = pygame.image.load(os.path.join(IMAGES_PATH, variant['explode']))
        self.laser_img = pygame.image.load(os.path.join(IMAGES_PATH, variant['laser']))
        
        # Difficulty stats
        self.speed_mult = variant['speed_mult']
        self.fire_mult = variant['fire_mult']
        
        # Apply speed multiplier to movement (ensuring we keep the current direction)
        direction = 1 if self.x_change >= 0 else -1
        self.x_change = ENEMY_SPEED * self.speed_mult * direction