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
        
        # UI Images (Scaled)
        self.ui_images = {
            'enemy1': pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, ENEMY_VARIANTS[0]['ship'])).convert_alpha(), (40, 40)),
            'enemy2': pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, ENEMY_VARIANTS[1]['ship'])).convert_alpha(), (40, 40)),
            'enemy3': pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, ENEMY_VARIANTS[2]['ship'])).convert_alpha(), (40, 40)),
            'boss': pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'boss1.png')).convert_alpha(), (60, 60)),
            'mega_boss': pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'megaboss1.png')).convert_alpha(), (80, 80))
        }

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_SM)
        self.score = 0
        self.progression_score = 0
        self.combo_kills = 0
        self.game_over = False
        self.started = False
        self.paused = False
        self.showing_rules = False
        self.floating_texts = [] # List of {'text': str, 'x': int, 'y': int, 'color': tuple, 'timer': int, 'y_speed': int, 'font_size': int}
        self.next_life_score = 5000
        self.next_ts_score = 10000
        self.next_boss_score = 10000
        self.next_mega_score = 50000

        # Entities
        self.sound_manager = SoundManager()
        self.player = Player()
        self.enemies = [Enemy(self.progression_score) for _ in range(NUM_ENEMIES)]

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
        self.active_boss_bombs = [] # Seeking homing bombs
        self.boss_bomb_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'bomb1.png')).convert_alpha(), (32, 32)),
            pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'bomb2.png')).convert_alpha(), (32, 32))
        ]
        
        ex_sheet = pygame.image.load(os.path.join(IMAGES_PATH, 'bombexplode.png')).convert_alpha()
        self.bomb_ex_frames = []
        frame_w = ex_sheet.get_width() // 3
        frame_h = ex_sheet.get_height()
        for i in range(3):
            frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
            frame.blit(ex_sheet, (0, 0), (i * frame_w, 0, frame_w, frame_h))
            self.bomb_ex_frames.append(pygame.transform.scale(frame, (64, 64)))
        self.boss_flawless = False
        
        # Crate drop system (replacing old missile pickup)
        self.crate_img = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'crate.png')).convert_alpha(), (32, 32))
        self.crate2_img = pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_PATH, 'crate2.png')).convert_alpha(), (32, 32))
        self.active_pickups = [] # List of {'x': float, 'y': float, 'type': str}
        self.missile_kills_count = 0
        self.missile_kills_target = 100
        self.active_missile_explosions = [] # List of {'x': float, 'y': float, 'timer': int}
        
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
                    if event.key == pygame.K_a:
                        self.player.x_change = -PLAYER_SPEED
                    if event.key == pygame.K_d:
                        self.player.x_change = PLAYER_SPEED
                    if event.key == pygame.K_w:
                        self.player.y_change = -PLAYER_SPEED
                    if event.key == pygame.K_s:
                        self.player.y_change = PLAYER_SPEED
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.x_change = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.y_change = 0

            # Auto-fire logic (allow holding spacebar)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                shots_fired = self.player.shoot(self.sound_manager)
                if shots_fired:
                    self.stats['shots_fired'] += shots_fired
            
            # Missile fire (Shift key - single press only)
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                if not getattr(self, '_shift_held', False):
                    self._shift_held = True
                    self.player.fire_missile(self.sound_manager)
            else:
                self._shift_held = False

            # Update and draw player
            self.player.update()
            self.player.draw(self.screen)
            
            # Stats: Triple Shot Time
            if self.player.triple_shot_timer > 0:
                self.stats['triple_shot_frames'] += 1

            # Update and draw enemies + check collisions
            for enemy in self.enemies:
                enemy.update(self.progression_score)

                # Fireballs hits enemy
                if not enemy.explosion_visible:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.img.get_width(), enemy.img.get_height())
                    for fb in self.player.fireballs[:]:
                        fb_rect = pygame.Rect(fb['x'], fb['y'], fb['img'].get_width(), fb['img'].get_height())
                        if enemy_rect.colliderect(fb_rect):
                            if fb in self.player.fireballs:
                                self.player.fireballs.remove(fb)
                            self.stats['shots_hit'] += 1
                            
                            old_mult = self.get_combo_multiplier()
                            self.combo_kills += 1
                            new_mult = self.get_combo_multiplier()
                            if new_mult > old_mult:
                                self.sound_manager.play('multiply')
                                
                            old_progression = self.progression_score
                            
                            # Score gets Combo Multiplier (1x to 16x)
                            mult = self.get_combo_multiplier()
                            earned = int(enemy.points * mult)
                            self.score += earned
                            
                            # Progression gets background Difficulty Multiplier
                            diff_mult = self.get_difficulty_multiplier()
                            prog_earned = int(enemy.points * diff_mult)
                            self.progression_score += prog_earned
                            
                            # Centralized Milestone Check
                            self._check_score_milestones(old_progression)
                            
                            text_color = COLOR_GREEN
                            if enemy.points == 200:
                                text_color = COLOR_BLUE
                            elif enemy.points == 300:
                                text_color = COLOR_ORANGE
                            
                            self._add_floating_text(f"{earned:,}", enemy.x, enemy.y, text_color)
                            self.sound_manager.play('success')
                            
                            # Stats: Kills per type
                            if enemy.points == 100:
                                self.stats['enemies_killed'][0] += 1
                            elif enemy.points == 200:
                                self.stats['enemies_killed'][1] += 1
                            elif enemy.points == 300:
                                self.stats['enemies_killed'][2] += 1
                            
                            # Missile pickup crate drop with dynamic scaling based on progression score
                            self.missile_kills_count += 1
                            if self.missile_kills_count >= self.missile_kills_target:
                                self.missile_kills_count = 0
                                # Target kills grows by 15 for every 50,000 progression score
                                self.missile_kills_target = 100 + int(self.progression_score // 50000) * 15
                                self.active_pickups.append({'x': enemy.x + 16, 'y': enemy.y, 'type': 'missile'})
                                self._add_floating_text("MISSILE CRATE DROP!", -1, 100, COLOR_CYAN,
                                                        duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
                                self.sound_manager.play('bonus')
                            
                            enemy.explode(self.sound_manager)
                            break
                            # enemy.respawn() <-- Removed: update() handles this after explosion

                # Enemy hits player
                if not enemy.explosion_visible and not self.player.invincible:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.img.get_width(), enemy.img.get_height())
                    player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
                    if enemy_rect.colliderect(player_rect):
                        if self.player.hit(self.sound_manager):
                            self.stats['lives_lost'] += 1
                            self.boss_flawless = False
                            self.combo_kills = 0
                            self._add_floating_text("-1 LIFE", 350, 400, COLOR_RED, 
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                        enemy.explode(self.sound_manager)

                # Enemy escapes (reaches bottom)
                if not enemy.explosion_visible and enemy.y > 560:
                    penalty = int(1000 * self.get_difficulty_multiplier())
                    self.score = max(0, self.score - penalty)
                    self.progression_score = max(0, self.progression_score - 200) # Lighter progression hit
                    self.sound_manager.play('fail')
                    self._add_floating_text(f"-{penalty:,}", enemy.x, 540, COLOR_RED)
                    self.stats['enemies_escaped'] += 1
                    enemy.respawn(self.progression_score)

                enemy.draw(self.screen)

            # Boss Logic
            if self.boss:
                if self.boss.update():
                    self.boss = None
                    self.enemies = [Enemy(self.progression_score) for _ in range(min(50, NUM_ENEMIES + (self.progression_score // 25000) * 2))]
                else:
                    self.boss.draw(self.screen)
                
                # Check fireball hits boss
                if self.boss and not self.boss.is_exploding:
                    boss_rect = pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)
                    for fb in self.player.fireballs[:]:
                        fb_rect = pygame.Rect(fb['x'], fb['y'], fb['img'].get_width(), fb['img'].get_height())
                        if boss_rect.colliderect(fb_rect):
                            if fb in self.player.fireballs:
                                self.player.fireballs.remove(fb)
                            
                            self.stats['shots_hit'] += 1
                            self.sound_manager.play('boss_hit')
                            old_progression = self.progression_score
                            
                            # Score gets Combo Multiplier (1x to 16x)
                            mult = self.get_combo_multiplier()
                            base_pts = 200 if self.boss.is_mega else 100
                            pts = int(base_pts * mult)
                            self.score += pts
                            
                            # Progression gets background Difficulty Multiplier
                            diff_mult = self.get_difficulty_multiplier()
                            prog_pts = int(base_pts * diff_mult)
                            self.progression_score += prog_pts
                            
                            color = COLOR_BLUE if self.boss.is_mega else COLOR_GREEN
                            self.stats['boss_hits'] += 1
                            self._check_score_milestones(old_progression)
                            self._add_floating_text(f"{pts:,}", fb['x'], fb['y'], color)
                            
                            is_dead, should_spawn_bomb = self.boss.hit()
                            if should_spawn_bomb:
                                self._spawn_boss_bomb()
                                
                            if is_dead:
                                # Boss Killed!
                                kill_score = 25000 if self.boss.is_mega else 10000
                                kill_text = "MEGA BOSS KILL!" if self.boss.is_mega else "BOSS KILL!"
                                
                                # Cinematic Mega Boss Death
                                if self.boss.is_mega:
                                    self.sound_manager.play('explosion2')
                                
                                old_progression = self.progression_score
                                self.score += kill_score
                                
                                # Progression gets background Difficulty Multiplier
                                diff_mult = self.get_difficulty_multiplier()
                                prog_kill = int(kill_score * diff_mult)
                                self.progression_score += prog_kill
                                
                                self._check_score_milestones(old_progression)
                                
                                self.player.activate_triple_shot()
                                self.player.triple_shot_timer = 1800 # 30 seconds
                                self.sound_manager.play('powerup')
                                
                                # Reward: Invincibility (2 seconds = 120 frames)
                                self.player.invincible = True
                                self.player.invincible_timer = -60 # Starts negative so it has 120 frames before hitting 60
                                
                                # Flawless Bonus Check (Flat bonus, no combo multiplier)
                                if self.boss_flawless:
                                    flawless_score = 5000 if self.boss.is_mega else 2000
                                    self.score += flawless_score
                                    
                                    prog_flawless = int(flawless_score * diff_mult)
                                    self.progression_score += prog_flawless
                                    
                                    flawless_color = COLOR_ORANGE if self.boss.is_mega else COLOR_BLUE
                                    self._add_floating_text("FLAWLESS!", -1, 150, COLOR_ORANGE, duration=180, font_size=FONT_SIZE_MD)
                                    self._add_floating_text(f"{flawless_score:,}", -1, 200, flawless_color, duration=180, font_size=FONT_SIZE_MD)
                                    self.boss_flawless = False # Reset
                                
                                self._add_floating_text(kill_text, -1, 250, COLOR_GREEN, 
                                                        duration=180, y_speed=-1, font_size=FONT_SIZE_MD)
                                self._add_floating_text(f"{kill_score:,}", -1, 320, COLOR_YELLOW, 
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
                
                # Check missile hits boss
                if self.boss and not self.boss.is_exploding:
                    boss_rect = pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)
                    for m in self.player.active_missiles[:]:
                        m_rect = pygame.Rect(m['x'], m['y'], 20, 40)
                        if boss_rect.colliderect(m_rect):
                            if m in self.player.active_missiles:
                                self.player.active_missiles.remove(m)
                            
                            # Massive damage: regular boss has 20HP, mega has 60HP
                            # Missile deals 20 damage (kills regular in 1, mega in 3 but we want 2)
                            missile_damage = 30 if self.boss.is_mega else 20
                            for _ in range(missile_damage):
                                is_dead, should_spawn_bomb = self.boss.hit()
                                if should_spawn_bomb:
                                    self._spawn_boss_bomb()
                                if is_dead:
                                    break
                            
                            # Missile explosion effect
                            self.active_missile_explosions.append({'x': m_rect.x - 22, 'y': m_rect.y - 12, 'timer': 0})
                            self.sound_manager.play('boom')
                            
                            self._add_floating_text("MISSILE HIT!", self.boss.x + 20, self.boss.y, COLOR_CYAN,
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                            
                            if is_dead:
                                # Boss Killed by missile!
                                kill_score = 25000 if self.boss.is_mega else 10000
                                kill_text = "MEGA BOSS KILL!" if self.boss.is_mega else "BOSS KILL!"
                                
                                if self.boss.is_mega:
                                    self.sound_manager.play('explosion2')
                                
                                old_progression = self.progression_score
                                self.score += kill_score
                                diff_mult = self.get_difficulty_multiplier()
                                prog_kill = int(kill_score * diff_mult)
                                self.progression_score += prog_kill
                                self._check_score_milestones(old_progression)
                                
                                self.player.activate_triple_shot()
                                self.player.triple_shot_timer = 1800
                                self.sound_manager.play('powerup')
                                self.player.invincible = True
                                self.player.invincible_timer = -60
                                
                                if self.boss_flawless:
                                    flawless_score = 5000 if self.boss.is_mega else 2000
                                    self.score += flawless_score
                                    prog_flawless = int(flawless_score * diff_mult)
                                    self.progression_score += prog_flawless
                                    self._add_floating_text("FLAWLESS!", -1, 150, COLOR_ORANGE, duration=180, font_size=FONT_SIZE_MD)
                                    flawless_color = COLOR_ORANGE if self.boss.is_mega else COLOR_BLUE
                                    self._add_floating_text(f"{flawless_score:,}", -1, 200, flawless_color, duration=180, font_size=FONT_SIZE_MD)
                                    self.boss_flawless = False
                                
                                self._add_floating_text(kill_text, -1, 250, COLOR_GREEN,
                                                        duration=180, y_speed=-1, font_size=FONT_SIZE_MD)
                                self._add_floating_text(f"{kill_score:,}", -1, 320, COLOR_YELLOW,
                                                        duration=180, y_speed=-1, font_size=FONT_SIZE_MD)
                                self.sound_manager.play('boss_kill')
                                self.sound_manager.stop_danger()
                                
                                if self.boss.is_mega:
                                    self.stats['mega_bosses_defeated'] += 1
                                else:
                                    self.stats['bosses_defeated'] += 1
                            break

                # Check missiles hit enemies
                for m in self.player.active_missiles[:]:
                    m_rect = pygame.Rect(m['x'], m['y'], 20, 40)
                    for enemy in self.enemies:
                        if not enemy.explosion_visible:
                            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.img.get_width(), enemy.img.get_height())
                            if m_rect.colliderect(enemy_rect):
                                if m in self.player.active_missiles:
                                    self.player.active_missiles.remove(m)
                                self.active_missile_explosions.append({'x': enemy.x - 12, 'y': enemy.y - 12, 'timer': 0})
                                self.sound_manager.play('boom')
                                enemy.explode(self.sound_manager)
                                break

                # Boss hits player directly
                if self.boss and not self.boss.is_exploding and not self.player.invincible:
                    boss_rect = pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)
                    player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
                    if boss_rect.colliderect(player_rect):
                        if self.player.hit(self.sound_manager):
                            self.stats['lives_lost'] += 1
                            self.boss_flawless = False
                            self.combo_kills = 0
                            self._add_floating_text("-1 LIFE", 350, 400, COLOR_RED, 
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)

            # Laser logic
            self._update_laser()

            # Player hit by laser
            if self.laser_visible and not self.player.invincible:
                laser_rect = pygame.Rect(self.laser_x, self.laser_y, self.active_laser_img.get_width(), self.active_laser_img.get_height())
                player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
                if laser_rect.colliderect(player_rect):
                    self.laser_visible = False
                    if self.player.hit(self.sound_manager):
                        self.stats['lives_lost'] += 1
                        self.boss_flawless = False
                        self.combo_kills = 0
                        self._add_floating_text("-1 LIFE", 350, 400, COLOR_RED, 
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)

            # Missile pickups and explosion animations
            self._update_pickups_and_missile_explosions()

            # Floating text display (+score, -penalty, flawless, lives)
            # Sort so "FLAWLESS" texts are rendered last to always sit on top of all other alert texts
            for ft in sorted(self.floating_texts[:], key=lambda x: 1 if "FLAWLESS" in x['text'] else 0):
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

            # Check game over (after player explosion finishes)
            if self.player.lives <= 0 and not self.player.explosion_visible \
                    and not self.game_over:
                self.game_over = True
                self.sound_manager.stop_music()
                self.sound_manager.stop_danger()
                self.sound_manager.play('game_over')

            # Update screen
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    # ---- Private helpers ----

    def _check_score_milestones(self, old_progression):
        """Check and apply score-based milestones and rewards using progression_score"""
        # Difficulty Increase every 25k (Reinforcements)
        if (old_progression // 25000) < (self.progression_score // 25000):
            if len(self.enemies) < 50:
                self.enemies.extend([Enemy(self.progression_score) for _ in range(2)])
                self._add_floating_text("ENEMY REINFORCEMENTS!", -1, 100, COLOR_RED, 
                                        duration=150, y_speed=-0.5, font_size=FONT_SIZE_MD)
                self.sound_manager.play('bonus')
            else:
                self._add_floating_text("ELITE SQUADRON INBOUND!", -1, 100, (255, 0, 255), 
                                        duration=150, y_speed=-0.5, font_size=FONT_SIZE_MD)
                self.sound_manager.play('bonus')

        # Overshield every 100k
        if (old_progression // 100000) < (self.progression_score // 100000):
            import random
            rx = random.randint(100, SCREEN_WIDTH - 100)
            self.active_pickups.append({'x': rx, 'y': -40, 'type': 'overshield'})
            self._add_floating_text("OVERSHIELD CARGO INBOUND!", -1, 100, COLOR_CYAN, 
                                    duration=150, y_speed=-0.5, font_size=FONT_SIZE_MD)
            self.sound_manager.play('bonus')

        # Exponential Life Gain
        while self.progression_score >= self.next_life_score:
            if self.player.lives < 3:
                self.player.lives += 1
                self.stats['lives_earned'] += 1
                self.sound_manager.play('bonus')
                self._add_floating_text("+1 LIFE", -1, 400, COLOR_GREEN, 
                                        duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
            else:
                self.player.activate_triple_shot()
                self._add_floating_text("TRIPLE SHOT!", -1, 350, COLOR_CYAN, 
                                        duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
                self.sound_manager.play('powerup')
            
            self.next_life_score *= 2

        # Exponential Triple Shot Gain
        while self.progression_score >= self.next_ts_score:
            self.player.activate_triple_shot()
            self._add_floating_text("TRIPLE SHOT!", -1, 350, COLOR_CYAN, 
                                    duration=120, y_speed=-1, font_size=FONT_SIZE_MD)
            self.sound_manager.play('powerup')
            self.next_ts_score *= 2

        # Dynamic Boss Spawns
        spawned_boss = False
        while self.progression_score >= self.next_mega_score:
            if self.progression_score >= 1000000:
                self.next_mega_score += 500000
            elif self.progression_score >= 500000:
                self.next_mega_score += 250000
            elif self.progression_score >= 250000:
                self.next_mega_score += 100000
            else:
                self.next_mega_score += 50000
                
            if not self.boss and not spawned_boss:
                if self.score < 1000000:
                    self.enemies = []
                self.boss = Boss(is_mega=True)
                self._add_floating_text("MEGA BOSS INCOMING!", -1, 300, (255, 0, 255), 
                                        duration=200, y_speed=-0.2, font_size=FONT_SIZE_MD)
                self.sound_manager.play_danger()
                self.boss_flawless = True
                spawned_boss = True

        while self.progression_score >= self.next_boss_score:
            if self.progression_score >= 1000000:
                self.next_boss_score += 200000
            elif self.progression_score >= 500000:
                self.next_boss_score += 100000
            elif self.progression_score >= 250000:
                self.next_boss_score += 50000
            elif self.progression_score >= 100000:
                self.next_boss_score += 20000
            else:
                self.next_boss_score += 10000
                
            if not self.boss and not spawned_boss:
                if self.score < 1000000:
                    self.enemies = []
                self.boss = Boss(is_mega=False)
                self._add_floating_text("BOSS INCOMING!", -1, 300, COLOR_RED, 
                                        duration=180, y_speed=-0.2, font_size=FONT_SIZE_MD)
                self.sound_manager.play_danger()
                self.boss_flawless = True
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
                if self.boss.is_mega:
                    ly = self.boss.y + self.boss.height - 65 # Spawns higher up to align with mega boss cannons
                else:
                    ly = self.boss.y + self.boss.height - 20 # Perfect intermediate offset between 10px and 30px
                
                if self.boss.is_mega:
                    self.active_boss_lasers.append({
                        'x': l1_x, 'y': ly, 
                        'frames': self.boss.laser_frames, 
                        'frame_idx': 0, 'anim_timer': 0, 'anim': True
                    })
                    self.active_boss_lasers.append({
                        'x': l2_x, 'y': ly, 
                        'frames': self.boss.laser_frames, 
                        'frame_idx': 0, 'anim_timer': 0, 'anim': True
                    })
                else:
                    self.active_boss_lasers.append({
                        'x': l1_x, 'y': ly, 
                        'img': self.boss.laser_img, 'anim': False
                    })
                    self.active_boss_lasers.append({
                        'x': l2_x, 'y': ly, 
                        'img': self.boss.laser_img, 'anim': False
                    })
                
                self.sound_manager.play('enemy_shot')
                self.laser_timer = 0
                self.laser_interval = random.randint(LASER_INTERVAL_MIN, LASER_INTERVAL_MAX)

        # Update and draw boss lasers
        for bl in self.active_boss_lasers[:]:
            if bl.get('anim', False):
                bl['anim_timer'] += 1
                if bl['anim_timer'] >= 6: # Flop back and forth every 6 frames
                    bl['anim_timer'] = 0
                    bl['frame_idx'] = 1 - bl['frame_idx']
                active_img = bl['frames'][bl['frame_idx']]
            else:
                active_img = bl['img']
                
            self.screen.blit(active_img, (bl['x'], bl['y']))
            bl['y'] += self.laser_y_change
            
            # Check collision with player
            if not self.player.invincible:
                laser_rect = pygame.Rect(bl['x'], bl['y'], active_img.get_width(), active_img.get_height())
                player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
                if laser_rect.colliderect(player_rect):
                    if self.player.hit(self.sound_manager):
                        self.stats['lives_lost'] += 1
                        self.boss_flawless = False
                        self.combo_kills = 0
                        self._add_floating_text("-1 LIFE", 350, 400, COLOR_RED, 
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                    if bl in self.active_boss_lasers:
                        self.active_boss_lasers.remove(bl)
                    continue

            if bl['y'] > SCREEN_HEIGHT:
                if bl in self.active_boss_lasers:
                    self.active_boss_lasers.remove(bl)

        # Update and draw boss bombs (seeking homing projectiles)
        for bb in self.active_boss_bombs[:]:
            if bb.get('exploding', False):
                # Handle explosion animation
                bb['ex_timer'] += 1
                if bb['ex_timer'] >= 15: # 3 frames * 5 ticks
                    if bb in self.active_boss_bombs:
                        self.active_boss_bombs.remove(bb)
                    continue
                frame_idx = min(2, bb['ex_timer'] // 5)
                # Offset by -16 to center the 64x64 explosion over the 32x32 bomb
                self.screen.blit(self.bomb_ex_frames[frame_idx], (bb['x'] - 16, bb['y'] - 16))
                continue

            # Update timer and blinking
            bb['timer'] -= 1
            if bb['timer'] <= 0:
                bb['exploding'] = True
                self.sound_manager.stop_tick()
                self.sound_manager.play('boom')
                continue

            # Blinking gets faster as timer drops (from ~15 frames down to 2 frames)
            blink_speed = max(2, int((bb['timer'] / 120) * 15))
            bb['anim_timer'] += 1
            if bb['anim_timer'] >= blink_speed:
                bb['anim_timer'] = 0
                bb['frame_idx'] = 1 - bb['frame_idx']
                self.sound_manager.play('tick')
                
            self.screen.blit(self.boss_bomb_frames[bb['frame_idx']], (bb['x'], bb['y']))
            
            # Draw bomb health bar
            bar_width = 32
            pygame.draw.rect(self.screen, (255, 0, 0), (bb['x'], bb['y'] - 8, bar_width, 4))
            pygame.draw.rect(self.screen, (0, 255, 0), (bb['x'], bb['y'] - 8, bar_width * (bb['hp'] / bb['max_hp']), 4))

            # True 2D full-directional homing towards player center
            player_center_x = self.player.x + 32 # Ship is 64x64
            player_center_y = self.player.y + 32
            bomb_center_x = bb['x'] + 16 # Bomb is 32x32
            bomb_center_y = bb['y'] + 16
            
            dx = player_center_x - bomb_center_x
            dy = player_center_y - bomb_center_y
            dist = math.hypot(dx, dy)
            
            seek_speed = 3.5 # Extremely responsive 2D seek speed
            if dist != 0:
                bb['x'] += (dx / dist) * seek_speed
                bb['y'] += (dy / dist) * seek_speed
                
            bomb_rect = pygame.Rect(bb['x'], bb['y'], 32, 32)

            # Check collision with player's fireballs
            hit_by_player = False
            for fb in self.player.fireballs[:]:
                fb_rect = pygame.Rect(fb['x'], fb['y'], fb['img'].get_width(), fb['img'].get_height())
                if bomb_rect.colliderect(fb_rect):
                    if fb in self.player.fireballs:
                        self.player.fireballs.remove(fb)
                    
                    bb['hp'] -= 1
                    if bb['hp'] <= 0:
                        bb['exploding'] = True
                        self.sound_manager.stop_tick()
                        self.sound_manager.play('boom')
                        hit_by_player = True
                        # Reward for shooting a bomb out of the sky
                        self.score += 500
                        self._add_floating_text("500", bb['x'], bb['y'], COLOR_CYAN)
                    else:
                        self.sound_manager.play('boss_hit')
                    break
                    
            if hit_by_player:
                continue

            # Check proximity collision with player (64x64 trigger area)
            if not self.player.invincible:
                proximity_rect = pygame.Rect(bb['x'] - 16, bb['y'] - 16, 64, 64)
                player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
                if proximity_rect.colliderect(player_rect):
                    if self.player.hit(self.sound_manager):
                        self.stats['lives_lost'] += 1
                        self.boss_flawless = False
                        self.combo_kills = 0
                        self._add_floating_text("-1 LIFE", 350, 400, COLOR_RED, 
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                    bb['exploding'] = True
                    self.sound_manager.stop_tick()
                    self.sound_manager.play('boom')
                    continue
                    
            if bb['y'] > SCREEN_HEIGHT:
                if bb in self.active_boss_bombs:
                    self.active_boss_bombs.remove(bb)

    def _spawn_boss_bomb(self):
        """Spawn a semi-homing bomb from the center of the boss"""
        if self.boss:
            bx = self.boss.x + self.boss.width // 2 - 20
            by = self.boss.y + self.boss.height - 20
            self.active_boss_bombs.append({
                'x': bx, 'y': by,
                'timer': 300, # 5 seconds at 60fps
                'frame_idx': 0,
                'anim_timer': 0,
                'exploding': False,
                'ex_timer': 0,
                'hp': 2,
                'max_hp': 2
            })
            self.sound_manager.play('enemy_shot')

    def _update_pickups_and_missile_explosions(self):
        """Update and draw missile and overshield crate pickups falling and missile explosions"""
        # Draw falling pickups (missile crates and overshield crates)
        for pickup in self.active_pickups[:]:
            img = self.crate_img if pickup['type'] == 'missile' else self.crate2_img
            self.screen.blit(img, (pickup['x'], pickup['y']))
            pickup['y'] += 2 # Slow descent
            
            # Player collects pickup
            pickup_rect = pygame.Rect(pickup['x'], pickup['y'], 32, 32)
            player_rect = pygame.Rect(self.player.x, self.player.y, 64, 64)
            if pickup_rect.colliderect(player_rect):
                self.active_pickups.remove(pickup)
                self.sound_manager.play('powerup') # Plays powerup.mp3
                
                if pickup['type'] == 'missile':
                    if self.player.missiles >= 4:
                        if self.player.lives < 3:
                            self.player.lives += 1
                            self.stats['lives_earned'] += 1
                            self.sound_manager.play('bonus')
                            self._add_floating_text("+1 LIFE", -1, 350, COLOR_GREEN,
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                        else:
                            self.score += 2000
                            self._add_floating_text("+2,000 PTS (MAX MISSILES)", -1, 350, COLOR_YELLOW,
                                                    duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                            self.sound_manager.play('bonus')
                    else:
                        self.player.missiles = min(4, self.player.missiles + 2) # Instantly mounts and shows missiles
                        self._add_floating_text("+2 MISSILES!", -1, 350, COLOR_CYAN,
                                                duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                elif pickup['type'] == 'overshield':
                    self.player.overshield = 2
                    self._add_floating_text("OVERSHIELD CHARGED!", -1, 350, COLOR_YELLOW,
                                            duration=90, y_speed=-2, font_size=FONT_SIZE_MD)
                continue
            
            if pickup['y'] > SCREEN_HEIGHT:
                self.active_pickups.remove(pickup)
        
        # Draw missile explosions (reuse bomb explosion frames)
        for me in self.active_missile_explosions[:]:
            me['timer'] += 1
            if me['timer'] >= 15:
                self.active_missile_explosions.remove(me)
                continue
            frame_idx = min(2, me['timer'] // 5)
            self.screen.blit(self.bomb_ex_frames[frame_idx], (me['x'], me['y']))

    def _draw_score(self):
        """Draw the score in the top-right and the combo multiplier in the top-middle"""
        score_text = self.font.render(f"Score: {self.score:,}", True, COLOR_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 10))
        
        # Combo Multiplier (Top-Middle)
        combo = self.get_combo_multiplier()
        combo_text = f"x{combo}"
        
        # Color transitions for combo levels
        combo_color = COLOR_WHITE
        if combo == 2: combo_color = COLOR_GREEN
        elif combo == 4: combo_color = COLOR_BLUE
        elif combo == 8: combo_color = COLOR_ORANGE
        elif combo == 16: combo_color = COLOR_YELLOW
        
        combo_surf = self.font.render(combo_text, True, combo_color)
        self.screen.blit(combo_surf, ((SCREEN_WIDTH - combo_surf.get_width()) // 2, 10))

    def get_difficulty_multiplier(self):
        """Return the current background difficulty multiplier based on progression score"""
        if self.progression_score >= 1000000: return 3.0
        if self.progression_score >= 500000: return 2.5
        if self.progression_score >= 250000: return 2.0
        if self.progression_score >= 150000: return 1.75
        if self.progression_score >= 100000: return 1.5
        if self.progression_score >= 50000: return 1.25
        return 1.0

    def get_combo_multiplier(self):
        """Return the skill-based scoring combo multiplier based on kills without dying"""
        if self.combo_kills >= 40: return 16
        if self.combo_kills >= 30: return 8
        if self.combo_kills >= 20: return 4
        if self.combo_kills >= 10: return 2
        return 1

    def _draw_game_over(self):
        """Draw the game over overlay with detailed stats"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210)) # Slightly darker for readability
        self.screen.blit(overlay, (0, 0))

        go_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        sub_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)
        stat_font = pygame.font.SysFont('Arial', 18, bold=True)

        # Title
        go_text = go_font.render("GAME OVER", True, COLOR_RED)
        self.screen.blit(go_text, (400 - go_text.get_width() // 2, 60))
        
        score_text = sub_font.render(f"Final Score: {self.score:,}", True, COLOR_YELLOW)
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 140))

        # Stats Section
        y_off = 220
        # Enemy Kills
        kills = self.stats['enemies_killed']
        escaped = self.stats['enemies_escaped']
        
        # Render Kills (Icons)
        k_head = stat_font.render("KILLS:", True, COLOR_WHITE)
        self.screen.blit(k_head, (120, y_off))
        
        self.screen.blit(self.ui_images['enemy1'], (190, y_off - 10))
        self.screen.blit(stat_font.render(f"x{kills[0]}", True, COLOR_WHITE), (240, y_off))
        
        self.screen.blit(self.ui_images['enemy2'], (300, y_off - 10))
        self.screen.blit(stat_font.render(f"x{kills[1]}", True, COLOR_WHITE), (350, y_off))
        
        self.screen.blit(self.ui_images['enemy3'], (410, y_off - 10))
        self.screen.blit(stat_font.render(f"x{kills[2]}", True, COLOR_WHITE), (460, y_off))
        
        # Escaped
        esc_color = COLOR_GREEN if escaped == 0 else (255, 50, 50)
        esc_label = stat_font.render("ESCAPED:", True, COLOR_WHITE)
        esc_val = stat_font.render(str(escaped), True, esc_color)
        self.screen.blit(esc_label, (540, y_off))
        self.screen.blit(esc_val, (640, y_off))
        
        # Bosses
        y_off += 60
        b_head = stat_font.render("BOSSES:", True, COLOR_BLUE)
        self.screen.blit(b_head, (180, y_off + 15))
        
        self.screen.blit(self.ui_images['boss'], (280, y_off - 5))
        self.screen.blit(stat_font.render(f"x{self.stats['bosses_defeated']}", True, COLOR_BLUE), (350, y_off + 15))
        
        self.screen.blit(self.ui_images['mega_boss'], (420, y_off - 15))
        self.screen.blit(stat_font.render(f"x{self.stats['mega_bosses_defeated']}", True, COLOR_BLUE), (510, y_off + 15))
        
        # Triple Shot Time
        ts_secs = self.stats['triple_shot_frames'] // 60
        ts_str = f"TRIPLE SHOT TOTAL TIME: {ts_secs}s"
        e_surf = stat_font.render(ts_str, True, COLOR_CYAN)
        self.screen.blit(e_surf, (400 - e_surf.get_width() // 2, y_off + 70))
        
        # Lives
        life_str = f"LIVES: Earned [{self.stats['lives_earned']}]  Lost [{self.stats['lives_lost']}]"
        l_surf = stat_font.render(life_str, True, COLOR_GREEN)
        self.screen.blit(l_surf, (400 - l_surf.get_width() // 2, y_off + 105))

        # Accuracy
        fired = self.stats['shots_fired']
        hit = self.stats['shots_hit']
        acc = (hit / fired * 100) if fired > 0 else 0
        acc_str = f"ACCURACY: {acc:.1f}%  (Fired: {fired} | Hits: {hit})"
        a_surf = stat_font.render(acc_str, True, COLOR_ORANGE) # Orange
        self.screen.blit(a_surf, (400 - a_surf.get_width() // 2, y_off + 140))

        # Footer
        restart_text = sub_font.render("R - Restart    ESC - Quit", True, COLOR_WHITE)
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
        desc1 = desc_font.render("Defend Earth from the alien invasion!", True, COLOR_WHITE)
        controls = desc_font.render("WASD to Move  |  SPACE to Shoot  |  P to Pause", True, COLOR_GRAY)
        rules_prompt = desc_font.render("Press H for Rules & Scoring", True, COLOR_CYAN)
        prompt_text = prompt_font.render("Press ANY OTHER KEY to Start", True, COLOR_YELLOW)

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
        header_color = COLOR_CYAN
        text_color = COLOR_WHITE

        title = title_font.render("MISSION RULES", True, header_color)
        self.screen.blit(title, (400 - title.get_width() // 2, 50))
        
        # --- Column 1: SCORING (Left) ---
        s_head = title_font.render("SCORING", True, COLOR_GREEN)
        self.screen.blit(s_head, (50, 150))
        
        scores = [
            (self.ui_images['enemy1'], "100 pts", COLOR_GREEN),
            (self.ui_images['enemy2'], "200 pts", COLOR_BLUE),
            (self.ui_images['enemy3'], "300 pts", COLOR_ORANGE)
        ]
        for i, (img, value, color) in enumerate(scores):
            self.screen.blit(img, (30, 200 + i * 55))
            value_surf = body_font.render(value, True, color)
            self.screen.blit(value_surf, (80, 210 + i * 55))

        # --- Column 2: THREATS (Center) ---
        p_head = title_font.render("THREATS", True, COLOR_RED)
        self.screen.blit(p_head, (400 - p_head.get_width() // 2, 150))
        
        penalties = [
            ("Enemy Escapes: ", "-1000 pts"),
            ("Hit by enemy or Laser: ", "-1 Life"),
            ("Max Lives: ", "3")
        ]
        for i, (label, value) in enumerate(penalties):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, COLOR_RED)
            x_pos = 400 - (label_surf.get_width() + value_surf.get_width()) // 2
            self.screen.blit(label_surf, (x_pos, 210 + i * 35))
            self.screen.blit(value_surf, (x_pos + label_surf.get_width(), 210 + i * 35))

        # --- Column 3: BOSSES (Right) ---
        b_head = title_font.render("BOSSES", True, COLOR_YELLOW)
        self.screen.blit(b_head, (SCREEN_WIDTH - b_head.get_width() - 50, 150))
        
        # Regular Boss
        self.screen.blit(self.ui_images['boss'], (560, 200))
        b1_txt = body_font.render("20HP (10k pts per kill)", True, COLOR_YELLOW)
        b1_hit = body_font.render("100pts per hit", True, COLOR_GREEN)
        self.screen.blit(b1_txt, (630, 210))
        self.screen.blit(b1_hit, (630, 230))
        
        # Mega Boss
        self.screen.blit(self.ui_images['mega_boss'], (540, 270))
        b2_txt = body_font.render("60HP (25k pts per kill)", True, COLOR_YELLOW)
        b2_hit = body_font.render("200pts per hit", True, COLOR_BLUE)
        self.screen.blit(b2_txt, (630, 280))
        self.screen.blit(b2_hit, (630, 300))

        # --- Footer: BONUS UPGRADES ---
        up_head = title_font.render("BONUS UPGRADES", True, COLOR_BLUE)
        self.screen.blit(up_head, (400 - up_head.get_width() // 2, 400))
        
        bonuses = [
            ("Triple Shot (TS): ", "Earned on Life Overflow (or every 10k, 20k... etc.)"),
            ("OVERSHIELD: ", "Absorb 2 Hits (Every 100k pts)"),
            ("MISSILES: ", "Press SHIFT to Fire. 2 per Crate (Spawned from enemy kills)")
        ]
        for i, (label, value) in enumerate(bonuses):
            label_surf = body_font.render(label, True, text_color)
            value_surf = body_font.render(value, True, COLOR_BLUE)
            x_pos = 400 - (label_surf.get_width() + value_surf.get_width()) // 2
            self.screen.blit(label_surf, (x_pos, 450 + i * 30))
            self.screen.blit(value_surf, (x_pos + label_surf.get_width(), 450 + i * 30))

        prompt = body_font.render("Press H or ESC to go back", True, COLOR_GRAY)
        self.screen.blit(prompt, (400 - prompt.get_width() // 2, 550))

    def _draw_pause_menu(self):
        """Draw the pause menu overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        pause_font = pygame.font.Font(FONT_PATH, FONT_SIZE_LG)
        prompt_font = pygame.font.Font(FONT_PATH, FONT_SIZE_MD)

        pause_text = pause_font.render("PAUSED", True, COLOR_WHITE)
        prompt_text = prompt_font.render("Press P to Resume", True, COLOR_WHITE)

        self.screen.blit(pause_text, (400 - pause_text.get_width() // 2, 250))
        self.screen.blit(prompt_text, (400 - prompt_text.get_width() // 2, 340))

    def _restart(self):
        """Reset all game state for a new round"""
        self.score = 0
        self.progression_score = 0
        self.combo_kills = 0
        self.game_over = False
        self.player.reset()
        self.enemies = [Enemy(self.progression_score) for _ in range(NUM_ENEMIES)]
        self.laser_visible = False
        self.laser_timer = 0
        self.laser_interval = LASER_INTERVAL_MAX
        self.boss = None
        self.active_boss_lasers = []
        self.active_boss_bombs = []
        self.boss_flawless = False
        self.floating_texts = []
        self.last_life_bonus = 0
        self.next_life_score = 5000
        self.next_ts_score = 10000
        self.next_boss_score = 10000
        self.next_mega_score = 50000
        self.active_pickups = []
        self.active_missile_explosions = []
        self.missile_kills_count = 0
        self.missile_kills_target = 100
        self._shift_held = False
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