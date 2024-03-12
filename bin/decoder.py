import numpy as np
from starfish.core.spots.DecodeSpots.trace_builders import build_spot_traces_exact_match
from starfish.core.spots.DecodeSpots.trace_builders import build_spot_traces_exact_match
import postcode.decoding_functions as post_decfunc


def decoder(spots, json_path, test_tile_idx=None):
    
    spots_s = []
    
    if test_tile_idx is not None:
        data_to_trace = build_spot_traces_exact_match(spots[f'fov_{test_tile_idx[0]}'])
        spots_s.append([f'fov_{test_tile_idx[0]}', np.swapaxes(data_to_trace.data, 1, 2)])
    else:
        for fov_name, spot in spots.items():
            data_to_trace = build_spot_traces_exact_match(spot)
            spots_s.append([fov_name, np.swapaxes(data_to_trace.data, 1, 2)])
            
    spots_s = list(sorted(spots_s, key=lambda x:x[0]))
    spots_s = [spots_s[i][1] for i in range(len(spots_s))]
    spots_s = np.concatenate(spots_s, axis=0)
    
    experiment = Experiment.from_json(json_path)
    
    barcodes_01 = np.swapaxes(np.array(experiment.codebook), 1, 2)
    out = post_decfunc.decoding_function(
        spots_s, barcodes_01, print_training_progress=False)
    df_class_names = np.concatenate(
        (experiment.codebook.target.values,
         ['infeasible','background','nan']))
    try:
        postcode_decoded_df = post_decfunc.decoding_output_to_dataframe(
            out, df_class_names, df_class_names)
    except:
        print('No spots detected, omitting PoSTcode')
    
    return postcode_decoded_df
    
#if __name__ == "__main__":
    
    #spots = '/path/to/spotDetection/output'
    #json_path = '/path/to/SpaceTx/primary/experiment.json'
    #decoder(spots, tile_indx, json_path)
