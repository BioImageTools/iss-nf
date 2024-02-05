import fire
import tifffile as tiff
import numpy as np

def estimate_tile_size(registered_anchor_path):
    # Load the registered anchor image
    registered_anchor = tiff.imread(registered_anchor_path)

    # need to be completed ...
    
    print(f"Estimated Tile Size: {tile_size}")
    return tile_size

if __name__ == "__main__":
    cli = {
        "run": estimate_tile_size
    }
    fire.Fire(cli)
