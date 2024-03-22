import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tif
from skimage.transform import rescale
import sys
import base64

def downsample_img(img, factor):
    return rescale(img, 1 / factor, anti_aliasing=False, preserve_range=True, multichannel=False)

def rescale_image(img):
    img = img.astype(np.float32)
    img -= img.min()
    img /= img.max()
    return img

def find_roi(img, size):
    height, width = img.shape
    x_center = (width - size) // 2
    y_center = (height - size) // 2
    return x_center, y_center

def read_roi_img(img, x_center, y_center, size):
    return img[y_center:y_center+size, x_center:x_center+size]

def reg_qc_plot(regImg_path):
    downscale_factor=10
    region_size=100
    dapis = []
    for file in regImg_path:
        if file.endswith('_DAPI.tif'):
            dapis.append(file)
        if file.endswith('_nuclei.tif'):
            nuclei_dir = file
            print(nuclei_dir, 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwww')

    ref_path = glob.glob(nuclei_dir)[0]
    ref = tif.memmap(ref_path)
    ref = rescale_image(ref)

    if min(ref.shape) > 1000:
        ref = downsample_img(ref, downscale_factor)
        region_size *= 2

    x_center, y_center = find_roi(ref, region_size)

    num_images = len(dapis)
    num_cols = len(dapis)
    num_rows = -(-num_images // num_cols)

    fig_height = 10 * num_rows
    fig, axes = plt.subplots(2 * num_rows, num_cols, figsize=(20, fig_height))

    for i, dapi_path in enumerate(dapis):
        dapi_img = tif.memmap(dapi_path)
        dapi_img = rescale_image(dapi_img)
        if min(dapi_img.shape) > 1000:
            dapi_img = downsample_img(dapi_img, downscale_factor)
        dapi_roi_img = read_roi_img(dapi_img, x_center, y_center, region_size)

        row_idx = i // num_cols
        col_idx = i % num_cols

        ax1 = axes[row_idx * 2][col_idx]
        ax2 = axes[row_idx * 2 + 1][col_idx]

        ax1.imshow(ref, cmap='cividis', interpolation='nearest')
        ax1.imshow(dapi_img, cmap='magma', interpolation='nearest', alpha=.6)
        ax1.set_title(f'DAPI ref on top of DAPI Image {i + 1}')
        ax1.axis('off')
        
        # Add grid lines to the current subplots with black color
        ax2.grid(True, linestyle='-', color='red', linewidth=0.9)

        ax2.imshow(dapi_roi_img, cmap='gray')
        ax2.set_title(f'DAPI ROI Image {i + 1}')
    for i in range(num_images, num_rows * num_cols):
        row_idx = i // num_cols
        col_idx = i % num_cols
        axes[row_idx * 2][col_idx].axis('off')
        axes[row_idx * 2 + 1][col_idx].axis('off')
    plt.tight_layout()
    qc_path = os.getcwd()
    output_plot_path = os.path.join(qc_path, "registration_qc_plots.png")
    plt.savefig(output_plot_path, bbox_inches='tight')
    plt.show()
    plt.close() 
    with open(output_plot_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    html_content = f"""
    <html>
    <head>
    <title>QC Plot</title>
    </head>
    <body>
    <h1>QC Plot</h1>
    <p>This plot shows DAPI reference overlaid on DAPI images.</p>
    <img src="data:image/png;base64,{encoded_string}" alt="QC Plot">
    </body>
    </html>
    """
    output_html_path = os.path.join(qc_path, "0-reg_qc.html")
    with open(output_html_path, 'w') as f:
        f.write(html_content)
    

if __name__ == "__main__":

    regImg_path = sys.argv[1:]
    reg_qc_plot(regImg_path)
    # cli = {
    #     "reg_qc": reg_qc_plot,
    #     }
    # fire.Fire(cli)