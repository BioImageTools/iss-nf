import os
import random
import numpy as np
import tifffile as tif
import re
import statistics
import pandas as pd
import fire

def data_collection(table_path):

    components = table_path.split('/')
    filename = components[-1]
    fov_name = filename.split('-')[0]
    last_part = filename.split('-')[-1]
    threshold = float(last_part[:-4])

    df_general = pd.DataFrame(columns=['threshold', '#Detected', '#Decoded', 'Percent', 'FDR'])

    df = pd.read_csv(table_path)

    filtered_df = df[df['passes_thresholds']==True]
    filtered_df = filtered_df[~filtered_df['target'].isin(empty_barcodes)]
    filtered_df = filtered_df[~filtered_df['target'].isin(remove_genes)]
    filtered_df = filtered_df[~filtered_df['target'].isin(invalid_codes)]

    total_filtered_count = len(filtered_df)
    empty_barcodes_count = df[df['target'].isin(empty_barcodes)].shape[0]
    invalid_codes_count = df[df['target'].isin(invalid_codes)].shape[0]

    df_general = df_general.append({'threshold': threshold,
                '#Detected': len(df),
                '#Decoded': total_filtered_count,
                'Percent': total_filtered_count/len(df) * 100,
                'FDR': get_fdr(empty_barcodes_count, len(df))}, ignore_index=True)

    threshold = df_general['threshold']
    detected_spots = df_general['#Detected']
    decoded_spots = df_general['#Decoded']
    false_discovery_rates = df_general['FDR']

    threshold_str = str(last_part[:-4])
    df_general.to_csv(f'df_general_{fov_name}-{threshold_str}.csv', index=False)  
        
        
if __name__ == "__main__":
    
    cli = {
        "data_collect": data_collection,
    }
    fire.Fire(cli)