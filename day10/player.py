"""
Player class handles the player ship, fireball, lives, and explosions
"""
import os
import pygame
from settings import *


class Player:
    def __init__(self):
        # Player ship variants
        self.img_idle = pygame.image.load(os.path.join(IMAGES_PATH, PLAYER_IMG))
        self.img_left = pygame.image.load(os.path.join(IMAGES_PATH, 'leftship.png'))
        self.img_right = pygame.image.load(os.path.join(IMAGES_PATH, 'rightship.png'))
        self.x = 368
        self.y = 520
        self.x_change = 0
        self.y_change = 0
        self.lives = 3

        # Fireball system
        self.fireball_img = pygame.image.load(os.path.join(IMAGES_PATH, FIREBALL_IMG))
        self.blue_fireball_img = pygame.image.load(os.path.join(IMAGES_PATH, BLUE_FIREBALL_IMG))
        self.fireballs = [] # List of {'x': float, 'y': float, 'x_ch': float, 'y_ch': float, 'img': Surface}
        self.fireball_speed = FIREBALL_SPEED
        self.triple_shot_timer = 0

        # Player explosion system (3x3 spritesheet)
        self.explosion_sheet = pygame.image.load(os.path.join(IMAGES_PATH, 'explosions.png')).convert_alpha()
        self.explosion_frames = []
        frame_w = self.explosion_sheet.get_width() // 3
        frame_h = self.explosion_sheet.get_height() // 3
        
        for row in range(3):
            for col in range(3):
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(self.explosion_sheet, (0, 0), (col * frame_w, row * frame_h, frame_w, frame_h))
                # Scale to 128x128 for a bigger impact
                self.explosion_frames.append(pygame.transform.scale(frame, (128, 128)))
                
        self.explosion_visible = False
        self.explosion_timer = 0
        self.explosion_duration = 27 # 9 frames * 3 ticks per frame

        # Invincibility after being hit
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = INVINCIBLE_DURATION

        # Overshield system
        self.overshield = 0 # 0 or 1

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

        self.y += self.y_change
        if self.y <= 5:
            self.y = 5
        if self.y >= 550:
            self.y = 550

        # Triple shot timer
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= 1

        # Fireballs movement
        for fb in self.fireballs[:]:
            fb['x'] += fb['x_ch']
            fb['y'] += fb['y_ch']
            if fb['y'] < -100 or fb['x'] < -20 or fb['x'] > SCREEN_WIDTH + 20:
                self.fireballs.remove(fb)

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
        # Pick sprite based on horizontal movement
        sprite = self.img_idle
        if self.x_change < 0:
            sprite = self.img_left
        elif self.x_change > 0:
            sprite = self.img_right

        # Flash every 6 frames when invincible
        if not (self.invincible and (self.invincible_timer // 6) % 2 == 0):
            screen.blit(sprite, (self.x, self.y))

        # Draw fireballs
        for fb in self.fireballs:
            screen.blit(fb['img'], (fb['x'] + 16, fb['y'] + 10))

        # Draw player explosion animation
        if self.explosion_visible:
            frame_idx = min(len(self.explosion_frames)-1, self.explosion_timer // 3)
            screen.blit(self.explosion_frames[frame_idx], (self.x - 32, self.y - 32))

        # Draw Overshield Bar
        if self.overshield > 0:
            # Yellow bar above ship, width based on strength (2 max)
            bar_w = 48
            current_w = bar_w * (self.overshield / 2)
            bar_rect = pygame.Rect(self.x + 8, self.y - 12, bar_w, 6)
            pygame.draw.rect(screen, (50, 50, 50), bar_rect) # Background
            pygame.draw.rect(screen, (255, 255, 0), (self.x + 8, self.y - 12, current_w, 6)) # Shield Color
            # Border
            pygame.draw.rect(screen, (200, 200, 0), bar_rect, 1)

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
        """Fire fireballs based on current powerups"""
        # Still enforce a single 'volley' at a time to prevent spam
        if len(self.fireballs) == 0:
            if self.triple_shot_timer > 0:
                # Spawn 3 blue fireballs
                img = self.blue_fireball_img
                self.fireballs.append({'x': self.x, 'y': self.y, 'x_ch': 0, 'y_ch': -self.fireball_speed, 'img': img})
                self.fireballs.append({'x': self.x, 'y': self.y, 'x_ch': -2, 'y_ch': -self.fireball_speed, 'img': img})
                self.fireballs.append({'x': self.x, 'y': self.y, 'x_ch': 2, 'y_ch': -self.fireball_speed, 'img': img})
                sound_manager.play('fire')
            else:
                # Single regular fireball
                img = self.fireball_img
                self.fireballs.append({'x': self.x, 'y': self.y, 'x_ch': 0, 'y_ch': -self.fireball_speed, 'img': img})
                sound_manager.play('fire')

    def activate_triple_shot(self):
        """Enable triple shot for 20 seconds (1200 frames at 60fps)"""
        self.triple_shot_timer = 1200

    def hit(self, sound_manager):
        """Handle the player being hit — check overshield first, else start explosion/lose life.
        Returns True if a life was actually lost, False if the shield absorbed the hit."""
        if self.overshield > 0:
            self.overshield -= 1
            self.invincible = True
            self.invincible_timer = 0
            sound_manager.play('bonus')
            return False

        self.explosion_visible = True
        self.explosion_timer = 0
        self.invincible = True
        self.invincible_timer = 0
        self.lives -= 1
        sound_manager.play('player_explosion')
        sound_manager.play('lose_life')
        return True

    def reset(self):
        """Full reset for game restart"""
        self.x = 368
        self.y = 520
        self.x_change = 0
        self.lives = 3
        self.fireballs = []
        self.triple_shot_timer = 0
        self.explosion_visible = False
        self.invincible = False
        self.overshield = 0