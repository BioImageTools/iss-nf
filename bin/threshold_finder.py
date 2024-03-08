import numpy as np
import pandas as pd
import fire

empty_barcodes = [
    'ABCA1', 'CDKN1A', 'CYP51A1', 'DHCR24',
    'FDFT1', 'HMGCR', 'HMMR', 'INSIG1',
    'LDLR', 'LIF', 'MYLIP', 'PIF1',
    'PLK1', 'SCD5', 'ACTB', 'GAPDH'
]

remove_genes = ['IGHA1', 'IGHG1', 'IGHD', 'IGHM']

invalid_codes = ['NaN']

def select_best_threshold1(thresholds, detected_spots, decoded_spots, false_discovery_rates):

    best_fdr = float('inf')
    best_threshold = None

    for i, threshold in enumerate(thresholds):
        fdr = false_discovery_rates[i]

        if fdr < best_fdr:
            best_fdr = fdr
            best_threshold = threshold
        elif fdr == best_fdr:
            if decoded_spots[i] > decoded_spots[i]:
                best_threshold = threshold
            elif decoded_spots[i] == decoded_spots[i]:
                if detected_spots[i] > detected_spots[i]:
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


def get_fdr(empties, total, n_gene_panel=242, n_emptyBarcodes=16):
    return (empties / total) * (n_gene_panel / n_emptyBarcodes)


def auto_threshold(*args):
        

        df_general = pd.DataFrame(columns=['threshold', '#Detected', '#Decoded', 'Percent', 'FDR'])

        for path in args:
            
            components = path.split('/')
            filename = components[-1]
            fov_name = filename.split('-')[0]
            last_part = filename.split('-')[-1]
            threshold = float(last_part[:-4])

            df = pd.read_csv(path)

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

        with open('picked_threshold.txt', 'w') as file:
                file.write(str(mode_first(arr)))
        
    
if __name__ == "__main__":
    
    cli = {
        "find_threshold": auto_threshold,
    }
    fire.Fire(cli)
