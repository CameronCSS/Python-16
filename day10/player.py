"""
Player class handles the player ship, fireball, lives, and explosions
"""
import os
import pygame
from settings import *


class Player:
    def __init__(self):
        # Player ship
        self.img = pygame.image.load(os.path.join(IMAGES_PATH, PLAYER_IMG))
        self.x = 368
        self.y = 520
        self.x_change = 0
        self.lives = 3

        # Fireball
        self.fireball_img = pygame.image.load(os.path.join(IMAGES_PATH, FIREBALL_IMG))
        self.fireball_x = 0
        self.fireball_y = 520
        self.fireball_y_change = FIREBALL_SPEED
        self.fireball_visible = False

        # Player explosion
        self.explode_img = pygame.image.load(os.path.join(IMAGES_PATH, PLAYER_EXPLODE_IMG))
        self.explosion_visible = False
        self.explosion_timer = 0
        self.explosion_duration = EXPLOSION_DURATION

        # Invincibility after being hit
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = INVINCIBLE_DURATION

        # Lives display images
        self.lives_img = pygame.image.load(os.path.join(IMAGES_PATH, PLAYER_LIVES_IMG))
        self.redx_img = pygame.image.load(os.path.join(IMAGES_PATH, PLAYER_REDX_IMG))

    def update(self):
        """Update player position, fireball, explosion, and invincibility each frame"""
        # Movement
        self.x += self.x_change
        if self.x <= 5:
            self.x = 5
        if self.x >= 730:
            self.x = 730

        # Fireball movement
        if self.fireball_visible:
            self.fireball_y -= self.fireball_y_change
            if self.fireball_y < 0:
                self.fireball_visible = False
                self.fireball_y = self.y

        # Explosion timer
        if self.explosion_visible:
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_duration:
                self.explosion_visible = False
                # Reset player position after explosion
                self.x = 368
                self.y = 520

        # Invincibility timer
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer >= self.invincible_duration:
                self.invincible = False

    def draw(self, screen):
        """Draw the player ship, fireball, and explosion"""
        # Flash every 6 frames when invincible
        if not (self.invincible and (self.invincible_timer // 6) % 2 == 0):
            screen.blit(self.img, (self.x, self.y))

        # Draw fireball
        if self.fireball_visible:
            screen.blit(self.fireball_img, (self.fireball_x + 16, self.fireball_y + 10))

        # Draw player explosion
        if self.explosion_visible:
            screen.blit(self.explode_img, (self.x - 32, self.y - 32))

    def draw_lives(self, screen):
        """Draw the lives indicator bar"""
        bar = pygame.Surface((120, 45), pygame.SRCALPHA)
        bar.fill((0, 60, 80, 180))
        screen.blit(bar, (0, 0))
        for i in range(3):
            if i < self.lives:
                screen.blit(self.lives_img, (10 + i * (self.lives_img.get_width() + 5), 8))
            else:
                screen.blit(self.redx_img, (10 + i * (self.lives_img.get_width() + 5), 8))

    def shoot(self, sound_manager):
        """Fire a fireball if one isn't already active"""
        if not self.fireball_visible:
            self.fireball_visible = True
            self.fireball_x = self.x
            self.fireball_y = self.y
            sound_manager.play('fire')

    def hit(self, sound_manager):
        """Handle the player being hit — start explosion, lose a life, become invincible"""
        self.explosion_visible = True
        self.explosion_timer = 0
        self.invincible = True
        self.invincible_timer = 0
        self.lives -= 1
        sound_manager.play('player_explosion')
        sound_manager.play('lose_life')

    def reset(self):
        """Full reset for game restart"""
        self.x = 368
        self.y = 520
        self.x_change = 0
        self.lives = 3
        self.fireball_visible = False
        self.fireball_y = 520
        self.explosion_visible = False
        self.invincible = False