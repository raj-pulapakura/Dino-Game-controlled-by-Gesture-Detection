# 🦖 Dino Game controlled by Gesture Detection

The classic dino game, except its controlled by your hand!

![dino](https://github.com/raj-pulapakura/Dino-Game-controlled-by-Gesture-Detection/assets/87762282/92b7e1e9-918a-4d7a-bc19-5f518aca820c)

## 📌 Overview

This project highlights the intersection of game development and computer vision technologies, specifically real-time object detection.

### Libraries used

- Pygame (to build the game interface)
- TensorFlow (to train the object detection model)
- OpenCV (processing and labelling images).

## 🤗 How it works

### YouTube Game Explanation

I made a YouTube video showing how the game works. Check it out 👇

[![Screenshot 2023-12-14 161047](https://github.com/raj-pulapakura/Dino-Game-controlled-by-Gesture-Detection/assets/87762282/d70803e5-38e0-4ed6-8c8e-c1e43b5f0361)](https://www.youtube.com/watch?v=GvOFWHpD_iY)

### Quick Explanation

- The object detection model is trained on two classes: a closed hand and an open palm. 
- When you open your palm, this triggers the dino to jump. To jump again, you need to first reset the dino by closing your hand.

![Group 1](https://user-images.githubusercontent.com/87762282/233251641-56517779-70f4-445e-9060-3eaec3dd661f.png)

## 🛠️ Development process

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
