from starfish.spots import FindSpots
from starfish import FieldOfView, Experiment
from starfish.types import Axes, FunctionSource


def find_spots( json_path,
                test_tile_idx,
                images=None,
                reference=None,
                min_sigma=1,
                max_sigma=2,
                num_sigma=30,
                threshold=.003,
                measurement_type='mean'
):
    
    final_spots = {}
    experiment = Experiment.from_json(json_path)
    
    if test_tile_idx is not None:
        exp = {fov_name: fov
               for i, (fov_name, fov) in enumerate(experiment.items())
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
        
    return final_spots

if __name__ == "__main__":
    
    json_path = '/path/to/SpaceTx/primary/experiment.json'
    find_spots(json_path, test_tile_idx=[9])