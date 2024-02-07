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

from dask.distributed import Client, as_completed

from . import utils


def _needs_padding(tile, tile_size) -> bool:
    return any([tile.shape[i] < tile_size for i in [0, 1]])

def _pad_to_size(
    image: np.ndarray,
    tile_size: int,
) -> np.ndarray:


    if _needs_padding(image, tile_size):
        pad_width = tuple((0, tile_size - image.shape[i]) for i in [0, 1])
        image = np.pad(image, pad_width, 'constant')

    return image

def _select_roi(image, roi):
    return image[roi.row:roi.row + roi.nrows,
                 roi.col:roi.col + roi.ncols]

def _get_round_id(name):
    r = int(name.split('r')[1].split('_')[0])
    r -= 1  
    return r

def _get_ch_id(name):
    return [ch_map[flcr] for flcr in ch_map if flcr in name][0]

def _get_files_by_type(image_files, img_type):
    if 'anchor' in img_type:
        return {k: v for k, v in image_files.items()
                if img_type in k}
    elif img_type == 'nuclei':
        return {k: v for k, v in image_files.items()
                if 'DAPI' in k}
    else:
        return {k: v for k, v in image_files.items()
                if not 'anchor' in k and not 'DAPI' in k}


def get_tile_coordinates(tile_size: int, image_shape) -> None:

    tile_coordinates = {}

    RoI = namedtuple('RoI', ['row', 'col', 'nrows', 'ncols'])
    tile_n = 0

    def _get_size(position, tile_size, total_size):
        dist_to_end = total_size - position
        size = tile_size
        size = size if dist_to_end > size else dist_to_end

        return size

    for r in range(0, image_shape[0], tile_size):
        nrows = _get_size(r, tile_size, image_shape[0])

        for c in range(0, image_shape[1], tile_size):
            ncols = _get_size(c, tile_size, image_shape[1])

            tile_coordinates[tile_n] = RoI(r, c, nrows, ncols)
            tile_n += 1

    return tile_coordinates


def _tile_image(image_name, file, tile_size, img_type,
                output_dir, tile_coordinates):

    image = tiff.memmap(file)
    coordinates = []
    for tile_id in tile_coordinates:
        coords = tile_coordinates[tile_id]
        tile = self._select_roi(
            image, roi=coords)
        tile = self._pad_to_size(tile, tile_size)

        r = 0 if 'anchor' in img_type \
            else self._get_round_id(image_name)

        c = self._get_ch_id(image_name) \
            if img_type in ['primary'] else 0

        file_name = f'{img_type}-f{tile_id}-r{r}-c{c}-z0.tiff'
        tiff.imsave(os.path.join(output_dir, file_name), tile)

        coordinates.append([
            tile_id, r, c, 0,
            coords.col, coords.row, 0,
            coords.col + tile_size, coords.row + tile_size, 0.0001])

    return coordinates

def _write_coords_file(self, coordinates, file_path) -> None:
    coords_df = pd.DataFrame(
        coordinates,
        columns=('fov', 'round', 'ch', 'zplane',
                 'xc_min', 'yc_min', 'zc_min',
                 'xc_max', 'yc_max', 'zc_max'))
    coords_df.to_csv(file_path, index=False)

def tile_images(tile_size: int, image_shape, image_files) -> None:

    tile_coordinates = get_tile_coordinates(tile_size, image_shape)

    img_types = ['anchor_dots', 'anchor_nuclei', 'nuclei', 'primary']     

    for img_type in img_types:
        os.makedirs(os.path.join(output_dir, img_type))
        type_images = _get_files_by_type(image_files, img_type)
        coordinates = []

        for i, (name, file) in enumerate(type_images.items()):
            mask_longer_strs = ' ' * 15

            image = tiff.memmap(file)
            coordinates = _tile_image(
                image, name, tile_size, img_type, coordinates, 
                os.path.join(output_dir, img_type))

        self._write_coords_file(
            coordinates,
            os.path.join(output_dir, img_type, 'coordinates.csv'))    
            
            
if __name__ == "__main__":
    
    channel_id_map: dict = {'Cy7': 0, 'Cy5': 2, 'Cy3': 1, 'FITC': 3},
    image_files = utils.get_image_file_map(input_dir)
    image_shape =
    tile_images(tile_size=size, image_shape, image_files)
            
            
            
            