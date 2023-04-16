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

## Final Thoughts

This model performs the best out of all the previous models. Saying this, I believe it is ready for exporting and integration into the game.

This process of iteration and testing out different model configurations has been a valuable learning experience for me. I now hold a deeper appreciation for the classical AI saying: "Garbage in, Garbage out". This cliche truly does hold, as low-quality data leads to undesirable performance, and high-quality data and annotation leads to prolific performance.

However, I believe the most important lesson I have gained from this experience is to not give up despite the challenges I may encounter. When the Iteration 2 Model 1 performance turned out to be bad, I panicked and thought that I would never achieve a higher performance than the prototype model. It took a moment of self-reflection and motivation to continue persisting with the training process, until I finally reached a desirable model performance.

Anyways, now that the training process is finally over, let's integrate this model into the game!