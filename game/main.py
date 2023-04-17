import os
import time
import cv2
import math
import pygame
from player import Player
from obstacle import Obstacle
from model_bridge.get_detections import load_model, get_category_index, get_detections
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

# detection model setup
model = load_model(PATHS["saved_model"])
category_index = get_category_index(PATHS["label_map"])

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

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

# camera feed setup
def convert_camera_feed_to_surface(feed):
    feed = cv2.cvtColor(feed,cv2.COLOR_BGR2RGB)
    feed = pygame.pixelcopy.make_surface(feed)
    feed = pygame.transform.flip(feed, flip_x=True, flip_y=False)
    feed = pygame.transform.rotate(feed, 90)
    feed = pygame.transform.scale_by(feed, 0.5)
    return feed
detection_class = 0
detection_score = 0
print(Fore.CYAN + "Connecting to webcam..." + Style.RESET_ALL)
cap = cv2.VideoCapture(0)
print(Fore.GREEN + "Connected to webcam" + Style.RESET_ALL)
ret, feed = cap.read()
detections_surface = convert_camera_feed_to_surface(feed)

print("STARTING GAME")

current_time = time.time()
previous_time = time.time()
delta = 0

"""
2 = palm
1 = closed
"""

has_reset_hand = True

# game loop
while running:

    previous_time = current_time
    current_time = time.time()
    delta += current_time - previous_time

    # run detections periodically (otherwise the game becomes really slow)
    if delta > 0.25:
        delta = 0
        # get camera feed from webcams
        ret, feed = cap.read()
        # get detections
        detection_class, detection_score, feed_with_detections = get_detections(model, category_index, feed)
        print(f"class: {detection_class} score: {detection_score}")
        # update detection surface
        detections_surface = convert_camera_feed_to_surface(feed_with_detections)

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    if int(detection_class) == 2 and detection_score > 0.90 and has_reset_hand and IS_SCROLLING:
        player.start_jumping()
        has_reset_hand = False

    if int(detection_class) == 1 and detection_score > 0.90 and not has_reset_hand:
        has_reset_hand = True 

    # check if obstacle has passed the screen -> load a new obstacle
    if obstacle.rect.right < 0:
        obstacle_group.remove(obstacle)
        obstacle = Obstacle(
            pos_x=OBSTACLE_START_X,
            pos_y=OBSTACLE_START_Y,
            img_path=PATHS["obstacle_asset"]
        )
        obstacle_group.add(obstacle)

    # RENDER
    # player
    player_group.draw(screen)
    player_group.update()

    # obstacle
    obstacle_group.draw(screen)
    if IS_SCROLLING: # only move obstacle if scrolling
        obstacle_group.update(SHIFT)

    # detections
    screen.blit(detections_surface.convert(), (0, 0))
    pygame.display.update()

    # check if player has collided with obstacle -> end game
    if player.rect.colliderect(obstacle.rect):
        IS_SCROLLING = False
        player.end_walking()
        player.end_jumping()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()