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

if __name__ == "__main__":
    
    spots = '/from/spotDetection/only/for/one/tile'
    json_path = '/hpc/scratch/hdd1/nv066607/ISS_tmp/ISS_471_NSCLC253_BL2/SpaceTx/primary/experiment.json'
    data_to_decode = next(iter(spots.values()))
    decode_starfish(data_to_decode, json_path)
