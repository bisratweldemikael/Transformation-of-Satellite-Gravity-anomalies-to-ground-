# -*- coding: utf-8 -*-
"""datapreparation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_lcbK5_RQmcgnLrXwAQBPAFLZBGpETt5
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install rasterio

from google.colab.patches import cv2_imshow
import rasterio
from rasterio import warp
from rasterio.enums import Resampling
import numpy as np
import cv2
import matplotlib.pyplot as plt

def align_geotiff_images(image1_path, image2_path):
    with rasterio.open(image1_path) as src1, rasterio.open(image2_path) as src2:
        image1, transform1 = src1.read(), src1.transform
        image2, transform2 = src2.read(), src2.transform

        image2_aligned, transform2_aligned = warp.reproject(
            image2,
            np.empty_like(image1),
            src_transform=transform2,
            dst_transform=transform1,
            src_crs=src2.crs,
            dst_crs=src1.crs,
            resampling=Resampling.bilinear
        )

        image1_uint8 = (image1 / image1.max() * 255).astype(np.uint8)
        image2_aligned_uint8 = (image2_aligned / image2_aligned.max() * 255).astype(np.uint8)

        return image1_uint8, image2_aligned_uint8

# Example usage
image1_path = "/content/drive/MyDrive/aligned_image2_with_white_pixels.tif"
image2_path = "/content/drive/MyDrive/groundhighresolution.tif"

aligned_image1, aligned_image2 = align_geotiff_images(image1_path, image2_path)

# Display the aligned images using matplotlib
plt.figure(figsize=(8, 8))

# Transpose the image data if necessary
aligned_image1 = aligned_image1.transpose(1, 2, 0)
aligned_image2 = aligned_image2.transpose(1, 2, 0)

plt.subplot(1, 2, 1)
plt.imshow(aligned_image1)
plt.title("Aligned Image 1")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(aligned_image2)
plt.title("Aligned Image 2")
plt.axis('off')

plt.show()

import cv2
import numpy as np
import os

def is_patch_entirely_white(patch):
    # Check if all pixels in the patch are white
    return np.all(patch == 255)

def crop_and_save_non_white_patches(aligned_image1, aligned_image2, side_length, output_folder, label):
    height, width, _ = aligned_image1.shape

    for i in range(height // side_length):
        for j in range(width // side_length):
            # Calculate the coordinates for cropping
            start_row = i * side_length
            end_row = start_row + side_length
            start_col = j * side_length
            end_col = start_col + side_length

            # Crop patches
            patch1 = aligned_image1[start_row:end_row, start_col:end_col]
            patch2 = aligned_image2[start_row:end_row, start_col:end_col]

            # Check if the patch is entirely white
            if not is_patch_entirely_white(patch1):
                # Create a folder if it doesn't exist
                folder_path = os.path.join(output_folder, f'label_{label}', f'patch_{i}_{j}')
                os.makedirs(folder_path, exist_ok=True)

                # Save the patches in the folder
                cv2.imwrite(os.path.join(folder_path, 'patch1.jpg'), patch1)
                cv2.imwrite(os.path.join(folder_path, 'patch2.jpg'), patch2)

                # Save spatial coordinates of the patch
                with open(os.path.join(folder_path, 'coordinates.txt'), 'w') as f:
                    f.write(f"start_row: {start_row}\nend_row: {end_row}\nstart_col: {start_col}\nend_col: {end_col}")

# Example usage
# Set the side length of the square patches
side_length = 256  # Adjust as needed

# Set the output folder and label
output_folder = "croped_patches"
label = "some_label"

# Crop and save non-white patches for aligned_image1 and aligned_image2
crop_and_save_non_white_patches(aligned_image1, aligned_image2, side_length, output_folder, label)

import os
from PIL import Image

def concatenate_images(image1_path, image2_path, output_path):
    # Open the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Verify that both images have the same dimensions
    if image1.size != image2.size:
        raise ValueError("Both images must have the same dimensions.")

    # Create a new image with double width
    new_width = image1.width + image2.width
    new_height = image1.height
    new_image = Image.new('RGB', (new_width, new_height))

    # Paste the first image on the left side
    new_image.paste(image1, (0, 0))

    # Paste the second image on the right side
    new_image.paste(image2, (image1.width, 0))

    # Save the result
    new_image.save(output_path)

def concatenate_images_in_folders(dataset_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over each label folder in the dataset
    for label_folder in os.listdir(dataset_folder):
        label_path = os.path.join(dataset_folder, label_folder)

        # Ensure it is a directory
        if os.path.isdir(label_path):
            # Iterate over each patch folder in the label folder
            for patch_folder in os.listdir(label_path):
                patch_path = os.path.join(label_path, patch_folder)

                # Ensure it is a directory
                if os.path.isdir(patch_path):
                    # List images in the patch folder
                    images = [img for img in os.listdir(patch_path) if img.endswith(".jpg")]

                    # Ensure there are exactly two images in the patch folder
                    if len(images) == 2:
                        # Sort the images to maintain order
                        images.sort()

                        # Get the paths of the two images
                        image1_path = os.path.join(patch_path, images[0])
                        image2_path = os.path.join(patch_path, images[1])

                        # Create output path for the concatenated image
                        output_path = os.path.join(output_folder, f"{patch_folder}.jpg")

                        # Concatenate the images
                        concatenate_images(image1_path, image2_path, output_path)

# Example usage
dataset_folder = '/content/croped_patches'
output_folder = '/content/output_concatenated3'

concatenate_images_in_folders(dataset_folder, output_folder)

import shutil

# Set the output folder path
output_folder = "output_concatenated3"

# Create a zip file of the output folder
shutil.make_archive(output_folder, 'zip', output_folder)

# Move the zip file to a location where it can be easily downloaded
shutil.move(f"{output_folder}.zip", "/content/GIORGIS23.zip")