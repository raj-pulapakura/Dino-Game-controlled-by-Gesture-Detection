import time
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from colorama import Fore, Style

def _load_model(path_to_saved_model):
    """
    Returns a TensorFlow saved model
    """
    # load saved model
    return tf.saved_model.load(path_to_saved_model)

def _get_category_index(path_to_label_map):
    """
    Returns a label map
    """
    # load label map
    return label_map_util.create_category_index_from_labelmap(path_to_label_map,
                                                                        use_display_name=True)

def get_detection_func(path_to_saved_model, path_to_label_map):
    """
    Returns a function (which is preconfigured with the given model and label_map) that gets detections from an image
    """
    # load model can category index
    model = _load_model(path_to_saved_model)
    category_index = _get_category_index(path_to_label_map)

    # create function that uses above model and category index to make detections
    def _detect_best(image):
        """
        Returns detection class with the highest score, the score and the image with the detection
        """
        # get detection function
        detect_fn = model.signatures["serving_default"]
        # convert to input tensor
        input_tensor = tf.convert_to_tensor(np.expand_dims(image, 0), dtype=tf.uint8)
        # get detections
        detections = detect_fn(input_tensor)
        # # convert to numpy arrays, and take index [0] to remove the batch dimension.
        num_detections = int(detections.pop('num_detections'))
        # apply detections to a copy of the image
        image_with_detections = image.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_with_detections,
            (detections['detection_boxes'][0, :num_detections]).numpy(),
            (detections['detection_classes'][0, :num_detections]).numpy().astype(np.int64),
            (detections['detection_scores'][0, :num_detections]).numpy(),
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=1,
            min_score_thresh=.80,
            agnostic_mode=False
        )
        return detections["detection_classes"][0][0], detections["detection_scores"][0][0], image_with_detections
    # return this function    
    return _detect_best