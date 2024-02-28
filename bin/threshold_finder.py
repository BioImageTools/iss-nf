import os
import random
import numpy as np
import tifffile as tif
import re
import statistics
import pandas as pd

# should be checked if we use from . or: 
from spot_detection import find_spots
from decoder import decoder

empty_barcodes = [
    'ABCA1', 'CDKN1A', 'CYP51A1', 'DHCR24',
    'FDFT1', 'HMGCR', 'HMMR', 'INSIG1',
    'LDLR', 'LIF', 'MYLIP', 'PIF1',
    'PLK1', 'SCD5', 'ACTB', 'GAPDH'
]

remove_genes = ['IGHA1', 'IGHG1', 'IGHD', 'IGHM']

invalid_codes = ['infeasible', 'background', 'nan']

n_genesPanel = 246

if remove_genes is not None:
    n_gene_panel = n_genesPanel - len(remove_genes) + len(empty_barcodes)
else:
    n_gene_panel = n_genesPanel + len(empty_barcodes)
        
        
def select_best_threshold1(thresholds, detected_spots, decoded_spots, false_discovery_rates):

    best_fdr = float('inf')
    best_threshold = None

    for i, threshold in enumerate(thresholds):
        fdr = false_discovery_rates[i]

        if fdr < best_fdr:
            best_fdr = fdr
            best_threshold = threshold
        elif fdr == best_fdr:
            if decoded_spots[i] > decoded_spots[np.where(thresholds==best_threshold)]:
                best_threshold = threshold
            elif decoded_spots[i] == decoded_spots[np.where(thresholds==best_threshold)]:
                if detected_spots[i] > detected_spots[np.where(thresholds==best_threshold)]:
                    best_threshold = threshold

    return best_threshold


def select_best_threshold2(thresholds, detected_spots, decoded_spots, false_discovery_rates):

    best_score = float('-inf')
    best_threshold = None

    for i, threshold in enumerate(thresholds):
        score = -(2 * false_discovery_rates[i]**3) + (2*decoded_spots[i])

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold


def select_best_threshold3(thresholds, detected_spots, decoded_spots, false_discovery_rates):

    best_score = float('-inf')
    best_threshold = None

    for i, threshold in enumerate(thresholds):

        score = (decoded_spots[i]) - (false_discovery_rates[i] **3)

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold


def select_best_threshold4(thresholds, detected_spots, decoded_spots, false_discovery_rates):

    best_score = float('-inf')
    best_threshold = None

    for i, threshold in enumerate(thresholds):
        score = detected_spots[i] + decoded_spots[i] - false_discovery_rates[i]

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold


def mode_first(data):
    
    frequency = {}
    for item in data:
        frequency[item] = frequency.get(item, 0) + 1
    
    max_frequency = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_frequency]
    
    return modes[0] if modes else None


def tile_picker(imgs_path, numTiles=50):
    

    tiff_files = [f for f in os.listdir(imgs_path) if f.endswith('.tiff')]
    random_files = random.sample(tiff_files, numTiles)

    max_intensity = 0
    max_intensity_file = ''

    for file_name in random_files:

        image = tif.memmap(os.path.join(imgs_path, file_name))
        intensity = np.sum(image)

        if intensity > max_intensity:
            max_intensity = intensity
            max_intensity_file = file_name

    picked_tile = int(re.search(r'(?<=f)\d+', max_intensity_file).group(0))
    
    return picked_tile


def get_fdr(empties, total, n_gene_panel=246, n_emptyBarcodes=16):
    return (empties / total) * (n_gene_panel / n_emptyBarcodes)


def auto_threshold(tiles_path, json_path, n_tilePicker=50, min_thr=.0005, max_thr=.1, n_vals=30, filt_prob=.7,):
    
    tile = tile_picker(tiles_path, n_tilePicker)
    thresh_values = np.logspace(np.log10(min_thr), np.log10(max_thr), n_vals, base=10)
        
    results = []
    for threshold in thresh_values:
        spots = find_spots(json_path, test_tile_idx=[tile], threshold=threshold)
        results.append([threshold, decoder(spots, json_path, test_tile_idx=[tile])])

    df_general = pd.DataFrame(columns=['threshold', '#Detected', '#Decoded', 'Percent', 'FDR'])

    for thresh, result in results:

        df = pd.DataFrame(result)
        filtered_df = df[df['Probability'] > filt_prob]
        filtered_df = filtered_df[~filtered_df['Code'].isin(empty_barcodes)]
        filtered_df = filtered_df[~filtered_df['Code'].isin(remove_genes)]
        filtered_df = filtered_df[~filtered_df['Code'].isin(invalid_codes)]

        total_filtered_count = len(filtered_df)
        empty_barcodes_count = df[df['Code'].isin(empty_barcodes)].shape[0]
        invalid_codes_count = df[df['Code'].isin(invalid_codes)].shape[0]
        
        df_general = df_general.append({'threshold': thresh,
                    '#Detected': len(df),
                    '#Decoded': total_filtered_count,
                    'Percent': total_filtered_count/len(df) * 100,
                    'FDR': get_fdr(empty_barcodes_count, len(df), n_gene_panel)}, ignore_index=True)

    thresholds = df_general['threshold']
    detected_spots = df_general['#Detected']
    decoded_spots = df_general['#Decoded']
    false_discovery_rates = df_general['FDR']
    
    arr = [
        select_best_threshold1(thresholds, detected_spots, decoded_spots, false_discovery_rates),
        select_best_threshold2(thresholds, detected_spots, decoded_spots, false_discovery_rates),
        select_best_threshold3(thresholds, detected_spots, decoded_spots, false_discovery_rates),
        select_best_threshold4(thresholds, detected_spots, decoded_spots, false_discovery_rates),
    ]

    return mode_first(arr)
                    

    
if __name__ == "__main__":
    
    cli = {
        "run_threshold": auto_threshold,
    }
    fire.Fire(cli)
