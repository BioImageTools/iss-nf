from starfish.spots import FindSpots
from starfish import FieldOfView, Experiment
from starfish.core.imagestack.imagestack import ImageStack
from starfish.types import Axes, FunctionSource


def find_spots( json_path,
                min_sigma=1,
                max_sigma=2,
                num_sigma=30,
                threshold=.003,
                measurement_type='mean'
):
    experiment = Experiment.from_json(json_path)
   
    fov = experiment.fov()
    primary = fov.get_image(FieldOfView.PRIMARY_IMAGES)
    reference = fov.get_image('anchor_dots')
    
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

    return spots

if __name__ == "__main__":
    
    json_path = '/path/to/primary/experiment.json'
    find_spots(json_path)