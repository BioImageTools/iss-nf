import os
import fire
import csv
from slicedimage import ImageFormat
from starfish.experiment.builder import format_structured_dataset
         
def spaceTx_format(input_path, csv, output_path):

    format_structured_dataset(input_path, csv, output_path, ImageFormat.TIFF)

    
if __name__ == "__main__":
    cli = {
        "run_formating": spaceTx_format
    }
    fire.Fire(cli)
            