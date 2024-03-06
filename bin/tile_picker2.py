import os
import random
import numpy as np
from starfish import Experiment
import fire
import csv

def tile_intensity_checker(picked_tiles):
    
    max_intensity = 0
    max_intensity_file = ''
    results = {}
    for fov_num, file_name in picked_tiles:
        
        image = file_name.xarray
        intensity = np.sum(image)
        results[f'fov_{fov_num}'] = float(intensity)

    return results

def tile_picker(files, n_tilePicker):
        
        exp = Experiment.from_json('experiment.json')
        num_fovs = len(list(exp.keys()))
        random_int = [random.randint(1, num_fovs-1) for _ in range(int(n_tilePicker)+1)]
        formatted_int = [f"{num:03}" for num in random_int]
        picked_tiles = [[i, exp[f"fov_{i}"].get_image("anchor_dots")] for i in formatted_int]
        tiles = tile_intensity_checker(picked_tiles)
        
        sorted_items = sorted(tiles.items(), key=lambda x: x[1], reverse=True)
        top_three = sorted_items[:3]
        
        with open('picked_tiles.txt', 'w') as file:
            for key, value in top_three:
                file.write(f"{key}: {value}\n")     
                    
if __name__ == "__main__":
    
    cli = {
        "tile_picker": tile_picker
    }
    fire.Fire(cli)



