import os
import sys
import time
import cv2
import pygame
from player import Player
from obstacle import Obstacle
from button import Button
from utilities.convert_array_to_surface import convert_array_to_surface
from utilities.model_bridge import get_detection_func
from colorama import Fore, Style

# SETUP ------------------------------------------------------------------------------------------------

print(Fore.YELLOW + "Setting up..." + Style.RESET_ALL)

# define paths
PATHS = {
    "saved_model": os.path.join("Tensorflow", "workspace", "iteration_3", "exported-models", "gesture_detection_model", "saved_model"),
    "label_map": os.path.join("Tensorflow", "workspace", "iteration_3", "annotations", "label_map.pbtxt"),
    "assets": os.path.join("game", "assets"),
}

# detection model setup
detect_best = get_detection_func(PATHS["saved_model"], PATHS["label_map"])
detection_class = 0
detection_score = 0
has_reset_hand = True

# camera feed setup
print(Fore.CYAN + "Connecting to webcam..." + Style.RESET_ALL)
cap = cv2.VideoCapture(0)
print(Fore.GREEN + "Connected to webcam" + Style.RESET_ALL)
ret, feed = cap.read()
detections_surface = convert_array_to_surface(feed)

# pygame setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 30)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
clock = pygame.time.Clock()

# screen setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Game"
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)

# --------------------------------------------------------------------------------------------------

# continually running loop (only stops when person clicks exit)
while True:

    # player setup
    PLAYER_START_X = 300
    PLAYER_START_Y = 500
    player = Player(
        pos_x=PLAYER_START_X, 
        pos_y=PLAYER_START_Y, 
        walking_sprite_paths=[
            os.path.join(PATHS["assets"], "dinorun0000.png"),
            os.path.join(PATHS["assets"], "dinorun0001.png"),
        ],
        jumping_sprite_path=os.path.join(PATHS["assets"], "dinoJump0000.png"),
        walking_speed=0.6,
        jump_velocity=20,
        jump_height=20,
        jump_gravity=1,
    ) 
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # obstacle setup
    OBSTACLE_START_X = SCREEN_WIDTH+100 # obstacle will start off the screen
    OBSTACLE_START_Y = 520
    obstacle = Obstacle(
        pos_x=OBSTACLE_START_X,
        pos_y=OBSTACLE_START_Y,
        img_path=os.path.join(PATHS["assets"], "cactusSmall0000.png")
    )
    obstacle_group = pygame.sprite.Group()
    obstacle_group.add(obstacle)

    # restart button setup
    restart_button = Button(
        x=SCREEN_WIDTH-60, 
        y=60, 
        scale=0.08, 
        image_normal=os.path.join(PATHS["assets"], "undo-arrow.png"),
        image_hover=os.path.join(PATHS["assets"], "undo-arrow-hover.png")
    )

    # game mechanics
    shift = 10
    FPS = 60
    score = 0
    is_scrolling = False
    is_playing = True
    has_collided = False

    # time tracker setup
    current_time = time.time()
    previous_time = time.time()
    delta = 0

    # text surfaces
    start_surface = my_font.render('Show closed hand to start', True, (0, 0, 0))
    end_surface = my_font.render("Game Over", True, (0, 0, 0))

    # -----------------------------------------------------------------------------------------------

    # game loop (stops when player collides with obstacle)
    while is_playing:

        screen.fill((255, 255, 255))

        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.rect.collidepoint(mouse_pos):
                    is_playing = False

        # DETECTIONS ------------------------------------------------------------------------------------------------

        # update delta
        previous_time = current_time
        current_time = time.time()
        delta += current_time - previous_time

        # run detections periodically (otherwise the game becomes really slow)
        if delta > 0.1 and not player.is_jumping:
            # reset delta
            delta = 0
            # get camera feed from webcam
            ret, feed = cap.read()
            # get detections
            detection_class, detection_score, feed_with_detections = detect_best(feed)
            # update detection surface
            detections_surface = convert_array_to_surface(feed_with_detections)

        # detect for closed
        if int(detection_class) == 1 and detection_score > 0.80 and not has_collided:
            # if the game hasn't strated yet, start the game with walking
            if not is_scrolling:
                is_scrolling = True
                player.start_walking()
            # if the game has started, then reset the jump
            if not has_reset_hand:
                has_reset_hand = True

        # detect for palm
        if int(detection_class) == 2 and detection_score > 0.80 and has_reset_hand and not has_collided:
            # only jump if the game has started and the jump has been reset
            player.start_jumping()
            has_reset_hand = False

        # RENDER --------------------------------------------------------------------------------------------------------

        # render obstacle
        obstacle_group.draw(screen)
        if is_scrolling: # only move obstacle if scrolling
            obstacle_group.update(shift)

        # render player
        player_group.draw(screen)
        player_group.update()

        # render detections
        screen.blit(detections_surface.convert(), (0, 0))

        # render text
        if not is_scrolling:
            if has_collided:
                screen.blit(end_surface, (400, 60))
            else:
                screen.blit(start_surface, (400, 60))

        # render restart button
        restart_button.process()
        screen.blit(restart_button.surface, restart_button.rect)

        # render score
        screen.blit(my_font.render(str(score), True, (0, 0, 0)), (SCREEN_WIDTH-100, SCREEN_HEIGHT-50))

        # CHECKS ------------------------------------------------------------------------------------------------------

        # check if obstacle has passed the screen -> load a new obstacle 
        if obstacle.rect.right < 0:
            obstacle_group.remove(obstacle)
            obstacle = Obstacle(
                pos_x=OBSTACLE_START_X,
                pos_y=OBSTACLE_START_Y,
                img_path=os.path.join(PATHS["assets"], "cactusSmall0000.png")
            )
            obstacle_group.add(obstacle)

        # check if player has collided with obstacle -> end game
        if player.rect.colliderect(obstacle.rect):
            is_scrolling = False
            has_collided = True
            player.end_walking()
            player.end_jumping()

        # update scroll and shift
        if is_scrolling and not has_collided:
            score += 1

        if score == 200:
            shift += 1
        if score == 400:
            shift += 1
        if score == 800:
            shift += 2
        if score == 1600:
            shift += 2
        if score == 3200:
            shift += 3

        pygame.display.flip()
        clock.tick(FPS)