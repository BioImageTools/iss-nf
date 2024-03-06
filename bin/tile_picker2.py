import os
import random
import numpy as np
from starfish import Experiment
import fire
import csv

def tile_picker(picked_tiles):
    
    max_intensity = 0
    max_intensity_file = ''

    for fov_num, file_name in picked_tiles:

        image = file_name.xarray
        intensity = np.sum(image)

        if intensity > max_intensity:
            max_intensity = intensity
            max_intensity_file = fov_num

    return max_intensity_file

def auto_tilePicker(files, n_tilePicker=30, min_thr=.0008, max_thr=.01, n_vals=10):
        
        print('gggggggggggggggggggggggggggggggggg', files)
        num_fovs = len(files)
        print('ddddddddddddddddddd', num_fovs)
        random_int = [random.randint(1, num_fovs-1) for _ in range(n_tilePicker)]
        print('ssssssss', random_int)
        formatted_int = [f"{num:03}" for num in random_int]
        print('oooooooooooooo', formatted_int)
        picked_tiles = [os.path.basename(f'anchor_dots-fov_{i}-c0-r0-z0.tiff') for i in formatted_int]        
        tile = tile_picker(picked_tiles)
        thresholds = np.logspace(np.log10(min_thr), np.log10(max_thr), n_vals, base=10)
        
        np.savetxt('thresholds.txt', thresholds)
        with open('picked_tile.txt', mode='w') as file:
            file.write(tile)
              
                    
if __name__ == "__main__":
    
    cli = {
        "tile_picker": auto_tilePicker
    }
    fire.Fire(cli)



