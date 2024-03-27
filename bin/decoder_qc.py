import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.lines import Line2D
import seaborn as sns
import sys
import base64

empty_barcodes = [
    'ABCA1', 'CDKN1A', 'CYP51A1', 'DHCR24',
    'FDFT1', 'HMGCR', 'HMMR', 'INSIG1',
    'LDLR', 'LIF', 'MYLIP', 'PIF1',
    'PLK1', 'SCD5', 'ACTB', 'GAPDH'
]

remove_genes = ['IGHA1', 'IGHG1', 'IGHD', 'IGHM']

invalid_codes = ['infeasible', 'background', 'nan']

MICROM_PER_PX = 0.1625

def print_in_a_box(text, margin=5):
    print('', '_' * (len(text) + (margin * 2)))
    print(f'|{" " * (len(text) + (margin * 2))}|')
    print(f'|{" " * margin}{text}{" " * margin}|')
    print(f'|_{"_" * (len(text) + (margin * 2) - 1)}|')

def scatter_plot(ax, data, gene_cm, x_col='X', y_col='Y', pixel_size=None,
                 despine=True, plot_title='', point_size=2, alpha=1,
                 others_color='lightgrey', background_color='white',
                 legend_loc='center left', scalebar_loc='upper right',
                 scalebar_box_alpha=0):
    def _despine(ax):
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color('none')
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
        return ax

    # Plot all
    ax.scatter(data[x_col], data[y_col], s=point_size, alpha=alpha,
               color=others_color,
               # color='k',
               label='Others')

    # Plot subset
    for gene in gene_cm:
        gene_data = data.loc[gene]
        ax.scatter(gene_data[x_col], gene_data[y_col], s=point_size, alpha=alpha,
                   color=gene_cm[gene], label=gene)
        
    if legend_loc is not None:
        lgnd = ax.legend(loc=legend_loc, ncol=1)
        for handle in lgnd.legendHandles:
            handle.set_sizes([50])

    if pixel_size is not None:
        scalebar = ScaleBar(dx=pixel_size, units='um', location=scalebar_loc,
                            box_alpha=scalebar_box_alpha)
        ax.add_artist(scalebar)
    plt.title(plot_title)

    if despine:
        ax = _despine(ax)
    
    ax.set_facecolor(background_color)

    return ax

def filter_results(spots, decoding_method, column_map, empty_barcodes=None, remove_gene=None):
    """
    Collect filtered results of chosen decoded method (either PoSTcode or Starfish).
    """
    if remove_gene is not None: 
        
        spots = spots[spots[column_map['passes_thresholds'][decoding_method]] & \
                                        ~spots[column_map['target'][decoding_method]].isin(remove_genes)]
    else:   
        spots = spots[spots[column_map['passes_thresholds'][decoding_method]]]
    
    if empty_barcodes is not None:
        empty_barcode_spots = spots[spots[column_map['target'][decoding_method]].isin(empty_barcodes)]

    return spots, empty_barcode_spots

def get_fdr(empties, total, n_genesPanel=246):

    empty_n = len(empty_barcodes)
    if remove_genes is not None: 
        panel_n = (n_genesPanel - len(remove_genes) + empty_n)
    else:
        panel_n = (n_genesPanel + empty_n)
    
    return (empties / total) * (panel_n / empty_n)

