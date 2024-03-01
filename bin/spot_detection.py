from starfish.spots import FindSpots
from starfish import FieldOfView, Experiment
from starfish.core.imagestack.imagestack import ImageStack
from starfish.types import Axes, FunctionSource
from starfish.core.spots.DecodeSpots.trace_builders import build_spot_traces_exact_match
from starfish.spots import DecodeSpots
from starfish.core.types import SpotFindingResults
from starfish.core.intensity_table.decoded_intensity_table import DecodedIntensityTable

import numpy as np


def find_spots( json_path,
                test_tile_idx=None,
                images=None,
                reference=None,
                min_sigma=1,
                max_sigma=2,
                num_sigma=30,
                threshold=.003,
                measurement_type='mean',
                decodingByStarfish=False,
)-> ImageStack:
    
    final_spots = {}
    exp = Experiment.from_json(json_path)
    
    if test_tile_idx is not None:
        exp = {fov_name: fov
               for i, (fov_name, fov) in enumerate(exp.items())
               if i in test_tile_idx} 
        
    for fov_name, fov in exp.items():
        primary = fov.get_image(FieldOfView.PRIMARY_IMAGES)
        reference = fov.get_image('anchor_dots')
        
        if images is not None and reference is not None:
            primary = images
            reference = reference

        bd = FindSpots.BlobDetector(
            min_sigma=min_sigma,
            max_sigma=max_sigma,
            num_sigma=num_sigma,
            threshold=threshold,
            is_volume=False,
            measurement_type=measurement_type,
        )
        dots_max = reference.reduce((Axes.ROUND, Axes.ZPLANE),
                                          func='max')
        spots = bd.run(image_stack=primary, reference_image=dots_max)

        final_spots[fov_name] = spots
        
        all_spots = []

        for fov_name, spot in final_spots.items():
            data_to_trace = build_spot_traces_exact_match(spot)
            all_spots.append([fov_name, np.swapaxes(data_to_trace.data, 1, 2)])

        all_spots = list(sorted(all_spots, key=lambda x:x[0]))
        all_spots = [all_spots[i][1] for i in range(len(all_spots))]
        all_spots = np.concatenate(all_spots, axis=0)
        
    
    if decodingByStarfish:
        results = decode_starfish(final_spots, json_path)
        return results[fov_name].to_features_dataframe().to_csv(f'{fov_name}.csv', index=False)
    else:
        return all_spots

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


if __name__ == "__main__":
    
    json_path = '/hpc/scratch/hdd1/nv066607/ISS_tmp/ISS_471_NSCLC253_BL2/SpaceTx/primary/experiment.json'
    results = find_spots(json_path, test_tile_idx=[200], threshold=.001, decodingByStarfish=False)