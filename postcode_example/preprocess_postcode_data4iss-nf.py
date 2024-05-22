import os
import re
import numpy as np
import pandas as pd
import tifffile as tiff
import fire
from skimage.exposure import rescale_intensity

"""
FUNCTION: This scripts need to be run in order to preprocess the mouse brain raw data referenced in the PoSTcode paper. There are two outputs:
    1. Tiled data normalised and with formatted names that can be used to start the workflow on the Spacetx-formatting step. Some csv files with the coordinates of the selected tiles are also produced at this step.
    2. Stitched data. Tiles are stitched together and padded so one can also run the whole end-to-end workflow. 

Usage: Follow the instructions to download the dataset. Once that this has been done, there will be a directory with some files like 'taglist.csv', 'tile_names.csv', etc. The script will need as an input the Path to the directory containing all the failes and the Output path to specify where to store them.
"""

fov_key = {
    '490LS': 'anchor_dots',
    'DAPI': 'nuclei',
}
channel_dict = {"425": 0, "488": 1, "568": 2, "647": 3}

primary_coords_str = ''
nuclei_coords_str = ''
anchor_dots_coords_str = ''


# Map the 'selected_tile_names'
def map_selected_tiles(indir):
    total_tiles = pd.read_csv(os.path.join(indir, 'tile_names.csv'))
    selected_tiles = list(total_tiles['selected_tile_names'])
    fov_idx_dict = {v:str(k) for k,v in enumerate(selected_tiles)}
    return selected_tiles, fov_idx_dict

def map_string(s):
    return f"fov_{int(s):03}"

def format_tiles(indir, outdir):
    """
    Format raw postcode mouse brain dataset downloaded from:
    
    https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BSST700
    
    Arguments
    ---------
    indir: str
        Path to directory containing all files. After download and unzipping, directory name is 'S-BSST700'
    outdir: str
        Path for writing formatted data and coordinates CSV file
    """
    selected_tiles, fov_idx_dict = map_selected_tiles(indir)
    total_fovs = []
    primary_coords_str = ''
    nuclei_coords_str = ''
    anchor_dots_coords_str = ''
    
    try:
        os.mkdir(outdir)
    except:
        pass
    
    for filename in os.listdir(os.path.join(indir, 'selected-tiles')):
        if '.tif' in filename:
            # Get metadata of tile coordinates and channel (see 'selected_tiles_map.png' in 'S-BSST700'):
            match = re.search(r"_X(\d+)_Y(\d+)_c0(\d+)", filename)
            channel = filename.split('_')[-1].split('.')[0]
            
            if match:
                X_number = match.group(1)
                Y_number = match.group(2)
                cycle = str(int(match.group(3)) - 1)#For StarFISH formating start round lower index at 0
                tile_value = 'X' + X_number + '_Y' + Y_number
                
                if tile_value in selected_tiles:
                    fov = fov_idx_dict[tile_value]
                    total_fovs.append(map_string(fov))
                    #total_fovs_str += fov_line_str
                    # Part for storing coordinates for each FoV:
                    x_min = int(X_number)*1000
                    y_min = int(Y_number)*1000
                    x_max, y_max = x_min+1000, y_min+1000
                

                if channel in fov_key.keys():
                    channel_key = fov_key[channel]
                    channel_idx = '0'
                else:
                    channel_key = 'primary'
                    channel_idx = str(channel_dict[channel])
                img = tiff.memmap(os.path.join(indir, 'selected-tiles', filename))
                new_filename = f'{channel_key}-f{fov}-r{cycle}-c{channel_idx}-z0.tiff'
            
                # Continuation of part for storing values:
                coords_string = [str(fov), cycle, channel_idx, '0', str(x_min), str(y_min), '0', str(x_max), str(y_max), '0.0001']
                string_line = ','.join(coords_string) + '\n'
                #print(string_line)
            
                if 'anchor_dots' in new_filename:
                    anchor_dots_coords_str += string_line
                elif 'nuclei' in new_filename:
                    nuclei_coords_str += string_line
                else:
                    primary_coords_str += string_line
                #print(X_number, Y_number, cycle, channel)
                #new_name = f"r{cycle}_"
                
                tiff.imwrite(os.path.join(outdir, new_filename), robust_min_max_norm(img.astype(np.float32)))
                #print(new_filename)
                
    # Save string to coordinate file:
    with open(os.path.join(outdir,'primary_coordinates.csv'), 'w') as fh:
        fh.writelines('fov,round,ch,zplane,xc_min,yc_min,zc_min,xc_max,yc_max,zc_max\n')
        fh.writelines(primary_coords_str)

    with open(os.path.join(outdir,'nuclei_coordinates.csv'), 'w') as fh:
        fh.writelines('fov,round,ch,zplane,xc_min,yc_min,zc_min,xc_max,yc_max,zc_max\n')
        fh.writelines(nuclei_coords_str)

    with open(os.path.join(outdir,'anchor_dots_coordinates.csv'), 'w') as fh:
        fh.writelines('fov,round,ch,zplane,xc_min,yc_min,zc_min,xc_max,yc_max,zc_max\n')
        fh.writelines(anchor_dots_coords_str)

    with open(os.path.join(outdir,'fovs.txt'), 'w') as fh:
        fh.writelines('\n'.join(list(set(total_fovs))))
                

