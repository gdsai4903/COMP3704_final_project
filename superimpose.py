import os
import random
from PIL import Image

def superimpose_images(human_image_path, background_image_path, output_image_path, position=(0, 0)):
    """
    Superimpose a human image with a transparent background onto an underwater image.
    
    Parameters:
    - human_image_path: str, path to the human cutout image (PNG)
    - background_image_path: str, path to the underwater background image (JPG/PNG)
    - output_image_path: str, path to save the final superimposed image
    - position: tuple, coordinates (x, y) where the human cutout will be placed on the background
    """
    
    # Open the human cutout and the underwater background images
    human_image = Image.open(human_image_path).convert("RGBA")
    background_image = Image.open(background_image_path).convert("RGBA")
    
    # Optionally resize the human image to fit the background better (e.g., scaling down)
    human_image = human_image.resize((int(background_image.width * 0.3), int(background_image.height * 0.3)))
    # Randomly generate the position on the background
    max_x = background_image.width - background_image.width
    max_y = background_image.height - background_image.height
    position = (random.randint(0, max_x), random.randint(0, max_y))
    # Paste the human image on the background using its alpha channel for transparency
    background_image.paste(human_image, position, human_image)
    
    # Save the resulting image
    background_image.save(output_image_path)

# Example usage
human_dir = "Data/range_without_bg_processed"
bg_dir = 'Data/Upward-looking'
output_dir = 'Data/superimposed'



if __name__=='__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_name in os.listdir(human_dir):
        human_img_path = os.path.join(human_dir, image_name)
        for bg_name in os.listdir(bg_dir):
            bg_img_path = os.path.join(bg_dir, bg_name)

        output_path = os.path.join(output_dir, f"{image_name+bg_name}.png")
        superimpose_images(human_img_path, bg_img_path, output_path)