def decoder_qc(table):
          
    df_general = pd.DataFrame(columns=['#Detected', '#Decoded', 'Percent', 'FDR%'])

    df = pd.read_csv(table)
    filtered_df = df[df['passes_thresholds_postcode']==True]
    filtered_df = filtered_df[~filtered_df['target_postcode'].isin(empty_barcodes)]
    filtered_df = filtered_df[~filtered_df['target_postcode'].isin(remove_genes)]
    filtered_df = filtered_df[~filtered_df['target_postcode'].isin(invalid_codes)]

    total_filtered_count = len(filtered_df)
    empty_barcodes_count =  df[df['passes_thresholds_postcode'] & \
                                        df['target_postcode'].isin(empty_barcodes)]
    invalid_codes_count = df[df['target_postcode'].isin(invalid_codes)].shape[0]
    total = df[df['passes_thresholds_postcode']]
    
    df_general = df_general.append({
                '#Detected': len(df),
                '#Decoded': total_filtered_count,
                'Percent': total_filtered_count/len(df) * 100,
                'FDR%': get_fdr(empty_barcodes_count.shape[0], total.shape[0]) *100}, ignore_index=True)
    
    df_general = df_general.fillna(0)  
    metrics = ['# Detected', '# Decoded', 'Percent', 'FDR%']
    values = df_general.iloc[0].tolist() 

    plt.figure(figsize=(10, 6))
    plt.plot(metrics, values, marker='o', color='darkcyan') 
    plt.title('Metrics Summary')
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.grid(True)

    for i, value in enumerate(values):
        plt.text(i, value, str(round(value, 2)), ha='center', va='bottom', color='black')

    plt.tight_layout()
    plt.savefig('0-metrics_summary.png')
    plt.close()
    
    detected_spots = df_general['#Detected']
    decoded_spots = df_general['#Decoded']
    false_discovery_rates = df_general['FDR%']

    non_decoded_spots = df['target_postcode'][~df['decoded_spots']]

    non_decoded_spots[
        ~(non_decoded_spots[:, ].isin(['nan', 'infeasible', 'background'] + empty_barcodes) |
         non_decoded_spots[:, ].isna())] = 'Low probability'

    non_decoded_spots[non_decoded_spots.isin(empty_barcodes)] = 'Empty barcodes'

    plt.figure(figsize=(8, 6))
    colors = plt.cm.Paired(range(len(non_decoded_spots)))
    ax = non_decoded_spots.value_counts(dropna=False).plot(
        kind='bar', color=colors
    )

    plt.xlabel('Spot')
    plt.ylabel('Count')
    plt.title('Non-decoded PoSTcode spot counts', fontsize=16)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('1-non_decoded_spot_counts.png')
    plt.close()
       
    ###################################################
    decoding_methods = ['starfish', 'postcode']

    column_map = {}
    column_map['target'] = {}
    column_map['passes_thresholds'] = {}

    for col_type in column_map:
        for method in decoding_methods:
            if method == 'starfish':
                column_map[col_type][method] = col_type
            else:
                column_map[col_type][method] = col_type + '_' + method
    ####################################################
   
    COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']
    decoding_method = 'postcode'

    gene_colors = {
        'COL1A2': COLORS[5],
        'CD4': COLORS[4],
        'KRT5': COLORS[0],
        'EPCAM': COLORS[0],
    }

    spots_for_scatter = filter_results(
        df, decoding_method, column_map, empty_barcodes, remove_genes)[0].set_index(column_map['target'][decoding_method])

    legend_location = 'upper left'
    scalebar_location = 'lower left'

    fig, ax = plt.subplots(figsize=(12, 8))

    scatter_plot(
        ax, spots_for_scatter, gene_cm=gene_colors, x_col='xc', y_col='yc',
        pixel_size=MICROM_PER_PX, despine=True,
        point_size=1, alpha=0.3, 
        others_color='grey',  
        legend_loc=legend_location,
        scalebar_loc=scalebar_location,
    )

    plt.title("Spatial Distribution of Gene Expression") 
    plt.xlabel("X Coordinate") 
    plt.ylabel("Y Coordinate")  
    plt.gca().invert_yaxis() 

    plt.grid(True, linestyle='--', alpha=0.5)

    legend_elements = [Line2D([0], [0], marker='o', color='w', markersize=10, markerfacecolor=color, label=gene) for gene, color in gene_colors.items()]
    ax.legend(handles=legend_elements, loc=legend_location, title="Genes", title_fontsize='large')

    plt.gca().set_aspect('equal')  # Set aspect ratio to 'equal'
    plt.tight_layout() 
    plt.savefig('2-spatial_distribution_gene_expression.png')
    plt.close()
    ###################################################### 

    filtered_spots = df[df['decoded_spots']].set_index('target_postcode')
    gene_counts = filtered_spots.groupby(filtered_spots.index).count()['xc'].sort_values(ascending=False)

    hks = ['RPLP0', 'GUSB']

    gene_counts_subset = gene_counts[gene_counts.index.isin(hks)]

    plt.figure(figsize=(10, 6))
    bars = gene_counts_subset.plot(kind='bar', color=['darkcyan', 'darkgreen'])  # Change colors to dark mode colors

    for gene, count in gene_counts_subset.items():
        plt.text(hks.index(gene), count + 10, f'Total: {count}', ha='center', va='bottom', color='white')  # Adjust text color for visibility

    plt.title('Gene Spot Counts')
    plt.xlabel('Genes')
    plt.ylabel('Spot Counts')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('3-gene_spot_counts.png')
    plt.close()
    ########################################################
    
    gene_count_subset = gene_counts.iloc[:26]
    plt.figure(figsize=(12, 6))
    sns.barplot(x=gene_count_subset.index, y=gene_count_subset.values, palette="viridis")
    plt.title('Top 25 Genes by % Total Spots', fontsize=16)
    plt.ylabel('% Total Spots', fontsize=12)
    plt.xlabel('Genes', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for index, value in enumerate(gene_count_subset.values):
        plt.text(index, value + 0.5, f'{value:,.2f}%', ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig('4-top_25_genes_total_spots.png')
    plt.close()

    gene_count_subset = gene_counts.iloc[-25:]
    plt.figure(figsize=(12, 6))
    sns.barplot(x=gene_count_subset.index, y=gene_count_subset.values, palette="magma_r")
    plt.title('Bottom 25 Genes by % Total Spots', fontsize=16)
    plt.ylabel('% Total Spots', fontsize=12)
    plt.xlabel('Genes', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for index, value in enumerate(gene_count_subset.values):
        plt.text(index, value * 1.025, f'{value:,.2f}%', ha='center', fontsize=8)
    plt.tight_layout()
    plt.savefig('5-bottom_25_genes_total_spots.png')
    plt.close()

    ########################################################
    
    dff = df[df['passes_thresholds_postcode'] == True].set_index('target_postcode')
    dff = dff.groupby(dff.index).count().sort_values('xc', ascending=False)

    empty_barcode_counts = dff[dff.index.isin(empty_barcodes)]
    df = empty_barcode_counts.iloc[:, 0:1].rename(columns={empty_barcode_counts.columns[0]: 'Spot count'})

    plt.figure(figsize=(10, 8))
    bars = plt.barh(df.index, df['Spot count'], color='#FF7F50')  # Set color to orange
    plt.xlabel('Spot count')
    plt.ylabel('Empty barcodes')
    plt.title('Spot counts for Empty Barcodes')
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig('6-spot_counts_empty_barcodes.png')
    plt.close()
    
    ###########################################################

    plot_folder = os.getcwd()

    plot_files = sorted(os.listdir(plot_folder))

    # Get the current directory
    current_dir = os.getcwd()

    # Save all plots in an HTML file
    html_content = '<html><head><style>.plot-container { display: block; }</style></head><body>'
    for plot_file in plot_files:
        if plot_file.endswith('.png'):
            with open(os.path.join(plot_folder, plot_file), 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                html_content += f'<div class="plot-container"><img src="data:image/png;base64,{img_base64}"></div>'
    html_content += '</body></html>'

    # Write the HTML content to a file named "plots.html" in the current directory
    html_file_path = os.path.join(current_dir, '3-decoding_plots.html')
    with open(html_file_path, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":

    csv_path = (sys.argv[1])
    decoder_qc(csv_path)