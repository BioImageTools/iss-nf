#Input will be folder containing python files, each of the with the name of the FoV:
import numpy as np
import os
import fire
import exp_metadata_json as exp_meta
from starfish import Codebook
import postcode.decoding_functions as post_decfunc
import pandas as pd

def postcode_decoder(
    exp_metadata_json,
    codebook_json,
    *args
):
    # Parse metadata to get genes and variables used for the results' output
    ExpJsonParser = exp_meta.ExpJsonParser(exp_metadata_json)
    # try maybe with GSK data? -> PoSTcode failing with sample dataset
    spots = []
    starfish_decoded = []
    #Get ordered list:
    for arg in args:
        if arg.endswith(".npy"):
            spots.append(arg)
        else:
            starfish_decoded.append(arg)
    
    starfish_decoded_table = pd.DataFrame()

    for spots in enumerate(sorted(starfish_decoded)):
        fov_spot_table = pd.read_csv(spots)
        starfish_decoded_table = pd.concat([starfish_decoded_table, fov_spot_table])
        
    # totals_fovs = len(args)
    fovs = [os.path.basename(arg).split('.')[0] for arg in spots]
    spots_numpy = [np.load(spot_matrix) for spot_matrix in spots]
    spots_s = []
    for fov_name, data_to_trace in zip(fovs, spots_numpy):
        spots_s.append([fov_name,
                       np.swapaxes(data_to_trace.data, 1, 2)])
    
    # Original to change:
    #data_to_trace = build_spot_traces_exact_match(spots[f'fov_{test_tile_idx[0]}'])
    #    spots_s.append([f'fov_{test_tile_idx[0]}', np.swapaxes(data_to_trace.data, 1, 2)])
            
    spots_s = list(sorted(spots_s, key=lambda x:x[0]))
    spots_s = [spots_s[i][1] for i in range(len(spots_s))]
    spots_s = np.concatenate(spots_s, axis=0)
    
    #experiment = Experiment.from_json(json_path)
    codebook = Codebook()
    codebook = codebook.open_json(codebook_json)
    barcodes_01 = np.swapaxes(np.array(codebook), 1, 2)
    try:
        out = post_decfunc.decoding_function(
            spots_s, barcodes_01, print_training_progress=False)
        df_class_names = np.concatenate(
            (codebook.target.values,
             ['infeasible','background','nan']))
    
        postcode_decoded_df = post_decfunc.decoding_output_to_dataframe(
            out, df_class_names, df_class_names)
        ##############################
        prob_threshold = 0.7
        empty_barcodes = [
            'ABCA1', 'CDKN1A', 'CYP51A1', 'DHCR24',
            'FDFT1', 'HMGCR', 'HMMR','INSIG1',
            'LDLR', 'LIF', 'MYLIP', 'PIF1',
            'PLK1', 'SCD5', 'ACTB', 'GAPDH'
        ]

        spot_table = pd.DataFrame()

        spot_table['target_postcode'] = postcode_decoded_df.Name.values
        spot_table['postcode_probability'] = postcode_decoded_df.Probability.values

        spot_table['passes_thresholds_postcode'] = True
        non_decoded = ['infeasible', 'background', 'nan']
        spot_table.loc[
            spot_table['target_postcode'].isin(non_decoded),
            'passes_thresholds_postcode'] = False
        spot_table.loc[
            spot_table['target_postcode'].isna(),
            'passes_thresholds_postcode'] = False
        spot_table.loc[
            spot_table['postcode_probability'] <= prob_threshold,
            'passes_thresholds_postcode'] = False

        if empty_barcodes is not None:
            if 'passes_thresholds_postcode' in spot_table:
                spot_table['decoded_spots'] = spot_table[
                    'passes_thresholds_postcode']
                spot_table.loc[
                    spot_table['target_postcode'].isin(empty_barcodes),
                    'decoded_spots'] = False
            else:
                spot_table['decoded_spots'] = spot_table[
                    'passes_thresholds']
                spot_table.loc[
                    spot_table['target'].isin(empty_barcodes),
                    'decoded_spots'] = False
        # spot_table.to_csv('postcode_output.csv', index=False)
        ###############################
        # postcode_decoded_df.to_csv('postcode_output.csv', index=False)
        starfish_decoded_table['Probability'] = spot_table['postcode_probability'] 
        starfish_decoded_table['target_postcode'] = spot_table['target_postcode']
        starfish_decoded_table['passes_thresholds_postcode'] = spot_table['passes_thresholds_postcode']
        starfish_decoded_table['decoded_spots'] = spot_table['decoded_spots']
        starfish_decoded_table.to_csv('postcode_starfish_output.csv', index=False)

    except:
        with open('postcode_decoding.csv', 'w+') as fh:
            fh.writelines('PoSTcode failed')
    
    #return postcode_decoded_df
    
if __name__ == "__main__":
    cli = {
        "run": postcode_decoder
    }
    fire.Fire(cli)
