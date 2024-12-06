"""
This script is designed to process and organize image and label data for training deep learning models.
It includes functionality to combine image and label files from separate train, validation, and test
folders into unified directories, and then splits the data into new train, validation, and test sets
based on specified ratios.

Functions:
-----------
1. combine_data(data_dir, image_dir, label_dir):
   - Combines images and corresponding label files from 'train', 'valid', and 'test' subdirectories
     into unified "all_images" and "all_labels" directories for easier processing.

2. split_data(image_dir, label_dir, output_dir, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
   - Splits the combined image and label data into new train, validation, and test sets based on the
     specified ratios. Ensures each image has a corresponding label and organizes the data into
     output directories.

Parameters:
-----------
data_dir : str
    Path to the main data directory containing subdirectories for 'train', 'valid', and 'test' data.
image_dir : str
    Path to the directory where all combined images will be stored.
label_dir : str
    Path to the directory where all combined labels will be stored.
output_dir : str
    Path to the directory where the newly split train, validation, and test data will be saved.
train_ratio : float
    Proportion of the data to allocate to the training set (default is 0.6).
val_ratio : float
    Proportion of the data to allocate to the validation set (default is 0.2).
test_ratio : float
    Proportion of the data to allocate to the test set (default is 0.2).

Usage:
------
1. Ensure the directory structure has 'train', 'valid', and 'test' subdirectories, each containing
   'images' and 'labels' folders with corresponding files.
2. Run `combine_data` to consolidate all images and labels into unified folders.
3. Run `split_data` to split the data into new train, validation, and test sets based on desired ratios.

Note:
-----
- The script ensures every image has a corresponding label during the splitting process.
- Warnings are printed for images without matching label files during the combining step.
"""

import os
import shutil
from sklearn.model_selection import train_test_split #type: ignore

# Paths
data_dir = "data/drowning"
image_dir = os.path.join(data_dir, "all_images")
label_dir = os.path.join(data_dir, "all_labels")

# Combine all images and labels into one folder
def combine_data(data_dir, image_dir, label_dir):
    """
    Combines the images and labels into 2 folders in the same directory
    """
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    # Subdirectories to process
    subdirs = ["train", "valid", "test"]

    for subdir in subdirs:
        sub_image_dir = os.path.join(data_dir, subdir, "images")
        sub_label_dir = os.path.join(data_dir, subdir, "labels")

        for image_fname in os.listdir(sub_image_dir):
            # Copy image
            shutil.copy(os.path.join(sub_image_dir, image_fname), os.path.join(image_dir, image_fname))

            # Match corresponding label file
            base_name = os.path.splitext(image_fname)[0]  # Get the base name (without extension)
            label_fname = f"{base_name}.txt"  # Assuming labels have a `.txt` extension
            label_path = os.path.join(sub_label_dir, label_fname)

            if os.path.exists(label_path):
                shutil.copy(label_path, os.path.join(label_dir, label_fname))
            else:
                print(f"Warning: Label file not found for image {image_fname}")

# Combine all data
combine_data(data_dir, image_dir, label_dir)

# Split into new train, validation, and test sets
def split_data(image_dir, label_dir, output_dir, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    """
    Split the data into desired ratios
    """
    # Ensure ratios add up to 1
    assert train_ratio + val_ratio + test_ratio == 1, "Ratios must sum to 1."

    # Create output directories
    splits = ["train", "valid", "test"]
    for split in splits:
        os.makedirs(os.path.join(output_dir, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, "labels"), exist_ok=True)

    # Get all filenames
    image_files = sorted(os.listdir(image_dir))
    label_files = sorted(os.listdir(label_dir))

    # Match image and label files by base name
    image_base_names = [os.path.splitext(fname)[0] for fname in image_files]
    label_base_names = [os.path.splitext(fname)[0] for fname in label_files]

    # Ensure every image has a corresponding label
    matched_files = [
        (image_files[i], f"{image_base_names[i]}.txt")
        for i in range(len(image_files))
        if image_base_names[i] in label_base_names
    ]

    # Extract matched filenames
    image_files = [image for image, label in matched_files]
    label_files = [label for image, label in matched_files]

    # Split filenames
    train_images, temp_images, train_labels, temp_labels = train_test_split(
        image_files, label_files, test_size=val_ratio + test_ratio, random_state=42
    )
    val_images, test_images, val_labels, test_labels = train_test_split(
        temp_images, temp_labels, test_size=test_ratio / (val_ratio + test_ratio), random_state=42
    )

    # Helper to move files
    def move_files(file_list, source_dir, target_dir):
        for fname in file_list:
            shutil.move(os.path.join(source_dir, fname), os.path.join(target_dir, fname))

    # Move files into respective folders
    move_files(train_images, image_dir, os.path.join(output_dir, "train", "images"))
    move_files(train_labels, label_dir, os.path.join(output_dir, "train", "labels"))

    move_files(val_images, image_dir, os.path.join(output_dir, "valid", "images"))
    move_files(val_labels, label_dir, os.path.join(output_dir, "valid", "labels"))

    move_files(test_images, image_dir, os.path.join(output_dir, "test", "images"))
    move_files(test_labels, label_dir, os.path.join(output_dir, "test", "labels"))

    print(f"Data split completed:")
    print(f"Train: {len(train_images)} images")
    print(f"Validation: {len(val_images)} images")
    print(f"Test: {len(test_images)} images")

# Perform the split
output_dir = "data/drowning_resplit"
split_data(image_dir, label_dir, output_dir)
