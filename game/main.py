import os
import time
import cv2
import math
import pygame
import tensorflow as tf
from player import Player
from obstacle import Obstacle
from utilities.convert_array_to_surface import convert_array_to_surface
from utilities.model_bridge import get_detection_func
from colorama import Fore, Style

print(Fore.YELLOW + "Setting up..." + Style.RESET_ALL)

# define paths
PATHS = {
    "saved_model": os.path.join("Tensorflow", "workspace", "iteration_3", "exported-models", "gesture_detection_model", "saved_model"),
    "label_map": os.path.join("Tensorflow", "workspace", "iteration_3", "annotations", "label_map.pbtxt"),
    "player_assets": os.path.join("game", "assets", "player"),
    "obstacle_asset": os.path.join("game", "assets", "obstacle.png"),
    "bg_asset": os.path.join("game", "assets", "bg.png")
}

# pygame setup
pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
clock = pygame.time.Clock()
running = True

# screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Game"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)

# player setup
PLAYER_START_X = 300
PLAYER_START_Y = 500
player = Player(
    pos_x=PLAYER_START_X, 
    pos_y=PLAYER_START_Y, 
    walking_sprite_paths=[os.path.join(PATHS["player_assets"], "walking", f"player{i}.png") for i in range(1, 4)],
    jumping_sprite_path=os.path.join(PATHS["player_assets"], "jumping", "player4.png"),
    walking_speed=0.5,
    jump_velocity=20,
    jump_height=20,
    jump_gravity=1,
) 
player_group = pygame.sprite.Group()
player_group.add(player)

# obstacle setup
OBSTACLE_START_X = SCREEN_WIDTH+500 # obstacle will start off the screen
OBSTACLE_START_Y = 500
obstacle = Obstacle(
    pos_x=OBSTACLE_START_X,
    pos_y=OBSTACLE_START_Y,
    img_path=PATHS["obstacle_asset"]
)
obstacle_group = pygame.sprite.Group()
obstacle_group.add(obstacle)

# load background
bg = pygame.image.load(PATHS["bg_asset"]).convert()
bg_width = bg.get_width()

# scrolling mechanics and FPS
n_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
scroll = 0
SHIFT = 10
IS_SCROLLING = False
FPS = 60

# detection model setup
detect_best = get_detection_func(PATHS["saved_model"], PATHS["label_map"])

# camera feed setup
detection_class = 0
detection_score = 0
has_reset_hand = True

print(Fore.CYAN + "Connecting to webcam..." + Style.RESET_ALL)
cap = cv2.VideoCapture(0)
print(Fore.GREEN + "Connected to webcam" + Style.RESET_ALL)

ret, feed = cap.read()
detections_surface = convert_array_to_surface(feed)

# time tracker setup
current_time = time.time()
previous_time = time.time()
delta = 0

print("STARTING GAME")

# game loop
while running:

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update delta
    previous_time = current_time
    current_time = time.time()
    delta += current_time - previous_time

    # run detections periodically (otherwise the game becomes really slow)
    if delta > 0.25:
        # reset delta
        delta = 0
        # get camera feed from webcam
        ret, feed = cap.read()
        # get detections
        detection_class, detection_score, feed_with_detections = detect_best(feed)
        # update detection surface
        detections_surface = convert_array_to_surface(feed_with_detections)

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

    # detect for closed
    if int(detection_class) == 1 and detection_score > 0.80:
        # if game has not started, then start game
        if not IS_SCROLLING:
            IS_SCROLLING = True
            player.start_walking()
        # if the game has started, then reset the jump
        if not has_reset_hand:
            has_reset_hand = True

    # detect for palm
    if int(detection_class) == 2 and detection_score > 0.80 and has_reset_hand and IS_SCROLLING:
        # only jump if the game has started and the jump has been reset
        player.start_jumping()
        has_reset_hand = False

    # check if obstacle has passed the screen -> load a new obstacle
    if obstacle.rect.right < 0:
        obstacle_group.remove(obstacle)
        obstacle = Obstacle(
            pos_x=OBSTACLE_START_X,
            pos_y=OBSTACLE_START_Y,
            img_path=PATHS["obstacle_asset"]
        )
        obstacle_group.add(obstacle)

    # render player
    player_group.draw(screen)
    player_group.update()

    # render obstacle
    obstacle_group.draw(screen)
    if IS_SCROLLING: # only move obstacle if scrolling
        obstacle_group.update(SHIFT)

    # render detections
    screen.blit(detections_surface.convert(), (0, 0))

    # check if player has collided with obstacle -> end game
    if player.rect.colliderect(obstacle.rect):
        IS_SCROLLING = False
        player.end_walking()
        player.end_jumping()
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()