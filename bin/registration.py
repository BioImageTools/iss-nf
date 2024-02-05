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
    fix_image_path: str,
    mov_image_path: str,
    parameter_files: str
):
    """
    Main function for learning transformation using ITK.
    
    Parameters
    ----------
    fix_image_path : str
        Path to reference image for learning the transformation.
    mov_image_path : str
        Path to moving image for applying the transformation.
    parameter_files : str
        Path to TXT file containing full path for each parameter file.
        
    Returns
    -------
    result_parameters : 
        TXT file with result parameters.
    """
    # Get list with path of all transformations:
    trnsfrms_paths_list = []
    with open(parameter_files, "r") as fh:
        lines = fh.readlines()
        for line in lines:
            trnsfrms_paths_list.append(line.split('\n')[0])
    # Build parameter object:
    parameter_object = itk.ParameterObject.New()
    parameter_object.ReadParameterFile(trnsfrms_paths_list)
    
    result_image, result_transform_parameters = itk.elastix_registration_method(
        read_image(fix_image_path),
        read_image(mov_image_path),
        parameter_object = parameter_object,
        log_to_console=False
    )
    
    #result_transform_parameters.WriteParameterFile(
    #    result_transform_parameters.GetParameterMap(0),
    #    "test_transformation.txt"
    #)
    for i in range(len(trnsfrms_paths_list)):
        result_transform_parameters.WriteParameterFile(
            result_transform_parameters.GetParameterMap(i),
            f"transformation_{i+1}.txt"
        )
    return f'Learning transformation from test is done!'
    
    
if __name__ == "__main__":
    cli = {
        "run": learn_transform
    }
    fire.Fire(cli)