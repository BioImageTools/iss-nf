import os
import csv
from slicedimage import ImageFormat
from starfish.experiment.builder import format_structured_dataset
         
def spaceTx_format(input_path, csv, output_path):

    format_structured_dataset(input_path, csv, output_path, ImageFormat.TIFF)

    
if __name__ == "__main__":
    
    spaceTx_format(input_dir, path_to_csv, output_dir)
