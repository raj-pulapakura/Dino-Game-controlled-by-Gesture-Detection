# Side-Scroller-Game-Gesture-Detection
The classic chrome dino game but you don't use the keyboard! Use your hand movements to make the dino jump!

## Overview

This project combines the simplicity of the chrome dino game with the complexity of an object detection model.

![Screenshot 2023-04-20 131226](https://user-images.githubusercontent.com/87762282/233249112-ad933c3d-810a-49ff-bcb3-03e8bc98c9ec.png)

This project uses libraries such as Pygame (game development), Tensorflow (model development) and OpenCV (computer vision).

## How it works

I made a YouTube video which explains the game mechanics ->

If you want a quick explanation:

The object detection model is trained on two classes: a closed hand and an open palm. To jump, open your palm. The detection model will detect this and make the dino jump. Then, you must reset the jump by closing your hand, after which you can jump again by opening your palm.

palm = JUMP, closed = RESET

![Group 1](https://user-images.githubusercontent.com/87762282/233251641-56517779-70f4-445e-9060-3eaec3dd661f.png)

## Project Code Structure

If you want to dive into the code for this project, here's a quick explanation of how to navigate through it.

The two main folders are *game* and *Tensorflow*. *game* contains the files relating to the dino game implementation such as scripts, classes and assets. *Tensorflow* contains all the code relating to model development.

### *game*

***assets***: this folder contains the images used in the game such as the dino sprite, cactus sprite and restart button icon.

***utilities***: this folder contains various helper functins used in the game

***Button.py, Obstacle.py, Player.py***: classes used in the game

***main.py***: the code for the main game loop and integration of the model

### *Tensorflow*

***models***: [cloned repository](https://github.com/tensorflow/models) which contains all the code relating to Tensorflow model development including the object detection API

***scripts***: various scripts used in the model development process

***workspace***: model development zone; organised into iterations; each iteration contains a README.md file which explains the contents of the iteration folder

## Detection Model

The final detection model used in the game is the [SSD MobileNet V2 FPNLite 320x320](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md). I chose this model as it is fast and provides decent performance in real time detection.
