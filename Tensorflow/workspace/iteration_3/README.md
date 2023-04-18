# Iteration 3

This iteration uses the same model configuration as Iteration 2 Model 2 but includes higher quality training data (better annotations and precise images). I removed the training samples that were low-quality (blurry, distorted, dark). Further, I focused on taking images from the webcam where my hand was in various positions and configurations, so the model would generalise better.

## Model 1: Configuration

- Model Type: SSD MobileNet V2 FPNLite 320x320 ([Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md))
- Classes: palm, closed
- Training samples per class: 35-37
- Testing samples per class: 4-5
- Number of steps trained for: 5000
- Batch size: 8

For more information about the model's configuration, go to ```models/model_1/pipeline.config``` which is located in this directory.

## Model 1: Performance

### Test dataset performance

This model performed exceedingly well on the test data.

Here are the results for the test dataset evaluation:
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.871
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.767
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.919
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.767
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.925
```

### Real-time detection

The model performed desirably well during real time detection. It was able to confidently (90%-100%) distinguish between a closed hand and an open palm.

Let's integrate this into the game!

## Model 2: Configuration

After integrating Model 1 into the game, I was hoping to increase the speed at which detections were made. So I attempted to train a model with the CenterNet architecture provided by Tensorflow which has a speed of 6 ms (compared to SSD's 22 ms) according to Tensorflow Model Zoo. However, this didn't go as planned and the model ended up performing terribly. Like absolutely terrible.

- Model Type: CenterNet MobileNetV2 FPN 512x512 ([Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md))
- Classes: palm, closed
- Training samples per class: 35-37
- Testing samples per class: 4-5
- Number of steps trained for: 5000
- Batch size: 8

For more information about the model's configuration, go to ```models/model_2/pipeline.config``` which is located in this directory.

### Test dataset performance

Here are the results for the test dataset evaluation:
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.010
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.027
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.019
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.070
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.070
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.087
```

As you can see, the precision and recall of the model aren't too great.

### Real-time detection

The model performed atrociously during real-time detection. It kept mislabelling other items in the room as a palm. It would occasionally be able to detect my palm with a confidence of around 60%, however it was not able to detection my closed hand at all.

Let's try a different architecture!
