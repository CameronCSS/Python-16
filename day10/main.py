"""
Day 10 challenge is all about using pygame to make a game!
This is going to be a real fun one!
"""
# Have to use pygame-ce since pygame is not available for python 3.14
import pygame
import os

cwd = os.getcwd()
images_path = os.path.join(cwd, 'images')

def main():
    """
    Main game logic will go here
    """
    # Initilize the game
    pygame.init()
    
    # Create the game screen
    screen = pygame.display.set_mode((800,600))
    
    # Title and Icon
    pygame.display.set_caption("Space Invaders")
    # Icon
    icon = pygame.image.load(os.path.join(images_path, 'ufo.png'))
    pygame.display.set_icon(icon)
    # Player
    player_img = pygame.image.load(os.path.join(images_path, 'ship.png'))
    player_x = 368
    player_y = 520


    def player(x, y):
        """
        Draws the player image onto the screen
        """
        screen.blit(player_img, (x, y))

    # Game loop
    is_running = True
    while is_running:
        screen.fill((3,45,47))

        for event in pygame.event.get():
            # QUIT occurs when you hit the X button on the window
            if event.type == pygame.QUIT:
                is_running = False
        player(player_x, player_y)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()