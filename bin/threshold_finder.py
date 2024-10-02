import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import exp_metadata_json as exp_meta
import fire

def plot_report(results, picked_threshold, genePanelOnemptyBarcode_ratio):
    plt.figure(figsize=(10, 8))
    
    for index, row in results.iterrows():
        fov = row['fov']
        thresholds = row['threshold']
        ratios = [r * genePanelOnemptyBarcode_ratio for r in row['ratio']]
        decoded_spots = row['#Decoded']
        plt.scatter(thresholds, ratios, c=decoded_spots, cmap='viridis', s=np.array(decoded_spots)*0.01)
        for threshold, ratio, spots in zip(thresholds, ratios, decoded_spots):
            plt.text(threshold, ratio, fov, fontsize=9, ha='right', va='bottom')
    
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

def find_special_element1(pairs):
    pairs.sort(key=lambda x: x[0], reverse=True)
    first_elements = [pair[0] for pair in pairs]
    median_value = np.median(first_elements)
    return median_value#pairs[0][0]

def find_special_element2(elements):
    sorted_by_second = sorted(elements, key=lambda x: (-x[2], x[1], -x[0]))
    filtered_data = []
    zero_encountered = False

    for obj in sorted_by_second:
        if obj[1] == 0.0:
            if not zero_encountered:
                filtered_data.append(obj)
                zero_encountered = True
        else:
            filtered_data.append(obj)

    top_5_lowest_second = filtered_data[:5]
    sorted_top_5_by_third = sorted(top_5_lowest_second, key=lambda x: x[2], reverse=True)
    threshold = max(obj[0] for obj in sorted_top_5_by_third)
    return threshold
    
def select_best_threshold(thresholds, ratios, expected_accuracy, genePanelOnemptyBarcode_ratio, decoded_spots, detected_spots):
   
    picked_threshold1 = []
    picked_threshold2 = []
    
    for ratio, threshold, decode, detect in zip(ratios, thresholds, decoded_spots, detected_spots):
        if  expected_accuracy is not None and ratio < expected_accuracy/genePanelOnemptyBarcode_ratio:
            picked_threshold1.append([threshold, ratio])
        picked_threshold2.append([threshold, ratio, decode/detect])
    if picked_threshold1:
        lowest_threshold = find_special_element1(picked_threshold1)
    else:
        lowest_threshold = find_special_element2(picked_threshold2)

    return lowest_threshold

def get_ratio(empties, total):
    return (empties / total) 

def auto_threshold(experiment_metadata_json, *args):
    
    ExpJsonParser = exp_meta.ExpJsonParser(experiment_metadata_json)
    empty_barcodes = ExpJsonParser.meta['empty_barcodes']
    try:
        expected_accuracy = ExpJsonParser.meta['expected_accuracy']
    except:
        expected_accuracy = None
    try:
        remove_genes = ExpJsonParser.meta["remove_genes"]
    except:
        remove_genes = []

    invalid_codes = ExpJsonParser.meta["invalid_codes"]        
    n_genesPanel = ExpJsonParser.meta["total_number_genes"]
    
    empty_n = len(empty_barcodes)
    if len(remove_genes) != 0: 
        panel_n = (n_genesPanel - len(remove_genes) + empty_n)
    else:
        panel_n = (n_genesPanel + empty_n)
        
    genePanelOnemptyBarcode_ratio = (panel_n / empty_n)

    df_general = pd.DataFrame(columns=['fov', 'threshold', 'ratio', '#Decoded', '#Detected'])

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
        empty_barcodes_count = df[df['target'].isin(empty_barcodes)].shape[0]
        total_filtered_count = len(filtered_df)

        try:
            df_general = df_general.append({
                '#Detected': len(df),
                'fov': fov_name,
                'threshold': threshold,
                '#Decoded': total_filtered_count,
                'ratio': get_ratio(empty_barcodes_count, len(df))}, ignore_index=True)
        except:
            pass
    df_general.to_csv('df_general.csv', index=False)
    results = df_general.groupby('fov').agg({
    'threshold': lambda x: x.tolist(),
    'ratio': lambda x: x.tolist(),
    '#Decoded': lambda x: x.tolist(),
    '#Detected': lambda x: x.tolist()
    }).reset_index()
    scores = []
    for index, row in results.iterrows():
        fov_name = row['fov']
        thresholds = row['threshold']
        ratios = row['ratio']
        decoded_spots = row['#Decoded']
        detected_spots = row['#Detected']
        scores.append(select_best_threshold(thresholds, ratios, expected_accuracy, genePanelOnemptyBarcode_ratio, decoded_spots, detected_spots))
    picked_threshold = np.max(scores)

    plot_report(results, picked_threshold, genePanelOnemptyBarcode_ratio)

    with open('picked_threshold.txt', 'w') as file:
            file.write(str(picked_threshold))
        
    
if __name__ == "__main__":

    cli = {
        "autocompute_thr": auto_threshold
    }
    fire.Fire(cli)
