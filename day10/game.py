"""
Game class — orchestrates the game loop, collision detection, UI, and all entities
"""
import math
import os
import random
import pygame
from enemy import Enemy
from boss import Boss
from player import Player
from settings import *
from sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Aliens Attack!")

        # Icon
        icon = pygame.image.load(os.path.join(IMAGES_PATH, ICON_IMG))
        pygame.display.set_icon(icon)

        # Background
        self.background = pygame.image.load(os.path.join(IMAGES_PATH, BG_IMG))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_SM)
        self.score = 0
        self.game_over = False
        self.started = False
        self.paused = False
        self.slow_motion_timer = 0
        self.showing_rules = False
        self.floating_texts = [] # List of {'text': str, 'x': int, 'y': int, 'color': tuple, 'timer': int, 'y_speed': int, 'font_size': int}
        self.next_life_score = 5000
        self.next_ts_score = 10000
        self.next_boss_score = 10000
        self.next_mega_score = 50000

        # Entities
        self.sound_manager = SoundManager()
        self.player = Player()
        self.enemies = [Enemy(self.score) for _ in range(NUM_ENEMIES)]

        # Laser (shared enemy weapon)
        self.active_laser_img = None
        self.laser_x = 0
        self.laser_y = 0
        self.laser_y_change = LASER_SPEED
        self.laser_visible = False
        self.laser_timer = 0
        self.laser_interval = LASER_INTERVAL_MAX
        self.boss = None
        self.active_boss_lasers = []
        self.stats = self._init_stats()

        # Start music
        self.sound_manager.play_music()

    def _init_stats(self):
        """Initialize game statistics"""
        return {
            'enemies_killed': [0, 0, 0], # [Normal, Elite, Ace]
            'bosses_defeated': 0,
            'mega_bosses_defeated': 0,
            'lives_earned': 0,
            'lives_lost': 0,
            'triple_shot_frames': 0,
            'boss_hits': 0,
            'shots_fired': 0,
            'shots_hit': 0,
            'enemies_escaped': 0
        }

    @staticmethod
    def _detect_collision(x1, y1, x2, y2, radius=27):
        """Detects collision between two objects using distance formula"""
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        return distance < radius

    def run(self):
        """
        Main game loop
        """
        is_running = True
        while is_running:
            # Background
            self.screen.blit(self.background, (0, 0))

            # Rules page state
            if self.showing_rules:
                self._draw_rules_page()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_h:
                            self.showing_rules = False
                pygame.display.update()
                self.clock.tick(60)
                continue

            # Start menu state
            if not self.started:
                self._draw_start_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            is_running = False
                        elif event.key == pygame.K_h:
                            self.showing_rules = True
                        else:
                            self.started = True
                pygame.display.update()
                self.clock.tick(60)
                continue

            # Pause state
            if self.paused:
                self._draw_pause_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.paused = False
                        if event.key == pygame.K_ESCAPE:
                            is_running = False
                pygame.display.update()
                self.clock.tick(60)
                continue

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
                    if event.key == pygame.K_p:
                        self.paused = True
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.sound_manager)
                        # Track shots fired (1 or 3)
                        self.stats['shots_fired'] += 3 if self.player.triple_shot_timer > 0 else 1
                    if event.key == pygame.K_LEFT:
                        self.player.x_change = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT:
                        self.player.x_change = PLAYER_SPEED
                    if event.key == pygame.K_UP:
                        self.player.y_change = -PLAYER_SPEED
                    if event.key == pygame.K_DOWN:
                        self.player.y_change = PLAYER_SPEED
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.x_change = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.y_change = 0

            # Update and draw player
            self.player.update()
            self.player.draw(self.screen)
            
            # Stats: Triple Shot Time
            if self.player.triple_shot_timer > 0:
                self.stats['triple_shot_frames'] += 1

            # Floating text display (+score, -penalty)
            for ft in self.floating_texts[:]:
                ft_font = pygame.font.Font(FONT_PATH, ft['font_size'])
                ft_surf = ft_font.render(ft['text'], True, ft['color'])
                
                # Handle auto-centering
                draw_x = ft['x']
                if draw_x == -1:
                    draw_x = (SCREEN_WIDTH - ft_surf.get_width()) // 2
                    
                self.screen.blit(ft_surf, (draw_x, ft['y']))
                ft['y'] += ft['y_speed']
                ft['timer'] -= 1
                if ft['timer'] <= 0:
                    self.floating_texts.remove(ft)

            # Update and draw enemies + check collisions
            for enemy in self.enemies:
                enemy.update(self.score)

                # Fireballs hits enemy
                for fb in self.player.fireballs[:]:
                    if self._detect_collision(fb['x'], fb['y'], enemy.x, enemy.y):
                        if fb in self.player.fireballs:
                            self.player.fireballs.remove(fb)
                        self.stats['shots_hit'] += 1
                        
                        old_score = self.score
                        self.score += enemy.points
                        
                        # Centralized Milestone Check
                        self._check_score_milestones(old_score)
                        
                        self._add_floating_text(f"+{enemy.points}", enemy.x, enemy.y, (0, 255, 0))
                        self.sound_manager.play('success')
                        
                        # Stats: Kills per type
                        if enemy.points == 100:
                            self.stats['enemies_killed'][0] += 1
                        elif enemy.points == 200:
                            self.stats['enemies_killed'][1] += 1
                        elif enemy.points == 300:
                            self.stats['enemies_killed'][2] += 1
                        
                        enemy.explode(self.sound_manager)
                        # enemy.respawn() <-- Removed: update() handles this after explosion

                # Enemy hits player
                if not self.player.invincible:
                    if self._detect_collision(self.player.x, self.player.y,
                                        enemy.x, enemy.y):
                        if self.player.hit(self.sound_manager):
                            self.stats['lives_lost'] += 1
                            self._add_floating_text("-1 LIFE", 350, 400, (255, 0, 0), 
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                        enemy.explode(self.sound_manager)

                # Enemy escapes (reaches bottom)
                if enemy.y > 560:
                    self.score = max(0, self.score - 1000)
                    self.sound_manager.play('fail')
                    self._add_floating_text("-1000", enemy.x, 540, (255, 0, 0))
                    self.stats['enemies_escaped'] += 1
                    enemy.respawn(self.score)

                enemy.draw(self.screen)

            # Boss Logic
            if self.boss:
                if self.boss.update():
                    self.boss = None
                    self.enemies = [Enemy(self.score) for _ in range(min(50, NUM_ENEMIES + (self.score // 25000) * 2))]
                else:
                    self.boss.draw(self.screen)
                
                # Check fireball hits boss
                if self.boss:
                    for fb in self.player.fireballs[:]:
                        if self._detect_collision(fb['x'], fb['y'], self.boss.x + self.boss.width//2, self.boss.y + self.boss.height//2, radius=60):
                            if fb in self.player.fireballs:
                                self.player.fireballs.remove(fb)
                            
                            self.stats['shots_hit'] += 1
                            self.sound_manager.play('boss_hit')
                            old_score = self.score
                            self.score += 100 # +100 per hit
                            self.stats['boss_hits'] += 1
                            self._check_score_milestones(old_score)
                            self._add_floating_text("+100", fb['x'], fb['y'], (0, 255, 0))
                            
                            if self.boss.hit():
                                # Boss Killed!
                                kill_score = 25000 if self.boss.is_mega else 10000
                                kill_text = "MEGA BOSS KILL!" if self.boss.is_mega else "BOSS KILL!"
                                
                                # Cinematic Mega Boss Death
                                if self.boss.is_mega:
                                    self.sound_manager.stop_all_sfx()
                                    self.sound_manager.play('explosion2')
                                    self.slow_motion_timer = 40 # 2 seconds at 20 FPS
                                
                                old_score = self.score
                                self.score += kill_score
                                self._check_score_milestones(old_score)
                                
                                self.player.activate_triple_shot()
                                self.player.triple_shot_timer = 1800 # 30 seconds
                                self.sound_manager.play('powerup')
                                
                                # Reward: Invincibility (2 seconds = 120 frames)
                                self.player.invincible = True
                                self.player.invincible_timer = -60 # Starts negative so it has 120 frames before hitting 60
                                
                                self._add_floating_text(kill_text, -1, 250, (0, 255, 0), 
                                                        duration=180, y_speed=-1, font_size=FONT_SIZE_MD)
                                self._add_floating_text(f"+{kill_score:,}", -1, 320, (255, 255, 0), 
                                                        duration=180, y_speed=-1, font_size=FONT_SIZE_MD)
                                self.sound_manager.play('boss_kill')
                                self.sound_manager.stop_danger() # Stop danger sound
                                
                                # Stats: Boss Defeats
                                if self.boss.is_mega:
                                    self.stats['mega_bosses_defeated'] += 1
                                else:
                                    self.stats['bosses_defeated'] += 1
                                    
                                # self.boss = None  <-- Removed: will be handled by update()
                                # self.enemies = ... <-- Removed: will be handled by update()
                                break
                
                # Boss hits player directly
                if self.boss and not self.player.invincible:
                    if self._detect_collision(self.player.x, self.player.y, 
                                            self.boss.x + self.boss.width//2, self.boss.y + self.boss.height//2, radius=60):
                        if self.player.hit(self.sound_manager):
                            self.stats['lives_lost'] += 1
                            self._add_floating_text("-1 LIFE", 350, 400, (255, 0, 0), 
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)

            # Laser logic
            self._update_laser()

            # Player hit by laser
            if self.laser_visible and not self.player.invincible:
                if self._detect_collision(self.player.x, self.player.y,
                                    self.laser_x, self.laser_y):
                    self.laser_visible = False
                    if self.player.hit(self.sound_manager):
                        self.stats['lives_lost'] += 1
                        self._add_floating_text("-1 LIFE", 350, 400, (255, 0, 0), 
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)

            # Check game over (after player explosion finishes)
            if self.player.lives <= 0 and not self.player.explosion_visible \
                    and not self.game_over:
                self.game_over = True
                self.sound_manager.stop_music()
                self.sound_manager.stop_danger()
                self.sound_manager.play('game_over')

            # Update screen
            pygame.display.update()
            
            # Slow motion logic for Mega Boss death
            fps = 60
            if self.slow_motion_timer > 0:
                self.slow_motion_timer -= 1
                fps = 20 # 3x slower
            
            self.clock.tick(fps)

        pygame.quit()

    # ---- Private helpers ----

    def _check_score_milestones(self, old_score):
        """Check and apply score-based milestones and rewards"""
        # Difficulty Increase every 25k (Reinforcements)
        if (old_score // 25000) < (self.score // 25000):
            if len(self.enemies) < 50:
                self.enemies.extend([Enemy(self.score) for _ in range(2)])
                self._add_floating_text("REINFORCEMENTS!", -1, 100, (255, 0, 0), 
                                        duration=150, y_speed=-0.5, font_size=FONT_SIZE_MD)
                self.sound_manager.play('bonus')
            else:
                self._add_floating_text("ELITE SQUADRON INBOUND!", -1, 100, (255, 0, 255), 
                                        duration=150, y_speed=-0.5, font_size=FONT_SIZE_MD)
                self.sound_manager.play('bonus')

        # Overshield every 100k
        if (old_score // 100000) < (self.score // 100000):
            self.player.overshield = 2
            self._add_floating_text("OVERSHIELD!", -1, 350, (0, 255, 255), 
                                    duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
            self.sound_manager.play('powerup')

        # Exponential Life Gain
        while self.score >= self.next_life_score:
            if self.player.lives < 3:
                self.player.lives += 1
                self.stats['lives_earned'] += 1
                self.sound_manager.play('bonus')
                self._add_floating_text("+1 LIFE", -1, 400, (0, 255, 0), 
                                        duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
            else:
                self.player.activate_triple_shot()
                self._add_floating_text("TRIPLE SHOT!", -1, 350, (0, 255, 255), 
                                        duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
                self.sound_manager.play('powerup')
            
            self.next_life_score *= 2

        # Exponential Triple Shot Gain
        while self.score >= self.next_ts_score:
            self.player.activate_triple_shot()
            self._add_floating_text("TRIPLE SHOT!", -1, 350, (0, 255, 255), 
                                    duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
            self.sound_manager.play('powerup')
            self.next_ts_score *= 2

        # Dynamic Boss Spawns
        spawned_boss = False
        while self.score >= self.next_mega_score:
            if self.score >= 500000:
                self.next_mega_score += 200000
            elif self.score >= 250000:
                self.next_mega_score += 100000
            else:
                self.next_mega_score += 50000
                
            if not self.boss and not spawned_boss:
                self.enemies = []
                self.boss = Boss(is_mega=True)
                self._add_floating_text("MEGA BOSS INCOMING!", -1, 300, (255, 0, 255), 
                                        duration=200, y_speed=-0.2, font_size=FONT_SIZE_MD)
                self.sound_manager.play_danger()
                spawned_boss = True

        while self.score >= self.next_boss_score:
            if self.score >= 500000:
                self.next_boss_score += 40000
            elif self.score >= 250000:
                self.next_boss_score += 20000
            else:
                self.next_boss_score += 10000
                
            if not self.boss and not spawned_boss:
                self.enemies = []
                self.boss = Boss(is_mega=False)
                self._add_floating_text("BOSS INCOMING!", -1, 300, (255, 0, 0), 
                                        duration=180, y_speed=-0.2, font_size=FONT_SIZE_MD)
                self.sound_manager.play_danger()
                spawned_boss = True

    def _update_laser(self):
        """Handle enemy and boss laser firing and movement"""
        # Regular enemy laser
        if not self.laser_visible and len(self.enemies) > 0 and not self.boss:
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

        # Boss dual lasers
        if self.boss and not self.boss.is_exploding:
            self.laser_timer += 1
            if self.laser_timer >= (self.laser_interval * self.boss.fire_mult):
                # Spawn two lasers from ends (10px in)
                l1_x = self.boss.x + 10
                l2_x = self.boss.x + self.boss.width - 20
                ly = self.boss.y + self.boss.height - 10
                
                self.active_boss_lasers.append({'x': l1_x, 'y': ly, 'img': self.boss.laser_img})
                self.active_boss_lasers.append({'x': l2_x, 'y': ly, 'img': self.boss.laser_img})
                
                self.sound_manager.play('enemy_shot')
                self.laser_timer = 0
                self.laser_interval = random.randint(LASER_INTERVAL_MIN, LASER_INTERVAL_MAX)

        # Update and draw boss lasers
        for bl in self.active_boss_lasers[:]:
            self.screen.blit(bl['img'], (bl['x'], bl['y']))
            bl['y'] += self.laser_y_change
            
            # Check collision with player
            if not self.player.invincible:
                if self._detect_collision(self.player.x, self.player.y, bl['x'], bl['y']):
                    if self.player.hit(self.sound_manager):
                        self.stats['lives_lost'] += 1
                        self._add_floating_text("-1 LIFE", 350, 400, (255, 0, 0), 
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                    if bl in self.active_boss_lasers:
                        self.active_boss_lasers.remove(bl)
                    continue

            if bl['y'] > SCREEN_HEIGHT:
                if bl in self.active_boss_lasers:
                    self.active_boss_lasers.remove(bl)

    def _draw_score(self):
        """Draw the score in the top-right"""
        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (600, 10))

    def _draw_game_over(self):
        """Draw the game over overlay with detailed stats"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210)) # Slightly darker for readability
        self.screen.blit(overlay, (0, 0))

        go_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        sub_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)
        stat_font = pygame.font.SysFont('Arial', 18, bold=True)

        # Title
        go_text = go_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(go_text, (400 - go_text.get_width() // 2, 60))
        
        score_text = sub_font.render(f"Final Score: {self.score:,}", True, (255, 255, 0))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 140))

        # Stats Section
        y_off = 220
        # Enemy Kills & Escaped
        kills = self.stats['enemies_killed']
        escaped = self.stats['enemies_escaped']
        
        # Render Kills (White)
        kill_str = f"KILLS: Normal [{kills[0]}]  Elite [{kills[1]}]  Ace [{kills[2]}]"
        k_surf = stat_font.render(kill_str, True, (255, 255, 255))
        
        # Render Divider (Gray)
        div_surf = stat_font.render("  |  ", True, (150, 150, 150))
        
        # Render Escaped (Conditional Color: Green if 0, Red if > 0)
        esc_color = (0, 255, 0) if escaped == 0 else (255, 50, 50)
        esc_label = stat_font.render("ESCAPED: ", True, (255, 255, 255))
        esc_val = stat_font.render(str(escaped), True, esc_color)
        
        # Calculate total width to center
        total_w = k_surf.get_width() + div_surf.get_width() + esc_label.get_width() + esc_val.get_width()
        start_x = 400 - total_w // 2
        
        self.screen.blit(k_surf, (start_x, y_off))
        curr_x = start_x + k_surf.get_width()
        self.screen.blit(div_surf, (curr_x, y_off))
        curr_x += div_surf.get_width()
        self.screen.blit(esc_label, (curr_x, y_off))
        curr_x += esc_label.get_width()
        self.screen.blit(esc_val, (curr_x, y_off))
        
        # Bosses
        boss_str = f"BOSSES: Regular [{self.stats['bosses_defeated']}]  Mega [{self.stats['mega_bosses_defeated']}]"
        b_surf = stat_font.render(boss_str, True, (100, 150, 255))
        self.screen.blit(b_surf, (400 - b_surf.get_width() // 2, y_off + 35))
        
        # Triple Shot Time
        ts_secs = self.stats['triple_shot_frames'] // 60
        ts_str = f"TRIPLE SHOT TOTAL TIME: {ts_secs}s"
        e_surf = stat_font.render(ts_str, True, (0, 255, 255))
        self.screen.blit(e_surf, (400 - e_surf.get_width() // 2, y_off + 70))
        
        # Lives
        life_str = f"LIVES: Earned [{self.stats['lives_earned']}]  Lost [{self.stats['lives_lost']}]"
        l_surf = stat_font.render(life_str, True, (0, 255, 0))
        self.screen.blit(l_surf, (400 - l_surf.get_width() // 2, y_off + 105))

        # Accuracy
        fired = self.stats['shots_fired']
        hit = self.stats['shots_hit']
        acc = (hit / fired * 100) if fired > 0 else 0
        acc_str = f"ACCURACY: {acc:.1f}%  (Fired: {fired} | Hits: {hit})"
        a_surf = stat_font.render(acc_str, True, (255, 165, 0)) # Orange
        self.screen.blit(a_surf, (400 - a_surf.get_width() // 2, y_off + 140))

        # Footer
        restart_text = sub_font.render("R - Restart    ESC - Quit", True, (255, 255, 255))
        self.screen.blit(restart_text, (400 - restart_text.get_width() // 2, 500))

    def _draw_start_menu(self):
        """Draw the start menu with game description"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        desc_font = pygame.font.Font(FONT_PATH, 20)
        prompt_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)

        title_text = title_font.render("ALIENS ATTACK!", True, (192, 25, 51))
        desc1 = desc_font.render("Defend Earth from the alien invasion!", True, (255, 255, 255))
        controls = desc_font.render("ARROWS to Move  |  SPACE to Shoot  |  P to Pause", True, (200, 200, 200))
        rules_prompt = desc_font.render("Press H for Rules & Scoring", True, (0, 255, 255))
        prompt_text = prompt_font.render("Press ANY OTHER KEY to Start", True, (255, 255, 0))

        self.screen.blit(title_text, (400 - title_text.get_width() // 2, 120))
        self.screen.blit(desc1, (400 - desc1.get_width() // 2, 240))
        self.screen.blit(controls, (400 - controls.get_width() // 2, 330))
        self.screen.blit(rules_prompt, (400 - rules_prompt.get_width() // 2, 380))
        self.screen.blit(prompt_text, (400 - prompt_text.get_width() // 2, 460))

    def _draw_rules_page(self):
        """Draw the detailed rules and scoring page"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)
        body_font = pygame.font.SysFont('Arial', 18, bold=True)
        header_color = (0, 255, 255)
        text_color = (255, 255, 255)

        title = title_font.render("MISSION RULES", True, header_color)
        self.screen.blit(title, (400 - title.get_width() // 2, 50))
        
        # --- Column 1: SCORING (Left) ---
        s_head = title_font.render("SCORING", True, (0, 255, 0))
        self.screen.blit(s_head, (30, 150))
        
        scores = [
            ("Standard Ship: ", "100 pts"),
            ("Elite Ship (Blue): ", "200 pts"),
            ("Ace Ship (Red): ", "300 pts"),
            ("Bonus Life: ", "Exponential (5k, 10k, 20k...)")
        ]
        for i, (label, value) in enumerate(scores):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, (0, 255, 0))
            self.screen.blit(label_surf, (30, 210 + i * 35))
            self.screen.blit(value_surf, (30 + label_surf.get_width(), 210 + i * 35))

        # --- Column 2: THREATS (Center) ---
        p_head = title_font.render("THREATS", True, (255, 0, 0))
        self.screen.blit(p_head, (400 - p_head.get_width() // 2, 150))
        
        penalties = [
            ("Enemy Escapes: ", "-1000 pts"),
            ("Enemy Laser: ", "-1 Life"),
            ("Max Lives: ", "3"),
            ("Game Over: ", "0 Lives Remaining")
        ]
        for i, (label, value) in enumerate(penalties):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, (255, 0, 0))
            x_pos = 400 - (label_surf.get_width() + value_surf.get_width()) // 2
            self.screen.blit(label_surf, (x_pos, 210 + i * 35))
            self.screen.blit(value_surf, (x_pos + label_surf.get_width(), 210 + i * 35))

        # --- Column 3: BOSSES (Right) ---
        b_head = title_font.render("BOSSES", True, (255, 255, 0))
        self.screen.blit(b_head, (SCREEN_WIDTH - b_head.get_width() - 30, 150))
        
        boss_intel = [
            ("Regular Boss: ", "10k (Doubles at 250k, 500k)"),
            ("Mega Boss: ", "50k (Doubles at 250k, 500k)"),
            ("Reward: ", "Reg-10k / Mega-25k"),
            ("Bonus: ", "None")
        ]
        for i, (label, value) in enumerate(boss_intel):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, (255, 255, 0))
            x_pos = SCREEN_WIDTH - (label_surf.get_width() + value_surf.get_width()) - 30
            self.screen.blit(label_surf, (x_pos, 210 + i * 35))
            self.screen.blit(value_surf, (x_pos + label_surf.get_width(), 210 + i * 35))

        # --- Footer: BONUS UPGRADES ---
        up_head = title_font.render("BONUS UPGRADES", True, (100, 150, 255))
        self.screen.blit(up_head, (400 - up_head.get_width() // 2, 400))
        
        bonuses = [
            ("Triple Shot (TS): ", "Exponential (10k, 20k...)"),
            ("OVERSHIELD: ", "Absorb 2 Hits (Every 100k pts)")
        ]
        for i, (label, value) in enumerate(bonuses):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, (100, 150, 255))
            x_pos = 400 - (label_surf.get_width() + value_surf.get_width()) // 2
            self.screen.blit(label_surf, (x_pos, 450 + i * 30))
            self.screen.blit(value_surf, (x_pos + label_surf.get_width(), 450 + i * 30))

        prompt = body_font.render("Press H or ESC to go back", True, (200, 200, 200))
        self.screen.blit(prompt, (400 - prompt.get_width() // 2, 550))

    def _draw_pause_menu(self):
        """Draw the pause menu overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        pause_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        prompt_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)

        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        prompt_text = prompt_font.render("Press P to Resume", True, (255, 255, 255))

        self.screen.blit(pause_text, (400 - pause_text.get_width() // 2, 250))
        self.screen.blit(prompt_text, (400 - prompt_text.get_width() // 2, 340))

    def _restart(self):
        """Reset all game state for a new round"""
        self.score = 0
        self.game_over = False
        self.player.reset()
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.laser_visible = False
        self.laser_timer = 0
        self.laser_interval = LASER_INTERVAL_MAX
        self.boss = None
        self.active_boss_lasers = []
        self.floating_texts = []
        self.last_life_bonus = 0
        self.stats = self._init_stats()
        self.sound_manager.play_music()

    def _add_floating_text(self, text, x, y, color, duration=45, y_speed=0, font_size=FONT_SIZE_XS):
        """Add a piece of floating text. Use x=-1 for auto-center."""
        # Only clamp if x is not the centering flag
        final_x = x
        if x != -1:
            final_x = max(10, min(x, SCREEN_WIDTH - 120))
            
        # Stagger vertical position if another text is already at this height
        final_y = y
        overlap_found = True
        attempts = 0
        while overlap_found and attempts < 5:
            overlap_found = False
            for ft in self.floating_texts:
                if (ft['x'] == final_x) and abs(ft['y'] - final_y) < 35:
                    final_y += 45 
                    overlap_found = True
                    break
            attempts += 1
            
        self.floating_texts.append({
            'text': text,
            'x': final_x,
            'y': final_y,
            'color': color,
            'timer': duration,
            'y_speed': y_speed,
            'font_size': font_size
        })