import os
import fire
import csv
from collections import namedtuple
from typing import Union

import numpy as np
import tifffile as tiff
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.transform import resize, rescale
from skimage.io import imsave
from starfish.experiment.builder import format_structured_dataset


def tile_test_image(
    img_path: str
):
    # Loop on FoVs:
    img_name = os.path.basename(img_path).split('.')[0]
    meta = img_name.split('_')
    r, ch = meta[0], meta[1]
    for fov in range(2):
        df = pd.DataFrame({'fov': [1, 2, 3]})
        coords_fov = f"coordinates-fov_{fov}.csv"
        df.to_csv(coords_fov, index=False)
        #for cidx, c in e:
        name = f"primary-f{fov}-{r}-{ch}-z0.tif"
        imsave(name, np.zeros((20,20)).astype(np.float32))
            #with open(name + '.txt', 'w') as fh:
            #   fh.write('path2image')

def save_path_txt(
    img_path
):
    base_name = os.path.basename(img_path)
    with open(base_name + ".txt", "w") as fh:
        fh.write(str(img_path))
        
#def print_list(
#    l: list
#    args*
#):
#    for el in l:
#        print(l)
        
#def format2spacetx(
#    image_file
#):
    
            
        
if __name__ == "__main__":
    cli = {
        "run_tiling": tile_test_image,
        "run_post": save_path_txt
    }
    fire.Fire(cli)
	
