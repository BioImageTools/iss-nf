import fire
import numpy as np
from registration import *
from starfish.spots import DecodeSpots
from starfish.core.imagestack.imagestack import ImageStack
from starfish.types import Axes
from starfish.spots import FindSpots, DecodeSpots
from starfish.core.types import SpotFindingResults
from starfish.core.intensity_table.decoded_intensity_table import DecodedIntensityTable
from starfish import Experiment, FieldOfView
from starfish.image import LearnTransform, ApplyTransform, Filter
from starfish.core.spots.DecodeSpots.trace_builders import build_spot_traces_exact_match
  

#### Auxiliary functions:
def register(
    image_stack: ImageStack,
    reference_stack: ImageStack,
    ) -> ImageStack:
    
    learn_translation = LearnTransform.Translation(reference_stack=reference_stack, axes=Axes.ROUND, upsampling=100)
    transforms_list = learn_translation.run(image_stack.reduce({Axes.CH, Axes.ZPLANE}, func='max'))

    # learn_translation = LearnTransform.Translation(reference_stack=reference_stack.reduce((Axes.ROUND, Axes.ZPLANE), func='max'), axes=Axes.ROUND, upsampling=100)
    # transforms_list = learn_translation.run(
    # image_stack.reduce({Axes.CH, Axes.ZPLANE}, func="max"))

    warp = ApplyTransform.Warp()
    registered = warp.run(image_stack, transforms_list=transforms_list,  in_place=False, verbose=True)

    return registered

def filter(
    radius,
    reference_stack: ImageStack,
    image_stack: ImageStack,
    ) -> ImageStack:
    
    filt = Filter.WhiteTophat(masking_radius=radius)
    filtered_imgs = filt.run(image_stack, verbose=False, in_place=False)
    filtered_ref  = filt.run(reference_stack, verbose=True, in_place=False)

    return filtered_imgs, filtered_ref

def find_spots(
    image_stack: ImageStack, 
    reference_stack: ImageStack,
    thresh,
) -> SpotFindingResults:
    """Detect spots using laplacian of gaussians approach."""
    bd = FindSpots.BlobDetector(
                min_sigma=1,
                max_sigma=3,
                num_sigma=30,
                threshold=thresh,
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

def process_fov(
    images_dir_path,
    fov_name,
    threshold,
    radius=9,
    filt= True,
    local_reg=not True
):
    exp = Experiment.from_json('experiment.json')
    fov = exp[fov_name]
    primary = fov.get_image(FieldOfView.PRIMARY_IMAGES)
    reference = fov.get_image('anchor_dots')
    
    if filt and not local_reg:
        primary, reference = filter(radius,
                                    reference_stack=reference,
                                    image_stack=primary)

    if not filt and local_reg:
        primary = register(image_stack=primary,
                           reference_stack=reference
                        )

    if filt and local_reg:
        
        primary = register(
                            image_stack=primary,
                           reference_stack=reference
                            )
        primary,  reference= filter(
                                    radius,
                                    reference_stack=reference,
                                    image_stack=primary
                                    )
        
    spots = find_spots(image_stack=primary,
                       reference_stack=reference, 
                       thresh=threshold
                       )

    spots4postcode = build_spot_traces_exact_match(spots)
    np.save(f'{fov_name}.npy', spots4postcode)
    decoded = decode(spots, exp)
    decoded.to_features_dataframe().to_csv(f'{fov_name}-starfish_results-{threshold}.csv', index=False)


if __name__ == "__main__":
    cli = {
        "decode_fov": process_fov
    }
    fire.Fire(cli)
