import os
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
    
    cmaps = [plt.cm.Reds_r, plt.cm.Greens_r]
    downscale_factor=10
    region_size=100
    dapis_after = []
    dapis_before = []
    for file in regImg_path:
        file_name = os.path.basename(file)

        if file_name.startswith('registered_') and (file_name.endswith('_DAPI.tiff') or file_name.endswith('_DAPI.tif')): #or file.endswith('_DAPI.tif'):
            dapis_after.append(file)
        if file_name.startswith('norm_') and (file_name.endswith('_nuclei.tiff') or file_name.endswith('_nuclei.tif')): #or file.endswith('_nuclei.tif'):
            nuclei_dir_after = file
        if file_name.startswith('r') and file_name[1].isdigit() and (file_name.endswith('_DAPI.tiff') or file_name.endswith('_DAPI.tif')):#or file.endswith('_DAPI.tif'):
            dapis_before.append(file)
        if file_name.startswith('anchor') and (file_name.endswith('_nuclei.tiff') or file_name.endswith('_nuclei.tif')):#or file.endswith('_nuclei.tif'):
            nuclei_dir_before = file
            
    ref_before = tif.memmap(nuclei_dir_before)
    ref_before = rescale_image(ref_before)
    ref_after = tif.memmap(nuclei_dir_after)
    ref_after = rescale_image(ref_after)

    if min(ref_after.shape) > 1000:
        ref_before = downsample_img(ref_before, downscale_factor)
        ref_after = downsample_img(ref_after, downscale_factor)
        region_size *= 2

    x_center, y_center = find_roi(ref_after, region_size)

    num_images = len(dapis_after)
    num_cols = len(dapis_after)
    num_rows = -(-num_images // num_cols)  

    fig_height = 10 * num_rows

    fig, axes = plt.subplots(1, num_cols, figsize=(20, fig_height))
    
    for i, dapi_path_before in enumerate(dapis_before):
        dapi_img_before = tif.memmap(dapi_path_before)
        dapi_img_before = rescale_image(dapi_img_before)
        if min(dapi_img_before.shape) > 1000:
            dapi_img_before = downsample_img(dapi_img_before, downscale_factor)
        dapi_roi_img_before = read_roi_img(dapi_img_before, x_center, y_center, region_size)

        col_idx = i  

        ax = axes[col_idx] 

        ax.imshow(ref_before, cmap=cmaps[0], vmin=np.min(ref_before), vmax=np.max(ref_before)/2)
        ax.imshow(dapi_img_before, cmap=cmaps[1], alpha=0.6, vmin=np.min(dapi_img_before), vmax=np.max(dapi_img_before)/2)
        ax.set_title(f'Overlaid DAPI Image {i + 1} before registration', fontsize=10)
        ax.axis('off')

    plt.tight_layout()
    qc_path = os.getcwd()
    output_plot_path_1 = os.path.join(qc_path, "registration_qc_plots_1.png")
    plt.savefig(output_plot_path_1, bbox_inches='tight')
    plt.show()
    plt.close() 

    fig_height = 10 * num_rows   
    fig, axes = plt.subplots(2 * num_rows, num_cols, figsize=(20, fig_height))

    for i, dapi_path_after in enumerate(dapis_after):
        dapi_img_after = tif.memmap(dapi_path_after)
        dapi_img_after = rescale_image(dapi_img_after)
        if min(dapi_img_after.shape) > 1000:
            dapi_img_after = downsample_img(dapi_img_after, downscale_factor)
        dapi_roi_img_after = read_roi_img(dapi_img_after, x_center, y_center, region_size)

        row_idx = i // num_cols
        col_idx = i % num_cols

        ax1 = axes[row_idx * 2][col_idx]
        ax2 = axes[row_idx * 2 + 1][col_idx]

        ax1.imshow(ref_after, cmaps[0], vmin=np.min(ref_after), vmax=np.max(ref_after)/2)
        ax1.imshow(dapi_img_after,  cmaps[1], alpha=.6, vmin=np.min(dapi_img_after), vmax=np.max(dapi_img_after)/2)
        ax1.set_title(f'Overlaid DAPI Image {i + 1} after registration', fontsize=10)
        ax1.axis('off')

        # Add grid lines to the current subplots with black color
        ax2.grid(True, linestyle='-', color='red', linewidth=0.9)

        ax2.imshow(dapi_roi_img_after, cmap='gray')
        ax2.set_title(f'DAPI ROI Image {i + 1}')

    for i in range(num_images, num_rows * num_cols):
        row_idx = i // num_cols
        col_idx = i % num_cols
        axes[row_idx * 2][col_idx].axis('off')
        axes[row_idx * 2 + 1][col_idx].axis('off')

    plt.tight_layout()
    qc_path = os.getcwd()
    output_plot_path_2 = os.path.join(qc_path, "registration_qc_plots_2.png")
    plt.savefig(output_plot_path_2, bbox_inches='tight')
    plt.show()
    plt.close() 

    # Encoding both images and including them in the HTML content
    with open(output_plot_path_1, "rb") as image_file:
        encoded_string_1 = base64.b64encode(image_file.read()).decode('utf-8')
    with open(output_plot_path_2, "rb") as image_file:
        encoded_string_2 = base64.b64encode(image_file.read()).decode('utf-8')

    html_content = f"""
    <html>
    <head>
    <title>QC Plot</title>
    </head>
    <body>
    <h1>QC Plot</h1>
    <p>This plot shows DAPI reference overlaid on DAPI images.</p>
    <img src="data:image/png;base64,{encoded_string_1}" alt="QC Plot 1">
    <img src="data:image/png;base64,{encoded_string_2}" alt="QC Plot 2">
    </body>
    </html>
    """
    output_html_path = os.path.join(qc_path, "0-reg_qc.html")
    with open(output_html_path, 'w') as f:
        f.write(html_content)
    

if __name__ == "__main__":

    regImg_path = sys.argv[1:]
    reg_qc_plot(regImg_path)
