"""
Enemy class handles enemy ships, their movement, and explosions
"""
import os
import random
import pygame
from settings import *


class Enemy:
    def __init__(self, score=0):
        self.x = random.randint(10, 720)
        self.y = random.randint(50, 200)
        self.x_change = ENEMY_SPEED
        self.y_change = 50
        self._load_variant(score)

        # Explosion tracking (2x2 grid = 4 frames)
        self.explosion_visible = False
        self.explosion_timer = 0
        self.explosion_duration = 12 # 4 frames * 3 ticks per frame
        self.explosion_x = 0
        self.explosion_y = 0
        self.pending_respawn = False

    def update(self, score):
        """Update enemy position and explosion timer each frame"""
        # Explosion timer and respawn logic
        if self.explosion_visible:
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_duration:
                self.explosion_visible = False
                if self.pending_respawn:
                    self.respawn(score)
                    self.pending_respawn = False
            return # Don't move while exploding

        self.x += self.x_change
        
        # Sporadic movement for Elite (300 pt) enemy
        if getattr(self, 'points', 0) == 300:
            self.y += getattr(self, 'y_speed', 0)
            if random.random() < 0.02: # 2% chance per frame (approx once a second)
                direction = 1 if random.random() < 0.5 else -1
                # Normal speed is heavily maintained, just switching directions or slightly accelerating
                self.x_change = ENEMY_SPEED * self.speed_mult * direction * random.uniform(0.7, 1.2)
                self.y_speed = random.uniform(-0.5, 1.5) # Gentle evasive vertical drift
            
            # Keep elite enemies from flying off the top
            if self.y < 20:
                self.y = 20
                self.y_speed = abs(getattr(self, 'y_speed', 0))

        if self.x <= 5:
            self.x = 5
            self.x_change = abs(self.x_change)
            if getattr(self, 'points', 0) != 300:
                self.y += self.y_change
        if self.x >= 730:
            self.x = 730
            self.x_change = -abs(self.x_change)
            if getattr(self, 'points', 0) != 300:
                self.y += self.y_change

    def draw(self, screen):
        """Draw the enemy ship or its active explosion"""
        if self.explosion_visible:
            # 4 frames, 3 ticks each
            frame_idx = min(len(self.explosion_frames)-1, self.explosion_timer // 3)
            screen.blit(self.explosion_frames[frame_idx], (self.explosion_x, self.explosion_y))
        else:
            screen.blit(self.img, (self.x, self.y))

    def explode(self, sound_manager):
        """Trigger explosion at current position and flag for respawn"""
        self.explosion_visible = True
        self.explosion_timer = 0
        self.explosion_x = self.x - 32
        self.explosion_y = self.y - 32
        self.pending_respawn = True
        sound_manager.play('enemy_explosion')

    def respawn(self, score):
        """Move enemy to a new random position with a new random variant"""
        self._load_variant(score)
        self.x = random.randint(10, 720)
        self.y = random.randint(50, 200)

    def _load_variant(self, score):
        """Pick an enemy variant based on dynamic score weights and load its assets"""
        # Default weights
        weights = [v['spawn_weight'] for v in ENEMY_VARIANTS]
        
        # Adjust weights after ~550k (when we hit 50 enemies cap)
        if score >= 1000000:
            weights = [0, 0, 100]
        elif score > 550000:
            p = (score - 550000) / 450000.0
            if p < 0.5:
                p2 = p / 0.5
                w1 = 70 - int(70 * p2)
                w2 = 20 + int(30 * p2)
                w3 = 10 + int(40 * p2)
                weights = [w1, w2, w3]
            else:
                p2 = (p - 0.5) / 0.5
                w1 = 0
                w2 = 50 - int(50 * p2)
                w3 = 50 + int(50 * p2)
                weights = [w1, w2, w3]

        variant = random.choices(ENEMY_VARIANTS, weights=weights, k=1)[0]
        
        self.img = pygame.image.load(os.path.join(IMAGES_PATH, variant['ship']))
        self.laser_img = pygame.image.load(os.path.join(IMAGES_PATH, variant['laser']))
        
        # Load and slice explosion sheet (2x2)
        sheet = pygame.image.load(os.path.join(IMAGES_PATH, variant['explode'])).convert_alpha()
        self.explosion_frames = []
        fw = sheet.get_width() // 2
        fh = sheet.get_height() // 2
        for row in range(2):
            for col in range(2):
                frame = pygame.Surface((fw, fh), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (col * fw, row * fh, fw, fh))
                self.explosion_frames.append(pygame.transform.scale(frame, (128, 128)))
        
        # Difficulty stats
        self.speed_mult = variant['speed_mult']
        self.fire_mult = variant['fire_mult']
        self.points = variant['points']
        
        direction = 1 if self.x_change >= 0 else -1
        self.x_change = ENEMY_SPEED * self.speed_mult * direction