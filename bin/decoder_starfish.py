import fire
import pickle
import os
import numpy as np
from registration import *
from starfish.spots import DecodeSpots
from starfish.core.imagestack.imagestack import ImageStack
from starfish.types import Axes, FunctionSource
from starfish.spots import FindSpots, DecodeSpots, AssignTargets
from starfish.core.types import SpotFindingResults
from starfish.core.intensity_table.decoded_intensity_table import DecodedIntensityTable
from starfish import Experiment, FieldOfView
from starfish.image import LearnTransform, ApplyTransform, Filter, Segment
from starfish.core.spots.DecodeSpots.trace_builders import build_spot_traces_exact_match

#### Auxiliary functions:
def register(
    image_stack: ImageStack,
    reference_stack: ImageStack,
) -> ImageStack:
    learn_translation = LearnTransform.Translation(
        reference_stack=reference_stack, axes=Axes.ROUND, upsampling=100)

    transforms_list = learn_translation.run(
        image_stack.reduce({Axes.CH, Axes.ZPLANE}, func='max'))

    warp = ApplyTransform.Warp()
    registered = warp.run(image_stack, transforms_list=transforms_list,
                            in_place=False, verbose=False)

    return registered

def find_spots(
    image_stack: ImageStack, 
    reference_stack: ImageStack,
    threshold: float = 0.003
) -> SpotFindingResults:
    """Detect spots using laplacian of gaussians approach."""
    bd = FindSpots.BlobDetector(
                threshold=threshold,
                min_sigma=1,
                max_sigma=2,
                num_sigma=30,
                is_volume=False,
                measurement_type='mean')
    dots_max = reference_stack.reduce((Axes.ROUND, Axes.ZPLANE),
                                       func='max')
    # Locate spots in reference image
    spots = bd.run(image_stack=image_stack, reference_image=dots_max)

    return spots

def decode(spots: SpotFindingResults, experiment) -> DecodedIntensityTable:
    """Decode pixel traces using the codebook."""
    decoder = DecodeSpots.PerRoundMaxChannel(
        codebook=experiment.codebook,
    )
    decoded = decoder.run(spots=spots)

    return decoded

"""
def decode_starfish(spots: SpotFindingResults, json_path) -> DecodedIntensityTable:

    exp = Experiment.from_json(json_path)
    codebook = exp.codebook
    decoder = DecodeSpots.PerRoundMaxChannel(
        codebook=codebook,
    )
    decoded_spots = {}
    for fov_name, spot in spots.items():
        decoded = decoder.run(spots=spot)
        decoded_spots[fov_name] = decoded

    return decoded_spots
"""

def process_fov(
    images_dir_path,
    fov_name: str,
    threshold: float = 0.003
):
    #exp = Experiment.from_json(os.path.join(images_dir_path, 'experiment.json'))
    exp = Experiment.from_json('experiment.json')
    fov = exp[fov_name]
    primary = fov.get_image(FieldOfView.PRIMARY_IMAGES)
    reference = fov.get_image('anchor_dots')
    dapi_rounds = fov.get_image('nuclei')
    dapi_ref = fov.get_image('anchor_nuclei')

    #if normalize:
    #    primary = _normalize(image_stack=primary)
            
    #if True:
        #if reg_withDapi:
        #primary_registered = self._register_new(
        #                                 fov_name,
        #                                 image_stack=primary,
        #                                 dapi_ref=dapi_ref,
        #                                 dapi_round=dapi_rounds
        #                                 )
        #    else:
    #primary_registered = register(
    #                        reference_stack=reference,
    #                        image_stack=primary
    #                        )

    filtered_ref = reference
    filtered_imgs = primary#_registered

    spots = find_spots(image_stack=filtered_imgs,
                       reference_stack=filtered_ref,
                       threshold=threshold)

    #decoded = decode(spots, exp)
    
    spots4postcode = build_spot_traces_exact_match(spots)
    #print(f"{fov_name}"*10)
    np.save(f'{fov_name}.npy', spots4postcode)
    # Do starfish decoding already in here:
    decoded = decode(spots, exp)
    decoded.to_features_dataframe().to_csv(f"{fov_name}-{str(threshold).split('.')[1]}-starfish_results.csv", index=False)


if __name__ == "__main__":
    cli = {
        "decode_fov": process_fov
    }
    fire.Fire(cli)