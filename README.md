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

