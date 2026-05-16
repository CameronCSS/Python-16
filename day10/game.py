"""
Game class — orchestrates the game loop, collision detection, UI, and all entities
"""
import math
import os
import random
import pygame
from enemy import Enemy
from player import Player
from settings import *
from sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        # Icon
        icon = pygame.image.load(os.path.join(IMAGES_PATH, ICON_IMG))
        pygame.display.set_icon(icon)

        # Background
        self.background = pygame.image.load(os.path.join(IMAGES_PATH, BG_IMG))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_SM)
        self.score = 0
        self.game_over = False

        # Entities
        self.sound_manager = SoundManager()
        self.player = Player()
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]

        # Laser (shared enemy weapon)
        self.active_laser_img = None
        self.laser_x = 0
        self.laser_y = 0
        self.laser_y_change = LASER_SPEED
        self.laser_visible = False
        self.laser_timer = 0
        self.laser_interval = LASER_INTERVAL_MAX

        # Start music
        self.sound_manager.play_music()

    @staticmethod
    def _detect_collision(x1, y1, x2, y2):
        """Detects collision between two objects using distance formula"""
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return distance < 27

    def run(self):
        """
        Main game loop
        """
        is_running = True
        while is_running:
            # Background
            self.screen.blit(self.background, (0, 0))

            # Game over state
            if self.game_over:
                self._draw_game_over()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            is_running = False
                        if event.key == pygame.K_r:
                            self._restart()
                pygame.display.update()
                self.clock.tick(60)
                continue

            # UI
            self.player.draw_lives(self.screen)
            self._draw_score()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.sound_manager)
                    if event.key == pygame.K_LEFT:
                        self.player.x_change = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT:
                        self.player.x_change = PLAYER_SPEED
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.x_change = 0

            # Update and draw player
            self.player.update()
            self.player.draw(self.screen)

            # Update and draw enemies + check collisions
            for enemy in self.enemies:
                enemy.update()

                # Fireball hits enemy
                if self.player.fireball_visible:
                    if self._detect_collision(self.player.fireball_x, self.player.fireball_y,
                                        enemy.x, enemy.y):
                        self.player.fireball_visible = False
                        self.player.fireball_y = self.player.y
                        self.score += 100
                        self.sound_manager.play('success')
                        enemy.explode(self.sound_manager)
                        enemy.respawn()

                # Enemy hits player
                if not self.player.invincible:
                    if self._detect_collision(self.player.x, self.player.y,
                                        enemy.x, enemy.y):
                        self.player.hit(self.sound_manager)
                        enemy.respawn()

                enemy.draw(self.screen)

            # Laser logic
            self._update_laser()

            # Player hit by laser
            if self.laser_visible and not self.player.invincible:
                if self._detect_collision(self.player.x, self.player.y,
                                    self.laser_x, self.laser_y):
                    self.laser_visible = False
                    self.player.hit(self.sound_manager)

            # Check game over (after player explosion finishes)
            if self.player.lives <= 0 and not self.player.explosion_visible \
                    and not self.game_over:
                self.game_over = True
                self.sound_manager.stop_music()
                self.sound_manager.play('game_over')

            # Update screen
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    # ---- Private helpers ----

    def _update_laser(self):
        """Handle enemy laser firing and movement"""
        if not self.laser_visible:
            self.laser_timer += 1
            if self.laser_timer >= self.laser_interval:
                shooter = random.choice(self.enemies)
                self.laser_x = shooter.x + shooter.img.get_width() // 2 - 5
                self.laser_y = shooter.y + shooter.img.get_height()
                self.active_laser_img = shooter.laser_img
                self.laser_visible = True
                self.sound_manager.play('enemy_shot')
                self.laser_timer = 0
                self.laser_interval = random.randint(LASER_INTERVAL_MIN, LASER_INTERVAL_MAX) * shooter.fire_mult

        if self.laser_visible:
            self.screen.blit(self.active_laser_img, (self.laser_x, self.laser_y + 20))
            self.laser_y += self.laser_y_change
            if self.laser_y > SCREEN_HEIGHT:
                self.laser_visible = False

    def _draw_score(self):
        """Draw the score in the top-right"""
        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (600, 10))

    def _draw_game_over(self):
        """Draw the game over overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        go_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        sub_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)

        go_text = go_font.render("GAME OVER", True, (255, 0, 0))
        score_text = sub_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = sub_font.render("R - Restart    ESC - Quit", True, (255, 255, 255))

        self.screen.blit(go_text, (400 - go_text.get_width() // 2, 200))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 300))
        self.screen.blit(restart_text, (400 - restart_text.get_width() // 2, 370))

    def _restart(self):
        """Reset all game state for a new round"""
        self.score = 0
        self.game_over = False
        self.player.reset()
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.laser_visible = False
        self.laser_timer = 0
        self.laser_interval = LASER_INTERVAL_MAX
        self.sound_manager.play_music()