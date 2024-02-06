import os
import fire
import numpy as np
import tifffile as tiff
from skimage import transform as tf
from skimage.io import imsave

import itk

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
    ### NOTE: KEEP NEXT LINES IN CASE WE WANT TO SAVE PATH OF INDIVIDUAL PARAMETER FILES IN TEXT FILE FOR NEXTFLOW
    #trnsfrms_paths_list = []
    #with open(parameter_files, "r") as fh:
    #    lines = fh.readlines()
    #    for line in lines:
    #        trnsfrms_paths_list.append(line.split('\n')[0])
    ### END OF NOTE FROM ABOVE
    
    # Build parameter object:
    parameter_object = itk.ParameterObject.New()
    parameter_object.ReadParameterFile(parameter_files)
    
    result_image, result_transform_parameters = itk.elastix_registration_method(
        read_image(fix_image_path),
        read_image(mov_image_path),
        parameter_object = parameter_object,
        log_to_console=False
    )
    
    # Get round number for transformation:
    round_id = os.path.basename(mov_image_path)[:2]
    
    ### SAME NOTE AS ABOVE, COME BACK AFTER KNOWING HOW TO STORE PARAMETER TEXT FILES
    #for i in range(len(trnsfrms_paths_list)):
    #    result_transform_parameters.WriteParameterFile(
    #        result_transform_parameters.GetParameterMap(i),
    #        f"transformation_{i+1}.txt"
    #    )
    ### END OF NOTE
    
    # Remove here after part above:
    result_transform_parameters.WriteParameterFile(
        result_transform_parameters.GetParameterMap(0),
        f"{round_id}_test_transformation.txt"
    )
    
    return f'Learning transformation from test is done!'
    
def apply_transform(
    parameter_result_transf: str,
    mov_image: str
):
    """
    Function to apply transformations learned from `learn_transform` function.
    
    Parameters
    ----------
    mov_image : str
        Path to moving image to which found transformation is applied.
    parameter_result_transf : str
        Path to TXT file with found parameters from the transformation.
        
    Returns
    -------
    Transformed image.
    """
    parameter_object = itk.ParameterObject.New()
    parameter_object.ReadParameterFile(parameter_result_transf)
    
    image = itk.imread(mov_image, itk.F)
    aligned_image = itk.transformix_filter(
        moving_image = image,
        transform_parameter_object = parameter_object,
        log_to_console=False)
    
    base_name = os.path.basename(mov_image)
    output_name = "registered_" + base_name
    aligned_image = np.asarray(aligned_image)
    tiff.imwrite(output_name, aligned_image)
    print(f"Saved {output_name} image!")
    
    
if __name__ == "__main__":
    cli = {
        "run_learn": learn_transform,
        "run_apply": apply_transform
    }
    fire.Fire(cli)