import os
import fire
import tifffile as tiff
import starfish
from starfish.types import Axes

def download_data(
    outdir: str,
    fov_idx: str = 'fov_001',
    x_range: tuple = (0, 512),
    y_range: tuple = (0, 512)
):
    # Set slice:
    x_slice = slice(x_range[0], x_range[1])
    y_slice = slice(y_range[0], y_range[1])
    
    # create output directory:
    try:
        os.mkdir(outdir)
    except:
        pass
    # Load experiment from bucket:
    exp = starfish.Experiment.from_json(
        "https://d2nhj9g34unfro.cloudfront.net/browse/formatted/20180926/iss_breast/experiment.json")
    # Select fov of interest:
    fov = exp[fov_idx]
    
    # Write nuclei and anchor dots:
    nuclei_stack = fov.get_image("nuclei", x=x_slice, y=y_slice).xarray.squeeze()
    tiff.imwrite(os.path.join(outdir, "anchor_nuclei.tif"), nuclei_stack)
    
    dots_stack = fov.get_image("dots", x=x_slice, y=y_slice).xarray.squeeze()
    tiff.imwrite(os.path.join(outdir, "anchor_dots.tif"), dots_stack)
    
    # Iterate over four rounds and four channels:
    image_stack = fov.get_image("primary", x=x_slice, y=y_slice)
    for r in range(4):
        # Create 'fake' nuclei for the registration:
        tiff.imwrite(os.path.join(outdir, f"r{r}_DAPI.tif"), nuclei_stack)
        for ch in range(4):
            img = image_stack.sel({Axes.ROUND: r, Axes.CH: ch}).xarray.squeeze()
            tiff.imwrite(os.path.join(outdir, f"r{r}_ch{ch}.tif"), img)

    # Save codebook:
    exp.codebook.to_json(os.path.join(outdir, 'codebook_minimaldataset.json'))
    
if __name__ == "__main__":
    cli = {
        "create_test_iss": download_data
    }
    fire.Fire(cli)