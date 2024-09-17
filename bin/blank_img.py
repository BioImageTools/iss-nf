import numpy as np
from PIL import Image

# Define the image size
image_shape = (34042, 26594)

# Create a black image with the desired size
black_image = np.zeros(image_shape, dtype=np.uint32)  # Using uint16 to match typical image depth

# Convert the numpy array to a PIL Image
black_image_pil = Image.fromarray(black_image)

# Save the image as a TIFF file
black_image_pil.save("/scratch/vakili/alvaro_convert/r7_Cy3.tiff", format='TIFF')
black_image_pil.save("/scratch/vakili/alvaro_convert/r8_Cy3.tiff", format='TIFF')
