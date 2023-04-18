
import cv2
import pygame


def convert_array_to_surface(feed):
    """
    Converts a numpy array to a pygame surface with necessary transformations
    """
    feed = cv2.cvtColor(feed,cv2.COLOR_BGR2RGB)
    feed = pygame.pixelcopy.make_surface(feed)
    feed = pygame.transform.flip(feed, flip_x=True, flip_y=False)
    feed = pygame.transform.rotate(feed, 90)
    feed = pygame.transform.scale_by(feed, 0.5)
    return feed