import os
import argparse
import tifffile as tiff
from starfish.core.experiment.builder import *

def print_image_shape(img_path):
    print(tiff.memmap(img_path).shape)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('paths', nargs='*')
    parser.add_argument('--flag', default=True)
    args = parser.parse_args()
    
    for arg in args.paths:
        #print(arg)
        print_image_shape(arg)
        