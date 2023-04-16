# Iteration 1

This iteration serves as a prototyping/proof of concept stage to test if this project is feasible.

## Model 1: Configuration

In this iteration a single model was created with the following characteristics:
- Model Type: SSD MobileNet V2 FPNLite 320x320 ([Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md))
- Classes: palm, closed
- Training samples per class: 9
- Testing samples per class: 1
- Number of steps trained for: 1000
- Batch size: 8

For more information about the model's configuration, go to ```models/model_1/pipeline.config``` which is located in this directory.

## Model 1: Performance

### Test dataset performance

Here are the results for the test dataset evaluation:
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.700
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = -1.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.700
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.700
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.700
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.700
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = -1.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = -1.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.700
```

As you can see, the model performed fairly well, given that only 9 training images were provided per class.

### Real-time performance

The model also performed decently well during real-time detection. It was able to generally distinguish between the closed hand and open palm.

## Next iteration...

Now that I know that this project is feasible, I can expand on this model and try to reach new heights of performance.

In the next iteration, I will use the same model architecture and configuration, however I will collect more samples for training and testing to see if it improves the performance of the model.