def stitch_channel(ch_idx, round_idx, input_dir, output_dir):
    x_shape = 1000
    x_total_tiles = 14 * x_shape + 1000
    y_total_tiles = 16 * x_shape + 1000
    # Create rectangular array that can fit all tiles and with '120' in each element (approximate background value)
    stitched_img = np.full((y_total_tiles, x_total_tiles), 120)
    for im_name in os.listdir(input_dir):
        if ('.tif' in im_name) and (ch_idx in im_name):
            match = re.search(r"_X(\d+)_Y(\d+)_c0(\d+)", im_name)
            img_round = match.group(3)[-1]
            if int(img_round) == round_idx:
                X = int(match.group(1)) * 1000 - 10000
                Y = int(match.group(2)) * 1000
                stitched_img[Y:Y+1000, X:X+1000] = tiff.memmap(os.path.join(input_dir, im_name))
    output_name = f"r{round_idx}_{ch_idx}.tif"
    if ch_idx == '490LS':
        tiff.imwrite(os.path.join(output_dir, 'anchor_dots.tif'), stitched_img.astype(np.uint16))
    elif ch_idx == 'DAPI' and round_idx == 1:
        tiff.imwrite(os.path.join(output_dir, output_name), stitched_img.astype(np.uint16))
        tiff.imwrite(os.path.join(output_dir, 'anchor_nuclei.tif'), stitched_img.astype(np.uint16))
    else:
        tiff.imwrite(os.path.join(output_dir, output_name), stitched_img.astype(np.uint16))
    
def stitch_experiment(input_dir, output_dir):
    try:
        os.mkdir(output_dir)
    except:
        pass
    
    total_rounds = [1,2,3,4]
    channels = ['DAPI',"425", "488", "568", "647"]
    for ch in channels:
        for r in total_rounds:
            #print(ch, r)
            stitch_channel(ch, r, input_dir, output_dir)
            
    stitch_channel('490LS', 1, input_dir, output_dir)
    stitch_channel('DAPI', 1, input_dir, output_dir)


def robust_min_max_norm(
    image,
    max_percentile: bool = 99.9999,
    ) -> np.ndarray:
    """Min-max image normalization robust to brigh pixel outlier.

    Parameters
    ----------
    image
        Input image.
    max_percentile: float
        Pixel intensity percentile to use instead of maximum pixel intensity.
        This makes the method robust to bright outliers.
    Returns
    -------
    Normalized image (as np.ndarray).
    """
    # ITKELastix tends to add negative intensity values to registered images,
    # which seems to be added to otherwise normal intensities (as judged by
    # intensity distributions)
    # Clip intensities to interval [0, max intensity] to avoid negative values
    if type(image) == str:
        image_name = os.path.basename(image)
        image = tiff.memmap(image)
        save_image = True
    else:
        save_image = False
    
    image = np.clip(image, 0, None)

    image = rescale_intensity(
        image.astype(np.float32),
        in_range=(image.min(), np.percentile(image, max_percentile)),
        out_range=(0.0, 1.0))
    
    # Transformation above may generate max values slightly higher than 1.0
    # (1.0000001, for example), which causes errors downstream
    # Clip intensities to interval [0, 1]
    image = np.clip(image, 0, 1)

    if save_image:
        tiff.imwrite(os.path.join(OUTPATH, image_name), image)
    else:
        return image
    
if __name__ == "__main__":
    cli = {
        "run_tile_formating": format_tiles,
        "run_stitched_formating": stitch_experiment
    }
    fire.Fire(cli)
