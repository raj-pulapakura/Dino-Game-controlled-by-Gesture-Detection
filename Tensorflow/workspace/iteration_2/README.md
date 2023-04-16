# Iteration 2

This iteration uses the same model configuration as the previous iteration but includes more training and test data. Image samples were collected from the internet as well as from my webcam.

## Model 1: Configuration

- Model Type: SSD MobileNet V2 FPNLite 320x320 ([Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md))
- Classes: palm, closed
- Training samples per class: 31
- Testing samples per class: 4
- Number of steps trained for: 1000
- Batch size: 8

For more information about the model's configuration, go to ```models/model_1/pipeline.config``` which is located in this directory.

## Model 1: Performance

### Test dataset performance

To my dismay, this model generally performed worse than the Iteration 1 model.

Here are the results for the test dataset evaluation:
```
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.598
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.947
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.522
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.504
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.544
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.562
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.662
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.675
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.550
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.688
```

### Real-time performance

Real-time performance also suffered quite a bit. The model was not able to confidently distinguish between the closed hand and open palm, with a confidence percentage ranging from about 50% to 60%. Further, the model was not able to detect my hand when I put it in front of my face, which suggests that images with more variation would augment the model's performance.

## Areas of Improvement

There are several things I can do to improve the model's performance:

- Increase the number of training steps
- Collect and annotate higher-quality data
- Change the model architecture
- Change the configuration (e.g. batch size) of the model

In the next model I will use the same model configuration and training/testing samples, but I will increase the number of training steps to see if this improves the performance.

## Model 2: Configuration

- Model Type: SSD MobileNet V2 FPNLite 320x320 ([Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md))
- Classes: palm, closed
- Training samples per class: 31
- Testing samples per class: 4
- Number of steps trained for: 5000
- Batch size: 8

Note that this model uses 5000 training steps while the previous model only used 1000.

For more information about the model's configuration, go to ```models/model_2/pipeline.config``` which is located in this directory.

## Model 2: Performance

### Test dataset performance

This model performed much better than the previous model on the test samples.

Here are the results for the test dataset evaluation:
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.860
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.851
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.863
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.875
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.850
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.863
```

Increasing the number of training steps improved the precision and recall of the model.

### Real-time performance

Despite the increase in performance on the test dataset, the model did show difficulty in differentiating between my hand and the other objects in the room (e.g. clock) during real-time detection. This is most likely due to poor training data.

## Next iteration...

In the next iteration I will focus on providing higher quality training images to the model as well as images that include different objects so the model can generalise better.