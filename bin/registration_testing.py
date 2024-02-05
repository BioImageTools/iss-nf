import fire
import numpy as np
import tifffile as tiff
from skimage import transform as tf
from skimage.io import imsave

import itk

"""
class ElastixRegistrator:
    def __init__(self, rescale_factor, parameter_files_path: str, task_output_transformation):
        self.parameter_files_path = parameter_files_path
        self.rescale_factor = rescale_factor
        self.task_output_transformation = task_output_transformation
"""

def read_image(img_path):
    return itk.imread(img_path, itk.F)

def get_image_metadata(img):
    return (itk.size(img), itk.origin(img), itk.spacing(img))

def learn_transform(
    *elastix_parameter_files
):
    """
    Main function for learning transformation using ITK.
    
    Parameters
    ----------
    elastix_parameter_files
        Path to TXT file containing parameters for registration.
    """
    for parameter_file in elastix_parameter_files:
        print(parameter_file)
    #print(fix_image_path)
    # Build parameter object:
    #parameter_object = itk.ParameterObject.New()
    #parameter_object.ReadParameterFile(parameter_files)
    
    #return f'Learning transformation from test is done!'
    
    
if __name__ == "__main__":
    cli = {
        "run": learn_transform
    }
    fire.Fire(cli)