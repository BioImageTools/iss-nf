import os
import argparse
import tifffile as tiff
import fire
from starfish.core.experiment.builder.structured_formatter import *
from starfish.experiment.builder import format_structured_dataset
from slicedimage import ImageFormat
from starfish import Experiment
from starfish.types import Axes


def print_folder_contents(folder):
    res = infer_stack_structure(Path(folder))
    print(res)
    #for f in os.listdir(folder):
    #    print(f)
    
def print_folder_contents2(folder):
    res = Path(folder)
    print(os.listdir(folder))
    #print(res)

def format_data(
    indir,
    coords
):
    format_structured_dataset(
        indir,
        coords,
        './',
        ImageFormat.TIFF
    )
    
def print_experiment(
    exp_dir
):
    for el in os.listdir(exp_dir):
        if 'experiment' in el:
            exp = Experiment.from_json(el)
            f = exp['fov_000']
            image = f.get_image("primary")
            img = image.sel({Axes.ROUND: 0, Axes.CH: 0}).xarray.squeeze()
            with open('experiment.txt', 'w') as fh:
                fh.write(f"Image shape is: {img.shape}")
    #print("Working!")
        
if __name__ == '__main__':
    cli = {
        "run": print_folder_contents,
        "run_folder": print_folder_contents2,
        "format": format_data,
        "print_experiment": print_experiment
    }
    fire.Fire(cli)