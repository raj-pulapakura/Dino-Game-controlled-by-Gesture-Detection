import math
import os
import pygame
from player import Player
from obstacle import Obstacle

# pygame setup
pygame.init()
clock = pygame.time.Clock()
RUNNING = True

# screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# player setup
PLAYER_START_X = 300
PLAYER_START_Y = 500
player = Player(
    pos_x=PLAYER_START_X, 
    pos_y=PLAYER_START_Y, 
    walking_sprite_paths=[os.path.join("assets", "player", "walking", f"player{i}.png") for i in range(1, 4)],
    jumping_sprite_path=os.path.join("assets", "player", "jumping", "player4.png"),
    walking_speed=0.2,
    jump_velocity=25,
    jump_height=25,
    jump_gravity=1,
) 
player_group = pygame.sprite.Group()
player_group.add(player)

# obstacle setup
OBSTACLE_START_X = SCREEN_WIDTH+100 # obstacle will start off the screen
OBSTACLE_START_Y = 500
obstacle = Obstacle(
    pos_x=OBSTACLE_START_X,
    pos_y=OBSTACLE_START_Y,
    img_path=os.path.join("assets", "obstacle.png")
)
obstacle_group = pygame.sprite.Group()
obstacle_group.add(obstacle)

# load background
bg = pygame.image.load(os.path.join("assets", "bg.png")).convert()
bg_width = bg.get_width()

# scrolling mechanics and FPS
n_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
scroll = 0
SHIFT = 5
IS_SCROLLING = False
FPS = 60

# game loop
while RUNNING:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # draw scrolling background
    for i in range(n_tiles):
        if i > 0: # this if statement makes the images overlap each other so the scrolling so more smooth
            screen.blit(bg, (i*bg_width-1+scroll, 0))
        else:
            screen.blit(bg, (i*bg_width+scroll, 0))
    
    # scroll background
    if IS_SCROLLING:
        scroll -= SHIFT
        # reset scroll
        if bg_width - abs(scroll) <= 0:
            scroll = -SHIFT

    # event handler
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        IS_SCROLLING = True
        player.start_walking()
    if keys[pygame.K_SPACE] and IS_SCROLLING:
        player.start_jumping()

    # check if obstacle has passed the screen
    if obstacle.rect.right < 0:
        obstacle_group.remove(obstacle)
        obstacle = Obstacle(
            pos_x=OBSTACLE_START_X,
            pos_y=OBSTACLE_START_Y,
            img_path=os.path.join("assets", "obstacle.png")
        )
        obstacle_group.add(obstacle)

    # RENDER
    player_group.draw(screen)
    player_group.update()

    obstacle_group.draw(screen)
    if IS_SCROLLING:
        obstacle_group.update(SHIFT)

    # check if player has collided with obstacle
    if player.rect.colliderect(obstacle.rect):
        IS_SCROLLING = False
        player.end_walking()
        player.end_jumping()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()