"""
Day 10 challenge is all about using pygame to make a game!
This is going to be a real fun one!
"""
# Have to use pygame-ce since pygame is not available for python 3.14
import pygame
import os
import random
import math
from pygame import mixer

cwd = os.getcwd()
images_path = os.path.join(cwd, 'images')
sounds_path = os.path.join(cwd, 'sounds')

def main():
    """
    Main game logic will go here
    """
    # Initilize the game
    pygame.init()
    clock = pygame.time.Clock()
    score = 0
    game_over = False
    font = pygame.font.Font('Score.ttf', 24)
    # background music
    mixer.music.load(os.path.join(sounds_path, 'bg_music.mp3'))
    mixer.music.set_volume(.5)
    mixer.music.play(-1)

    # Sounds
    pygame.mixer.init()
    fire_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'fire_shot.mp3'))
    enemy_explosion_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'explosion_1.mp3'))
    player_explosion_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'explosion_2.mp3'))
    enemy_shot_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'enemy_shot.mp3'))
    success_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'success.mp3'))
    lose_life_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'lose_life.mp3'))
    game_over_sound = pygame.mixer.Sound(os.path.join(sounds_path, 'game_over.mp3'))
    
    # Create the game screen
    screen = pygame.display.set_mode((800,600))
    
    # Title and Icon
    pygame.display.set_caption("Space Invaders")
    # Icon
    icon = pygame.image.load(os.path.join(images_path, 'ufo.png'))
    pygame.display.set_icon(icon)
    # Background image
    background = pygame.image.load(os.path.join(images_path, 'BG.jpg'))

    # Lives
    lives_img = pygame.image.load(os.path.join(images_path, 'ship_smaller.png'))
    redx_img = pygame.image.load(os.path.join(images_path, 'redx.png'))
    lives = 3

    # Player
    player_img = pygame.image.load(os.path.join(images_path, 'ship.png'))
    player_x = 368
    player_y = 520
    player_x_change = 0
    player_y_change = 0

    # Enemy
    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []

    num_enemies = 5
    
    for enemy in range(num_enemies):
        enemy_img.append(pygame.image.load(os.path.join(images_path, 'enemyship.png')))
        enemy_x.append(random.randint(0, 736))
        enemy_y.append(random.randint(50, 200))
        enemy_x_change.append(6)
        enemy_y_change.append(50)

    # Fireball
    fireball_img = pygame.image.load(os.path.join(images_path, 'fireball.png'))
    fireball_x = 0
    fireball_y = 520
    fireball_x_change = 0
    fireball_y_change = 25
    fireball_visible = False

    # Laser
    laser_img = pygame.image.load(os.path.join(images_path, 'laser.png'))
    laser_x = 0
    laser_y = 0
    laser_y_change = 15
    laser_visible = False
    laser_timer = 0
    laser_interval = 150

    # Enemy Explosion
    enemy_explode_img = pygame.image.load(os.path.join(images_path, 'enemyexplode.png'))
    explosion_x = 0
    explosion_y = 0
    explosion_visible = False
    explosion_timer = 0
    explosion_duration = 20

    # Player explosion
    player_explode_img = pygame.image.load(os.path.join(images_path, 'explode.png'))
    player_explosion_visible = False
    player_explosion_timer = 0
    player_explosion_duration = 20
    player_invincible = False
    player_invincible_timer = 0
    player_invincible_duration = 60

    def player(x, y):
        """
        Draws the player image onto the screen
        """
        # Flash every 6 frames when invincible
        if player_invincible and (player_invincible_timer // 6) % 2 == 0:
            return  # skip drawing = flash effect
        screen.blit(player_img, (x, y))
    
    def draw_lives():
        """
        Draws the lives onto the screen
        """
        bar = pygame.Surface((120, 45), pygame.SRCALPHA)
        bar.fill((0, 60, 80, 180))
        screen.blit(bar, (0, 0))
        for i in range(3):
            if i < lives:
                screen.blit(lives_img, (10 + i * (lives_img.get_width() + 5), 8))
            else:
                screen.blit(redx_img, (10 + i * (lives_img.get_width() + 5), 8))

    def draw_enemy(x, y, i):
        """
        Draws the enemy image onto the screen
        """
        screen.blit(enemy_img[i], (x, y))

    def shoot_fireball(x, y):
        """
        Shoot the fireball across the screen
        """
        nonlocal fireball_visible, fireball_x, fireball_y
        fireball_visible = True
        fireball_x = x
        fireball_y = y
        fire_sound.play()

    def detect_collision(x1, y1, x2, y2):
        """
        Detects collision between two objects
        """
        distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        if distance < 27:
            return True
        return False

    def trigger_enemy_explosion(x, y):
        nonlocal explosion_visible, explosion_x, explosion_y, explosion_timer
        explosion_x = x
        explosion_y = y
        explosion_visible = True
        explosion_timer = 0
        enemy_explosion_sound.play()

    def trigger_player_explosion():
        nonlocal player_explosion_visible, player_explosion_timer, player_invincible, player_invincible_timer
        player_explosion_visible = True
        player_explosion_timer = 0
        player_invincible = True
        player_invincible_timer = 0
        player_explosion_sound.play()
        lose_life_sound.play()

    def draw_score():
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (600, 10))

    def draw_game_over():
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        go_font = pygame.font.Font('Score.ttf', 64)
        sub_font = pygame.font.Font('Score.ttf', 32)
        go_text = go_font.render("GAME OVER", True, (255, 0, 0))
        score_text = sub_font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = sub_font.render("R - Restart    ESC - Quit", True, (255, 255, 255))
        screen.blit(go_text, (400 - go_text.get_width() // 2, 200))
        screen.blit(score_text, (400 - score_text.get_width() // 2, 300))
        screen.blit(restart_text, (400 - restart_text.get_width() // 2, 370))

    # Game loop
    is_running = True
    while is_running:
        # Background image
        screen.blit(background, (0, 0))
        if game_over:
                draw_game_over()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            is_running = False
                        if event.key == pygame.K_r:
                            main()  # restart by calling main again
                            return
                pygame.display.update()
                clock.tick(60)
                continue

        # Display lives
        draw_lives()
        draw_score()

        # Event loop
        for event in pygame.event.get():

            # QUIT occurs when you hit the X button on the window
            if event.type == pygame.QUIT:
                is_running = False

            # Press Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Prevents recalling fireball by shooting another early
                    if not fireball_visible:
                        shoot_fireball(player_x, player_y)
                if event.key == pygame.K_LEFT:
                    player_x_change = -6
                if event.key == pygame.K_RIGHT:
                    player_x_change = 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        # Motify player location
        player_x += player_x_change

        # Keep player inside screen
        if player_x <= 5:
            player_x = 5
        if player_x >= 730:
            player_x = 730
        if player_y <= 5:
            player_y = 5
        if player_y >= 520:
            player_y = 520

        player(player_x, player_y)

        # Modify enemy location
        for enemy in range(num_enemies):
            enemy_x[enemy] += enemy_x_change[enemy]

            if enemy_x[enemy] <= 5:
                enemy_x_change[enemy] = enemy_x_change[enemy] * -1
                enemy_y[enemy] += enemy_y_change[enemy]
            if enemy_x[enemy] >= 730:
                enemy_x_change[enemy] = enemy_x_change[enemy] * -1
                enemy_y[enemy] += enemy_y_change[enemy]

            collision = detect_collision(fireball_x, fireball_y, enemy_x[enemy], enemy_y[enemy])
            if collision and fireball_visible:
                fireball_visible = False
                fireball_y = player_y
                score += 100
                success_sound.play()
                trigger_enemy_explosion(enemy_x[enemy] - 32, enemy_y[enemy] - 32)
                enemy_x[enemy] = random.randint(0, 736)
                enemy_y[enemy] = random.randint(50, 200)
            
            # Player hit by enemy
            if not player_invincible:
                player_collision = detect_collision(player_x, player_y, enemy_x[enemy], enemy_y[enemy])
                if player_collision:
                    trigger_player_explosion()
                    lives -= 1
                    enemy_x[enemy] = random.randint(0, 736)
                    enemy_y[enemy] = random.randint(50, 200)

            draw_enemy(enemy_x[enemy], enemy_y[enemy], enemy)
        
        # Enemy explosion
        if explosion_visible:
            screen.blit(enemy_explode_img, (explosion_x, explosion_y))
            explosion_timer += 1
            if explosion_timer >= explosion_duration:
                explosion_visible = False
        
        # Player explosion
        if player_explosion_visible:
            screen.blit(player_explode_img, (player_x - 32, player_y - 32))
            player_explosion_timer += 1
            if player_explosion_timer >= player_explosion_duration:
                player_explosion_visible = False
                # Reset player
                player_x = 368
                player_y = 520

                # Check if game is over
                if lives <= 0:
                    game_over = True
                    mixer.music.stop()
                    game_over_sound.play()

        # Motify fireball location
        if fireball_visible:
            screen.blit(fireball_img, (fireball_x + 16, fireball_y + 10))
            fireball_y -= fireball_y_change
            if fireball_y < 0:
                fireball_visible = False
                fireball_y = player_y

        # Randomly shoot laser
        if not laser_visible:
            laser_timer += 1
            if laser_timer >= laser_interval:
                shooter = random.randint(0, num_enemies - 1)
                laser_x = enemy_x[shooter] + enemy_img[shooter].get_width() // 2 - 5
                laser_y = enemy_y[shooter] + enemy_img[shooter].get_height()
                laser_visible = True
                enemy_shot_sound.play()
                laser_timer = 0
                laser_interval = random.randint(40, 150)

        # Move laser
        if laser_visible:
            screen.blit(laser_img, (laser_x, laser_y + 20))
            laser_y += laser_y_change
            if laser_y > 600:
                laser_visible = False

        # Player hit by laser
        if laser_visible and not player_invincible:
            laser_collision = detect_collision(player_x, player_y, laser_x, laser_y)
            if laser_collision:
                laser_visible = False
                trigger_player_explosion()
                lives -= 1

        # Invincibility timer
        if player_invincible:
            player_invincible_timer += 1
            if player_invincible_timer >= player_invincible_duration:
                player_invincible = False

        # Update screen
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()