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

def auto_tilePicker(exp_dir, n_tilePicker=30, min_thr=.0008, max_thr=.01, n_vals=10):
        json_path = '/hpc/scratch/hdd1/sg250269/ISS_tmp/ISS_451_NSCLC78_BL3/SpaceTx/primary/experiment.json'
        exp = Experiment.from_json(json_path)
        #exp = Experiment.from_json('experiment.json')
        num_fovs = len(list(exp.keys()))
        random_int = [random.randint(1, num_fovs-1) for _ in range(n_tilePicker)]
        formatted_int = [f"{num:03}" for num in random_int]

        picked_tiles = [[i, exp[f"fov_{i}"].get_image("anchor_dots")] for i in formatted_int]
        
        tile = tile_picker(picked_tiles)
        thresholds = np.logspace(np.log10(min_thr), np.log10(max_thr), n_vals, base=10)
        
        np.savetxt('thresholds.txt', thresholds)
        with open('picked_tile.txt', mode='w') as file:
            file.write(tile)

        #return tile, thresholds
              
                    
if __name__ == "__main__":
    
    cli = {
        "tile_picker": auto_tilePicker
    }
    fire.Fire(cli)

