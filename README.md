# Dino Game controlled by Gesture Detection

The classic dino game, except its controlled by your hand!

![dino](https://github.com/raj-pulapakura/Dino-Game-controlled-by-Gesture-Detection/assets/87762282/92b7e1e9-918a-4d7a-bc19-5f518aca820c)

## 📌 Overview

This project highlights the intersection of Game Development and Computer Vision technologies, specifically real-time Object Detection.

### Libraries used

- Pygame (to build the game interface)
- TensorFlow (to train the object detection model)
- OpenCV (processing and labelling images).

## 🤗 How it works

### YouTube Game Explanation

I made a YouTube video showing how the game works. Check it out 👇

[![Screenshot 2023-12-14 161047](https://github.com/raj-pulapakura/Dino-Game-controlled-by-Gesture-Detection/assets/87762282/d70803e5-38e0-4ed6-8c8e-c1e43b5f0361)](https://www.youtube.com/watch?v=GvOFWHpD_iY)

### Quick Explanation

- The Object Detection model is trained on two classes: a closed hand and an open palm. 
- When you open your palm, this triggers the dino to jump. To jump again, you need to first reset the dino by closing your hand.

![Group 1](https://user-images.githubusercontent.com/87762282/233251641-56517779-70f4-445e-9060-3eaec3dd661f.png)

## 🛠️ Development processes

The project comprised of three main processes:

1. Image collection and annotation (labelling)
2. Object Detection Model Training
3. Game Integration and Testing

I think I repeated these processes around 5 times before I eventually found the optimal solution. The most difficult part of this project was finding the right balance between speed and accuracy. 

### 🧮 Image collection and annotation

- Initially training images were scraped from the web, however these were often poor quality images.
- Labelling these images was an arduous task, although this was very much relieved with the extremely useful [LabelImg](https://github.com/HumanSignal/labelImg) tool.
- After determining that the project was feasible, I wrote an image collection script to collect images from my webcam. This was largely facilitated by the OpenCV library.
- Eventually I curated a dataset which contained high-quality webcam images, which is ultimately what powered the performance of the Object Detection Model.

### 🎛️ Object Detection Model Training

Training the Object Detection Model was undoubtedly the crux of the project. Each training session took around 3-5 hours.

This part of the project was particularly challenging and insightful, as the model's performance depends on so many factors:
- Data quality
- Model architecture
- Number of training epochs 

Model architectures were sourced from [TensorFlow 2 Detection Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md), which open sources a large range of pretrained object detection architectures ready to be fine-tuned.

I tested 2 model architectures for this project:
- CenterNet MobileNetV2 FPN 512x512 (fast, but extremely inaccurate)
- SSD MobileNet V2 FPNLite 320x320 (relatively slow, decent real-time accuracy)

After 5 trials, I settled on the SSD MobileNet architecture. Although it was slower than the CenterNet architecture, the CenterNet architecture was too simple to fulfil the object detection task.

### 🎮 Game Integration and Testing

The game interface was built using Python (it's incredible that I was able to use a single programming language for the entire project) and the amazing game library [PyGame](https://www.pygame.org/docs).

The game is comprised of two components:
- Camera feed, which was handled by OpenCV.
- Game assets, which are rendered by PyGame.

Integrating the model into the game proved to be rather difficult. The FPS had to carefully tuned so that:
- The game was smooth and playable.
- The model wasn't overburdened, which would have slowed down the game even further.

Also, it was completely infeasible to load every single frame into the object detection model. Thus, the camera feed input was fed periodically into the Object Detection Model, ensuring that the game didn't become slow.

## 🗃️ Project Code Structure

I highly encourage you to dive into the code. Here's a quick navigation guide.

The two main folders are `game` and `Tensorflow`:
- `game` contains the files relating to the dino game implementation such as scripts, classes and assets. 
- `Tensorflow` contains all the code relating to image annotation and model development.

### `game`

- `game/assets`: Contains the images used in the game such as the dino sprite, cactus sprite and restart button icon.

- `game/utilities`: Contains various helper functions used in the game.

- `game/Button.py`, `game/Obstacle.py`, `game/Player.py`: PyGame Classes.

- `game/main.py`: Runs the game.

### `Tensorflow`

- `TensorFlow/models`: [Cloned repository](https://github.com/tensorflow/models) which contains all the code relating to Tensorflow model development including the object detection API.

- `TensorFlow/scripts`: Various scripts used in the model development process.

- `TensorFlow/workspace`: Model development zone; organised into iterations; each iteration contains a README.md file which explains the contents of the iteration folder.
