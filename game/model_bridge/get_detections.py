import time
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from colorama import Fore, Style

def load_model(path_to_saved_model):
    print(Fore.YELLOW + "Loading model...", end="")
    start_time = time.time()
    # load saved model
    model = tf.saved_model.load(path_to_saved_model)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f" Done! Took {elapsed_time} seconds" + Style.RESET_ALL)
    return model

def get_category_index(path_to_label_map):
    # load label map
    category_index = label_map_util.create_category_index_from_labelmap(path_to_label_map,
                                                                        use_display_name=True)
    return category_index

def get_detections(model, category_index, image):
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
    # detections = {key: value[0, :num_detections].numpy()
    #             for key, value in detections.items()}
    # detections['num_detections'] = num_detections

    # # detection_classes should be ints.
    # detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

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

