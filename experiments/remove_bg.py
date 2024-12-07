import os
import numpy as np
from PIL import Image
import scipy.io as sio

def load_segmentation_map(mat_path, key='MM'):
    # Load .mat file
    mat_data = sio.loadmat(mat_path)
    
    # Extract the segmentation mask
    segmentation_map = mat_data[key][0][0][0]  # Assuming 'PartMask' is at this location
    return segmentation_map

def apply_mask(image, mask):
    # Threshold the mask to create a binary mask
    binary_mask = (mask > 0.5).astype(np.uint8)  # Threshold can be adjusted as needed
    
    # Ensure the mask is 3D to match the image's shape
    if binary_mask.ndim == 2:
        binary_mask = np.stack([binary_mask] * 4, axis=-1)  # Convert (H, W) to (H, W, 3)
    
    # Apply the binary mask to the image (keeping only the foreground)
    masked_image = image * binary_mask
    
    return masked_image

def remove_background_from_image(image_path, mat_path, output_path):
    # Load the image
    image = np.array(Image.open(image_path).convert('RGBA'))

    # Load the segmentation mask
    segmentation_map = load_segmentation_map(mat_path)

    # Apply the segmentation mask to remove the background
    masked_image = apply_mask(image, segmentation_map)

    # Save the resulting image with transparent background
    result_image = Image.fromarray(masked_image)
    result_image.save(output_path)

# Example usage
input_dir = "Data/range_without_bg/images"
mask_dir = 'Data/range_without_bg/mask'
output_dir = 'Data/range_without_bg_processed'



if __name__=='__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_name in os.listdir(input_dir):
        input_img_path = os.path.join(input_dir, image_name)
        mask = os.path.join(mask_dir, f"{image_name.split('.')[0]}.mat")

        output_path = os.path.join(output_dir, f"{image_name.split('.')[0]}.png")

        remove_background_from_image(input_img_path, mask, output_path)
