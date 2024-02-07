import os
import csv
from collections import namedtuple
from typing import Union

import numpy as np
import tifffile as tiff
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.transform import resize, rescale


def needs_padding(tile, tile_size) -> bool:
    return any([tile.shape[i] < tile_size for i in [0, 1]])

def pad_to_size(
    image: np.ndarray,
    tile_size: int,
) -> np.ndarray:

    if needs_padding(image, tile_size):
        pad_width = tuple((0, tile_size - image.shape[i]) for i in [0, 1])
        image = np.pad(image, pad_width, 'constant')

    return image

def select_roi(image, roi):
    return image[roi.row:roi.row + roi.nrows,
                 roi.col:roi.col + roi.ncols]

def get_round_id(name):
    r = int(name.split('r')[1].split('_')[0])
    r -= 1  
    return r

def get_ch_id(name):
    return [ch_map[flcr] for flcr in ch_map if flcr in name][0]

def get_tile_coordinates(tile_size: int, image_shape) -> None:

    tile_coordinates = {}

    RoI = namedtuple('RoI', ['row', 'col', 'nrows', 'ncols'])
    tile_n = 0

    def get_size(position, tile_size, total_size):
        dist_to_end = total_size - position
        size = tile_size
        size = size if dist_to_end > size else dist_to_end

        return size

    for r in range(0, image_shape[0], tile_size):
        nrows = get_size(r, tile_size, image_shape[0])

        for c in range(0, image_shape[1], tile_size):
            ncols = get_size(c, tile_size, image_shape[1])

            tile_coordinates[tile_n] = RoI(r, c, nrows, ncols)
            tile_n += 1

    return tile_coordinates


def tile_image(image, image_name, tile_size, img_type, output_dir,
              tile_coordinates):

    coordinates = []
    for tile_id in tile_coordinates:
        coords = tile_coordinates[tile_id]
        tile = select_roi(
            image, roi=coords)
        tile = pad_to_size(tile, tile_size)

        r = 0 if 'anchor' in img_type \
            else self.get_round_id(image_name)

        c = self.get_ch_id(image_name) \
            if img_type in ['primary'] else 0

        file_name = f'{img_type}-f{tile_id}-r{r}-c{c}-z0.tiff'
        tiff.imsave(os.path.join(output_dir, file_name), tile)

        coordinates.append([
            tile_id, r, c, 0,
            coords.col, coords.row, 0,
            coords.col + tile_size, coords.row + tile_size, 0.0001])

    return coordinates

def write_coords_file(coordinates, file_path) -> None:
    coords_df = pd.DataFrame(
        coordinates,
        columns=('fov', 'round', 'ch', 'zplane',
                 'xc_min', 'yc_min', 'zc_min',
                 'xc_max', 'yc_max', 'zc_max'))
    coords_df.to_csv(file_path, index=False)

def tile_images(image_path, tile_size,  output_dir) -> None:
    
    image = tiff.memmap(image_path)
    image_shape = image.shape
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    
    if "_DAPI" in image_name:
        img_type = 'nuclei'
    elif "dots" in image_name:
        img_type = 'anchor_dots'
    elif "_nuclei" in image_name:
        img_type = 'anchor_nuclei'
    else:
        img_type = 'primary'
        
    output = os.path.join(output_dir, img_type)

    tile_coordinates = get_tile_coordinates(tile_size, image_shape)
    
    coordinates = tile_image(image, image_name, tile_size, img_type, output,
                            tile_coordinates)

    write_coords_file(
        coordinates,
        os.path.join(output, 'coordinates.csv'))    
            
        
if __name__ == "__main__":
    
    tile_images(image_path, tile_size, output_dir)
            
            
            
            