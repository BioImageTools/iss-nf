import numpy as np
import fire
from starfish import Codebook
import postcode.decoding_functions as post_decfunc
import pandas as pd
import exp_metadata_json as exp_meta


def postcode_decoder(
    experiment_metadata_json,
    codebook_json,
    starfish_decoded_table,
    spots_postcode_input
):
    ExpJsonParser = exp_meta.ExpJsonParser(experiment_metadata_json)
    empty_barcodes = ExpJsonParser.meta['empty_barcodes']
    try:
        remove_genes = ExpJsonParser.meta["remove_genes"]
    except:
        remove_genes = []
    invalid_codes = ExpJsonParser.meta["invalid_codes"]

    starfish_decoded_table = pd.read_csv(starfish_decoded_table)
    spots_postcode_input = np.load(spots_postcode_input)
    spots_postcode_input = spots_postcode_input['arr_0']

    codebook = Codebook()
    codebook = codebook.open_json(codebook_json)
    barcodes_01 = np.swapaxes(np.array(codebook), 1, 2)

    try:
        out = post_decfunc.decoding_function(
            spots_postcode_input, barcodes_01, print_training_progress=False)
        df_class_names = np.concatenate(
            (codebook.target.values,
                ['infeasible','background','nan']))

        postcode_decoded_df = post_decfunc.decoding_output_to_dataframe(
            out, df_class_names, df_class_names)
        ##############################
        prob_threshold = 0.7

        spot_table = pd.DataFrame()

        spot_table['target_postcode'] = postcode_decoded_df.Name.values
        spot_table['postcode_probability'] = postcode_decoded_df.Probability.values
        spot_table['passes_thresholds_postcode'] = True

        spot_table.loc[
            spot_table['target_postcode'].isin(invalid_codes),
            'passes_thresholds_postcode'] = False
        spot_table.loc[
            spot_table['target_postcode'].isin(remove_genes),
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


        starfish_decoded_table['Probability'] = spot_table['postcode_probability'] 
        starfish_decoded_table['target_postcode'] = spot_table['target_postcode']
        starfish_decoded_table['passes_thresholds_postcode'] = spot_table['passes_thresholds_postcode']
        starfish_decoded_table['decoded_spots'] = spot_table['decoded_spots']
        starfish_decoded_table.to_csv('postcode_starfish_output.csv', index=False)

    except:
        with open('postcode_decoding_failed.csv', 'w+') as fh:
            fh.writelines('PoSTcode failed: Negative eigenvalues affect the covariance matrix utilized in multivariate normal distribution, requiring it to be positive definite when employed by the PostCode.')
    
if __name__ == "__main__":
   
    cli = {
        "run": postcode_decoder
    }
    fire.Fire(cli)
