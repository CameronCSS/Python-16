"""
Boss class — a massive enemy that appears at 50k milestones
"""
import os
import random
import pygame
from settings import *

class Boss:
    def __init__(self, is_mega=False):
        self.is_mega = is_mega
        if is_mega:
            img_name = random.choice(['megaboss1.png', 'megaboss2.png'])
        else:
            img_name = random.choice(['boss1.png', 'boss2.png'])
            
        self.img = pygame.image.load(os.path.join(IMAGES_PATH, img_name))
        if is_mega:
            self.laser_frames = [
                pygame.image.load(os.path.join(IMAGES_PATH, 'megabosslaser1.png')),
                pygame.image.load(os.path.join(IMAGES_PATH, 'megabosslaser2.png'))
            ]
            self.laser_img = self.laser_frames[0]
        else:
            self.laser_img = pygame.image.load(os.path.join(IMAGES_PATH, 'bosslaser.png'))
        
        # Start at the top center
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2)
        self.y = -self.height # Start off-screen
        
        self.x_change = 2 if is_mega else 3 # Mega is slightly slower/heavier
        self.y_change = 0.3 if is_mega else 0.5 
        self.max_hp = 60 if is_mega else 20
        self.hp = self.max_hp
        
        # Dual lasers
        self.fire_mult = 0.6 if is_mega else 0.4 # Mega shoots slower now

        # Boss explosion system (3x3 spritesheet)
        ex_name = 'boss_explosions2.png' if is_mega else 'boss_explosions.png'
        self.explosion_sheet = pygame.image.load(os.path.join(IMAGES_PATH, ex_name)).convert_alpha()
        self.explosion_frames = []
        frame_w = self.explosion_sheet.get_width() // 3
        frame_h = self.explosion_sheet.get_height() // 3
        
        for row in range(3):
            for col in range(3):
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(self.explosion_sheet, (0, 0), (col * frame_w, row * frame_h, frame_w, frame_h))
                # Scale to 256x256 for a massive boss explosion
                self.explosion_frames.append(pygame.transform.scale(frame, (256, 256)))
                
        self.is_exploding = False
        self.explosion_timer = 0
        self.explosion_duration = 45 # 9 frames * 5 ticks per frame
        self.move_timer = 0
        self.fired_bombs = set() # Track already-triggered health milestones

    def update(self):
        """Boss movement pattern or explosion update"""
        if self.is_exploding:
            self.explosion_timer += 1
            return self.explosion_timer >= self.explosion_duration

        self.y += self.y_change
        self.x += self.x_change
        
        # Initial descent
        if not getattr(self, 'reached_altitude', False):
            if self.y > 100:
                self.y = 100
                self.reached_altitude = True
                self.y_change = 0 # Stop initial drop
        else:
            # Sporadic movement for both Regular & Mega Boss
            self.move_timer += 1
            if self.move_timer >= 40: # Evaluate roughly every 0.66 seconds
                self.move_timer = 0
                if random.random() < 0.7: # 70% chance to shift movement
                    new_speed = random.uniform(2.5, 4.8) # Sporadic lateral speed bounds
                    self.x_change = new_speed if random.random() < 0.5 else -new_speed
                    self.y_change = random.uniform(-1.8, 1.8) # Sporadic vertical speed bounds
            
            # Vertical boundaries for both Regular & Mega Boss
            if self.y < 30:
                self.y = 30
                self.y_change = abs(self.y_change)
            elif self.y > 250:
                self.y = 250
                self.y_change = -abs(self.y_change)

        # Bounce off walls
        if self.x <= 10:
            self.x = 10
            self.x_change = abs(self.x_change)
        elif self.x >= SCREEN_WIDTH - self.width - 10:
            self.x = SCREEN_WIDTH - self.width - 10
            self.x_change = -abs(self.x_change)
        return False

    def draw(self, screen):
        """Draw the boss or its explosion"""
        if self.is_exploding:
            frame_idx = min(len(self.explosion_frames)-1, self.explosion_timer // 5)
            # Center the massive explosion
            ex_x = self.x + self.width // 2 - 128
            ex_y = self.y + self.height // 2 - 128
            screen.blit(self.explosion_frames[frame_idx], (ex_x, ex_y))
            return

        screen.blit(self.img, (self.x, self.y))
        
        # Simple health bar
        if self.hp > 0:
            bar_width = self.width
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, bar_width, 10))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, bar_width * (self.hp / self.max_hp), 10))

    def hit(self):
        """Take damage
        Returns a tuple: (is_dead, should_spawn_bomb)
        """
        if self.is_exploding:
            return False, False
        self.hp -= 1
        
        # Check health milestones for seeking bomb release
        should_spawn_bomb = False
        if self.is_mega:
            if self.hp <= 45 and 45 not in self.fired_bombs:
                self.fired_bombs.add(45)
                should_spawn_bomb = True
            elif self.hp <= 15 and 15 not in self.fired_bombs:
                self.fired_bombs.add(15)
                should_spawn_bomb = True
        else:
            if self.hp <= 10 and 10 not in self.fired_bombs:
                self.fired_bombs.add(10)
                should_spawn_bomb = True
                
        if self.hp <= 0:
            self.is_exploding = True
            return True, should_spawn_bomb
        return False, should_spawn_bomb
