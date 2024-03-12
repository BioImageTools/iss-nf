import os
import fire
import numpy as np
import tifffile as tiff
from skimage.io import imsave
from skimage.exposure import rescale_intensity

import itk

def read_image(img_path):
    return itk.imread(img_path, itk.F)

def get_image_metadata(img):
    return (itk.size(img), itk.origin(img), itk.spacing(img))

def robust_min_max_norm(
    image,
    max_percentile: bool = 99.9999,
    ) -> np.ndarray:
    """Min-max image normalization robust to brigh pixel outlier.

    Parameters
    ----------
    image
        Input image.
    max_percentile: float
        Pixel intensity percentile to use instead of maximum pixel intensity.
        This makes the method robust to bright outliers.
    Returns
    -------
    Normalized image (as np.ndarray).
    """
    # ITKELastix tends to add negative intensity values to registered images,
    # which seems to be added to otherwise normal intensities (as judged by
    # intensity distributions)
    # Clip intensities to interval [0, max intensity] to avoid negative values
    if type(image) == str:
        image_name = os.path.basename(image)
        image = tiff.memmap(image)
        save_image = True
    else:
        save_image = False
    
    image = np.clip(image, 0, None)

    image = rescale_intensity(
        image.astype(np.float32),
        in_range=(image.min(), np.percentile(image, max_percentile)),
        out_range=(0.0, 1.0))
    
    # Transformation above may generate max values slightly higher than 1.0
    # (1.0000001, for example), which causes errors downstream
    # Clip intensities to interval [0, 1]
    image = np.clip(image, 0, 1)

    if save_image:
        tiff.imwrite("norm_" + image_name, image)
    else:
        return image

def learn_transform(
    fix_image_path: str,
    mov_image_path: str,
    *args,
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
    parameter_files = [arg for arg in args]
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
    
    #return f'Learning transformation from test is done!'
    
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
    aligned_image = robust_min_max_norm(aligned_image)
    tiff.imwrite(output_name, aligned_image)
    #print(f"Saved {output_name} image!")

    
if __name__ == "__main__":
    cli = {
        "run_learn": learn_transform,
        "run_apply": apply_transform,
        "run_norm": robust_min_max_norm
    }
    fire.Fire(cli)