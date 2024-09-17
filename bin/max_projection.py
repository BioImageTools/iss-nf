from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None  # Removes the limit
# List of image paths
image_paths = [
"/scratch/vakili/alvaro_convert/anchor_dots1.tiff",
"/scratch/vakili/alvaro_convert/anchor_dots2.tiff",
"/scratch/vakili/alvaro_convert/anchor_dots3.tiff"
]

# Load all images
images = [np.array(Image.open(image_path)) for image_path in image_paths]

# Check if any images were loaded
if not images:
    raise ValueError("No TIFF images found in the specified paths.")

# Convert the list of images to a NumPy array
stack = np.stack(images)

# Perform maximum intensity projection along the stack (axis=0)
max_projection = np.max(stack, axis=0)

# Convert the result back to an image
result_image = Image.fromarray(max_projection)

# Save the projected image as a TIFF file
output_file = '/scratch/vakili/alvaro_convert/anchor_dots.tiff'
result_image.save(output_file)

print(f"Projected image saved to {output_file}")
