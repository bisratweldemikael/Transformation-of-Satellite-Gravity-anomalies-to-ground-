# Transformation-of-Satellite-Gravity-anomalies-to-ground-
new repo
# Generating a synthetic Ground Gravity Anomaly with Pix2Pix GAN

This project aims to utilize the pix2pix Generative Adversarial Network (GAN) architecture for generating ground gravity anomaly maps from satellite gravity anomaly data. The pipeline involves data preparation steps followed by training a pix2pix model tailored for this specific image-to-image translation task.

## Data Preparation

### 1. Alignment of GeoTIFF Images
GeoTIFF images containing satellite and ground gravity anomaly data are aligned using rasterio to ensure spatial consistency.

### 2. Cropping Non-White Patches
Non-white patches are cropped from aligned images to focus on relevant features. These patches are saved along with their spatial coordinates.

### 3. Concatenating Images
Pairs of images stored in labeled folders are concatenated to create input-output pairs for training the pix2pix model.

## Model Training

### 1. Discriminator Definition
A discriminator model is defined to assess the authenticity of generated ground gravity anomaly maps compared to real maps.

### 2. Generator Definition
A generator model is defined based on the U-Net architecture to learn the mapping from satellite gravity anomaly images to ground gravity anomaly maps.

### 3. GAN Definition
The generator and discriminator are combined into a GAN model, which is trained iteratively to improve the quality of generated maps.

## Usage

1. **Data Preparation**: Execute the data preparation script to align, crop, and organize GeoTIFF images.
2. **Model Training**: Train the pix2pix model using the prepared data to learn the mapping from satellite to ground gravity anomaly maps.
3. **Evaluation**: Assess the performance of the trained model by generating ground gravity anomaly maps from satellite data and comparing them with real maps.

## Requirements

- Python 3.x
- TensorFlow
- Keras
- Rasterio
- OpenCV
- Matplotlib


