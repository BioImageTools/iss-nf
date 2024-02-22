from starfish.spots import DecodeSpots
from starfish.core.types import SpotFindingResults
from starfish.core.intensity_table.decoded_intensity_table import DecodedIntensityTable
from starfish import Experiment



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

def _process_fov(
    fov: FieldOfView,
    fov_name,
    normalize: bool = False,
    register: bool = True,
    filt: bool = True,
    reg_withDapi=True,
):
        primary = fov.get_image(FieldOfView.PRIMARY_IMAGES)
        reference = fov.get_image('anchor_dots')
        dapi_rounds = fov.get_image('nuclei')
        dapi_ref = fov.get_image('anchor_nuclei')

        if normalize:
            primary = self._normalize(image_stack=primary)
            
        if register:
            if reg_withDapi:
                primary_registered = self._register_new(
                                         fov_name,
                                         image_stack=primary,
                                         dapi_ref=dapi_ref,
                                         dapi_round=dapi_rounds
                                         )
            else:
                primary_registered = self._register(
                                         fov_name,
                                         reference_stack=reference,
                                         image_stack=primary,
                                         )

        if filt:
            filtered_imgs, filtered_ref = self._filter(
                                    reference_stack=reference,
                                    image_stack=primary)


        if filt is False:
            filtered_ref = reference
            filtered_imgs = primary_registered

        spots = self._find_spots(image_stack=filtered_imgs,
                                 reference_stack=filtered_ref)

        decoded = self._decode(spots)

        return decoded, spots, fov_name

if __name__ == "__main__":
    
    spots = '/from/spotDetection/only/for/one/tile'
    json_path = '/hpc/scratch/hdd1/nv066607/ISS_tmp/ISS_471_NSCLC253_BL2/SpaceTx/primary/experiment.json'
    data_to_decode = next(iter(spots.values()))
    decode_starfish(data_to_decode, json_path)
