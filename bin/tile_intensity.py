import numpy as np
import tifffile as tif
import fire 

def tile_intensity(path):

    image = tif.memmap(f'{path}')
    intensity = np.sum(image)

    filename = path.split('/')[-1].split('-c')[0]

    with open(f'tile_intensity_{filename}.txt', mode='w') as file:
        file.write(str(intensity))   
    
            
if __name__ == "__main__":
    
    cli = {
        "intensity_measurement": tile_intensity
    }
    fire.Fire(cli)

