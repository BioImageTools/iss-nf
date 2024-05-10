import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import sys
import json

def plot_report(results, picked_threshold):
    plt.figure(figsize=(10, 8))
    
    for index, row in results.iterrows():
        fov = row['fov']
        thresholds = row['threshold']
        fdrs = row['FDR']
        decoded_spots = row['#Decoded']
        plt.scatter(thresholds, fdrs, c=decoded_spots, cmap='viridis', s=np.array(decoded_spots)*0.01)
        for threshold, fdr, spots in zip(thresholds, fdrs, decoded_spots):
            plt.text(threshold, fdr, fov, fontsize=9, ha='right', va='bottom')
    
    cbar = plt.colorbar(label='Number of Decoded')
    
    plt.title('Scatter Plot of Thresholds vs. FDRs Colored by Number of Decoded')
    plt.xlabel('Thresholds')
    plt.ylabel('FDRs')
    plt.xscale('log')
    plt.axvline(x=picked_threshold, color='r', ls='--', label=f'Picked threshold - {picked_threshold}')
    plt.legend()
    qc_path = os.getcwd()
    output_plot_path = os.path.join(qc_path, "picked_thresh_plot.png")
    plt.savefig(output_plot_path, bbox_inches='tight')
    plt.show()
    plt.close() 

    with open(output_plot_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    html_content = f"""
    <html>
    <head>
    <title>QC Plot</title>
    </head>
    <body>
    <h1>QC Plot</h1>
    <p>This plot shows how the threshold is chosen based on the number of decoded vs FDR for all three chosen tiles.</p>
    <img src="data:image/png;base64,{encoded_string}" alt="QC Plot">
    </body>
    </html>
    """
    output_html_path = os.path.join(qc_path, "4-thresh_qc.html")
    with open(output_html_path, 'w') as f:
        f.write(html_content)

# def score(fdr_percentage, decoded_spots, fdr_weight=0.4):
#     return (1 - fdr_weight) * decoded_spots - fdr_weight * fdr_percentage

# def select_best_threshold(thresholds, fdrs, decoded_spots, fdr_weight=0.5):

#     best_score = float('-inf')
#     best_threshold = None

#     for threshold, fdr, spots in zip(thresholds, fdrs, decoded_spots):
#         fdr_percentage = fdr * 100 
#         s = score(fdr_percentage, spots, fdr_weight)
#         if s > best_score:
#             best_score = s
#             best_threshold = threshold

#     return best_threshold
def normalize(values):
    
    min_val = min(values)
    max_val = max(values)
    normalized_values = [(val - min_val) / (max_val - min_val) for val in values]
    return normalized_values

def score(fdr_percentage, decoded_spots, fdr_weight, decoded_weight):
    
    return decoded_weight * decoded_spots - fdr_weight * fdr_percentage

def select_best_threshold(thresholds, fdrs, decoded_spots, fdr_weight=0.6, decoded_weight=0.4):

    normalized_fdrs = normalize(fdrs)
    normalized_decoded_spots = normalize(decoded_spots)

    scores = [score(fdr, spots, fdr_weight, decoded_weight) for fdr, spots in zip(normalized_fdrs, normalized_decoded_spots)]

    knee_point_index = knee_point_detection(scores)
    best_threshold = thresholds[knee_point_index]

    return best_threshold

def knee_point_detection(scores):

    scores = np.array(scores)
    scores = scores / np.max(scores) 

    knee_point_index = None
    max_distance = 0

    for i in range(1, len(scores)):
        distance = abs(scores[i] - scores[0]) + abs(scores[-1] - scores[i])
        if distance > max_distance:
            max_distance = distance
            knee_point_index = i

    return knee_point_index

def mode_first(data):
    
    frequency = {}
    for item in data:
        frequency[item] = frequency.get(item, 0) + 1
    
    max_frequency = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_frequency]
    
    return modes[0] if modes else None


def get_fdr(empties, total, n_genesPanel, empty_barcodes, remove_genes):

    empty_n = len(empty_barcodes)
    if remove_genes is not None: 
        panel_n = (n_genesPanel - len(remove_genes) + empty_n)
    else:
        panel_n = (n_genesPanel + empty_n)
    
    return (empties / total) * (panel_n / empty_n)

def auto_threshold(n_genesPanel, empty_barcodes, remove_genes, invalid_codes, *args):
    
    empty_barcodes = json.load(open(empty_barcodes, 'r'))
    remove_genes   = json.load(open(remove_genes, 'r'))
    invalid_codes  = json.load(open(invalid_codes, 'r')) 

    df_general = pd.DataFrame(columns=['fov', 'threshold', '#Detected', '#Decoded', 'Percent', 'FDR'])

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

        df_general = df_general.append({
            'fov': fov_name,
            'threshold': threshold,
            '#Detected': len(df),
            '#Decoded': total_filtered_count,
            'Percent': total_filtered_count/len(df) * 100,
            'FDR': get_fdr(empty_barcodes_count, len(df), n_genesPanel, empty_barcodes, remove_genes)}, ignore_index=True)

    results = df_general.groupby('fov').agg({
    'threshold': lambda x: x.tolist(),
    'FDR': lambda x: x.tolist(),
    '#Decoded': lambda x: x.tolist()
    }).reset_index()
    scores = []
    for index, row in results.iterrows():
        fov_name = row['fov']
        thresholds = row['threshold']
        fdrs = row['FDR']
        decoded_spots = row['#Decoded']
        scores.append(select_best_threshold(thresholds, fdrs, decoded_spots))
    picked_threshold = mode_first(scores)
    plot_report(results, picked_threshold)

    with open('picked_threshold.txt', 'w') as file:
            file.write(str(picked_threshold))
        
    
if __name__ == "__main__":
    import fire
    cli = {
        "autocompute_thr": auto_threshold
    }
    fire.Fire(cli)
    # n_genesPanel = int(sys.argv[1])
    # empty_barcodes = (sys.argv[2])
    # remove_genes = (sys.argv[3])
    # invalid_codes = (sys.argv[4])
    # csv_paths = (sys.argv[5])
    # auto_threshold(n_genesPanel, empty_barcodes, remove_genes, invalid_codes, csv_paths)