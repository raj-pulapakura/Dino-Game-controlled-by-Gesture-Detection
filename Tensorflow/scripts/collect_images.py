"""
Collects images and partitions them into training and testing datasets
"""

import argparse
import random
import cv2
import os
import time
import uuid
import shutil
from colorama import Fore, Style

def get_arguments():
    """
    Returns arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images_dir", help="Parent directory to store images", type=str)
    parser.add_argument("-tr", "--train_dir", help="Directory to store images for training dataset (should be inside images_dir)", type=str)
    parser.add_argument("-te", "--test_dir", help="Directory to store images for test dataset (should be inside images_dir)", type=str)
    parser.add_argument("-l", "--labels", help="Labels to collect (separated by comma)", type=str)
    parser.add_argument("-n", "--imgs_per_class", help="Number of images to collect per label", type=int)
    parser.add_argument("-ts", "--test_size", help="Test partition percentage", type=float)
    args = parser.parse_args()
    images_dir = args.images_dir
    train_dir = args.train_dir
    test_dir = args.test_dir
    labels = args.labels.split(",")
    imgs_per_class = args.imgs_per_class
    test_size = args.test_size
    return images_dir, train_dir, test_dir, labels, imgs_per_class, test_size

def create_temp_dir(images_dir):
    """
    Create temporary directory to store collected images
    """
    path = os.path.join(images_dir, "collected")
    if not os.path.exists(path):
        os.mkdir(path)

    return path

def create_label_dirs(images_dir, labels):
    """
    Create directories for each label (if they do not already exist)
    """
    for label in labels:
        path = os.path.join(images_dir, label)
        print(f"\t{path}")
        if not os.path.exists(path):
            os.mkdir(path)

def create_train_test_dirs(train_dir, test_dir):
    """
    Creates train and test dirs if they do not already exist
    """
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

def collect_images(images_dir, labels, imgs_per_class):
    """
    Collects images using webcam
    """
    print(Fore.CYAN + "COLLECTING IMAGES FROM WEBCAM:")
    print(Fore.RED + "Connecting to webcam")
    cap = cv2.VideoCapture(0)
    print(Fore.GREEN + "Connected to webcam" + Style.RESET_ALL)

    img_count = 0
    total_imgs = len(labels) * imgs_per_class

    current_label_idx = 0
    current_label_img_count = 0
    printed_label = False

    previous = time.time()
    delta = 0

    while img_count < total_imgs:
        # show frame continuously
        _, frame = cap.read()
        cv2.imshow("frame", frame)
        
        # get new time delta
        current = time.time()
        delta += (current-previous)
        previous = current
            
        # check if we should go to the next label
        if current_label_img_count == imgs_per_class:
            current_label_img_count = 0
            current_label_idx+=1
            printed_label = False
        
        # print current label
        if not printed_label:
            print(f"Collecting images for {labels[current_label_idx]}")
            printed_label=True
        
        # if delta is greater than 3 (3 seconds has passed), then save frame
        if delta > 3:
                
            # save frame
            print(f"\tSaving image {current_label_img_count} for {labels[current_label_idx]}")
            path = os.path.join(images_dir, labels[current_label_idx], f"{labels[current_label_idx]}.{uuid.uuid1()}.jpg")
            cv2.imwrite(path, frame)
            print("\tSaved")
            # increment stuff
            current_label_img_count+=1
            img_count+=1
            # reset delta
            delta = 0
        
        if cv2.waitKey(10) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def partition_into_train_and_test(images_dir, train_dir, test_dir, labels, test_size):
    """
    Separate collected samples into training and testing directories with shuffling
    """
    print(Fore.CYAN + "SEPARATING COLLECTED SAMPLES INTO TRAIN AND TEST DIRECTORIES:" + Style.RESET_ALL)
    time.sleep(1)
    for label in labels:
        label_path = os.path.join(images_dir, label)
        samples = os.listdir(label_path)
        # shuffling
        random.shuffle(samples)
        # getting number of test samples
        n_test = max(1, round(len(samples) * test_size))
        # getting train and test samples
        test_samples = samples[:n_test]
        train_samples = samples[n_test:]
        # saving samples in respective directories
        print(Fore.BLUE + f"Moving {label} samples" + Style.RESET_ALL)
        time.sleep(1)
        print(f"\tMoving test samples ({n_test})")
        for s in test_samples:
            src_path = os.path.join(label_path, s)
            dst_path = os.path.join(test_dir, s)
            print(f"\t\t{s}")
            shutil.move(src_path, dst_path)

        print(f"\tMoving train samples ({len(samples)-n_test})")
        for s in train_samples:
            src_path = os.path.join(label_path, s)
            dst_path = os.path.join(train_dir, s)
            print(f"\t\t{s}")
            shutil.move(src_path, dst_path)

def remove_temp_dir(dir):
    """
    Removes temporary directory for collected images as images have now been partitioned into train and test
    """
    shutil.rmtree(dir)

def main():

    images_dir, train_dir, test_dir, labels, imgs_per_class, test_size = get_arguments()
    collected_imgs_dir = create_temp_dir(images_dir)
    print(Fore.CYAN + "CREATING DIRECTORIES" + Style.RESET_ALL)
    create_label_dirs(collected_imgs_dir, labels)
    create_train_test_dirs(train_dir, test_dir)
    collect_images(collected_imgs_dir, labels, imgs_per_class)
    partition_into_train_and_test(collected_imgs_dir, train_dir, test_dir, labels, test_size)
    remove_temp_dir(collected_imgs_dir)

main()