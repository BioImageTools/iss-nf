import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import plotly.graph_objects as go
import sys
import base64
import seaborn as sns
from matplotlib.lines import Line2D


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

    ax.scatter(data[x_col], data[y_col], s=point_size, alpha=alpha,
               color=others_color,
               # color='k',
               label='Others')

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

    ###################################################
    COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']
    decoding_method = 'postcode'
    """
    gene_colors = {
        'COL1A2': COLORS[5],
        'CD4': COLORS[4],
        'KRT5': COLORS[0],
        'EPCAM': COLORS[0],
    }
    """
    gene_colors = {
        'Gapdh': COLORS[5],
        'Penk': COLORS[4],
        'Plpp4': COLORS[0],
        'Cux2': COLORS[0],
    }

    spots_for_scatter = filter_results(
        df, decoding_method, column_map, empty_barcodes, remove_genes)[0].set_index(column_map['target'][decoding_method])

    legend_location = 'upper left'
    scalebar_location = 'lower left'

    fig, ax = plt.subplots(figsize=(12, 8))

    scatter_plot(
        ax, spots_for_scatter, gene_cm=gene_colors, x_col='xc', y_col='yc',
        pixel_size=MICROM_PER_PX, despine=True,
        point_size=0.5, alpha=0.1, 
        others_color='k',  
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
    plt.savefig('Spatial_Distribution_Gene_Expression.png')
    plt.close()

    ###################################################### 
    non_decoded_spots = df['target_postcode'][~df['decoded_spots']]

    non_decoded_spots[
        ~(non_decoded_spots.str.contains('nan|infeasible|background|' + '|'.join(empty_barcodes)) |
          non_decoded_spots.isna())] = 'Low probability'

    non_decoded_spots[non_decoded_spots.isin(empty_barcodes)] = 'Empty barcodes'

    fig = go.Figure(go.Bar(
        x=non_decoded_spots.value_counts(dropna=False).index,
        y=non_decoded_spots.value_counts(dropna=False).values,
        marker=dict(color=non_decoded_spots.value_counts(dropna=False).values, colorscale='Viridis'),
    ))

    fig.update_layout(
        title='Non-decoded PoSTcode spot counts',
        xaxis=dict(title='Spot'),
        yaxis=dict(title='Count'),
    )
    #####################################################

    filtered_spots = df[df['decoded_spots']].set_index('target_postcode')
    gene_counts = filtered_spots.groupby(filtered_spots.index).count()['xc'].sort_values(ascending=False)

    hks = ['RPLP0', 'GUSB']
    gene_counts_subset = gene_counts[gene_counts.index.isin(hks)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=gene_counts_subset.index,
        y=gene_counts_subset.values,
        marker_color=['darkcyan', 'darkgreen'],
        text=[f'Total: {count}' for count in gene_counts_subset.values],
        hoverinfo='text'
    ))

    fig.update_layout(
        title='Gene Spot Counts',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='Spot Counts'),
        xaxis_tickangle=-45,
    )

    #####################################################

    def convert_palette_to_plotly(palette):
        rgb_values = sns.color_palette(palette).as_hex()
        return [f'rgb({int(r[1:3], 16)},{int(r[3:5], 16)},{int(r[5:], 16)})' for r in rgb_values]

    custom_palette = sns.color_palette("coolwarm", as_cmap=True)

    def convert_palette_to_plotly(palette):
        rgb_values = palette(range(256))
        return [f'rgb({int(r[0]*255)},{int(r[1]*255)},{int(r[2]*255)})' for r in rgb_values]

    gene_count_subset_top = gene_counts.iloc[:26]
    fig_top = go.Figure(go.Bar(
        x=gene_count_subset_top.index,
        y=gene_count_subset_top.values.flatten(),
        marker_color=convert_palette_to_plotly(custom_palette),
    ))
    fig_top.update_layout(
        title='Top 25 Genes by % Total Spots',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='% Total Spots'),
    )
    #####################################################
    custom_palette = sns.color_palette("coolwarm", as_cmap=True)

    def convert_palette_to_plotly(palette):
        rgb_values = palette(range(256))
        return [f'rgb({int(r[0]*255)},{int(r[1]*255)},{int(r[2]*255)})' for r in rgb_values]

    gene_count_subset_bottom = gene_counts.iloc[-25:]
    fig_bottom = go.Figure(go.Bar(
        x=gene_count_subset_bottom.index,
        y=gene_count_subset_bottom.values.flatten(),
        marker_color=convert_palette_to_plotly(custom_palette),
    ))
    fig_bottom.update_layout(
        title='Bottom 25 Genes by % Total Spots',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='% Total Spots'),
    )
    #####################################################
    df2 = df[df['passes_thresholds_postcode']==True].set_index('target_postcode')

    def get_lob(blanks):
        return np.mean(blanks) + (1.645 * np.std(blanks))

    housekeepers = ['RPLP0', 'GUSB']

    df2 = df2.groupby(df2.index).count().sort_values('xc', ascending=False)
    df2['i'] = range(df2.shape[0])

    empty_barcode_counts = df2[df2.index.isin(empty_barcodes)]
    lob = get_lob(empty_barcode_counts.iloc[:, 0])
    housekeeper_counts = df2[df2.index.isin(housekeepers)]
    regular_target_counts = df2[~df2.index.isin(housekeepers)]
    regular_target_counts = regular_target_counts[~regular_target_counts.index.isin(empty_barcodes)]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(
        regular_target_counts['i'], regular_target_counts['xc'],
        s=12,
        facecolor='k',
        label='Targets',
    )
    ax.scatter(
        empty_barcode_counts['i'], empty_barcode_counts['xc'],
        s=36,
        facecolor='r',
        label='Empty barcodes',
    )
    ax.scatter(
        housekeeper_counts['i'], housekeeper_counts['xc'],
        s=36,
        facecolor='lightgreen',
        label='Housekeepers',
    )

    #plt.axhline(y=lob, color='r', linestyle='--', linewidth=0.5, label=f'LoB: {round(lob)} spots')

    ax.set_yscale('log')
    ax.set_title('PoSTcode results', fontsize=14)
    ax.set_ylabel('Spot counts', fontsize=14)
    ax.set_xlabel('Target panel', fontsize=14)
    ax.legend()
    plt.tight_layout() 
    plt.savefig('Postcode_Result.png')
    plt.close()

    #####################################################
    df3 = empty_barcode_counts.iloc[:, 0:1].rename(columns={empty_barcode_counts.columns[0]: 'Spot count'})

    fig = go.Figure(go.Bar(
        y=df3.index,
        x=df3['Spot count'],
        orientation='h', 
        marker_color='#FF7F50' 
    ))

    fig.update_layout(
        title='Spot counts for Empty Barcodes',
        xaxis=dict(title='Spot count'),
        yaxis=dict(title='Empty barcodes'),
    )
    #####################################################


    fig_non_decoded = go.Figure(go.Bar(
        x=non_decoded_spots.value_counts(dropna=False).index,
        y=non_decoded_spots.value_counts(dropna=False).values,
        marker=dict(color=non_decoded_spots.value_counts(dropna=False).values, colorscale='Viridis'),
    ))

    fig_non_decoded.update_layout(
        title='Non-decoded PoSTcode spot counts',
        xaxis=dict(title='Spot'),
        yaxis=dict(title='Count'),
        height=400, 
        width=600   
    )

    fig_gene_counts = go.Figure()

    fig_gene_counts.add_trace(go.Bar(
        x=gene_counts_subset.index,
        y=gene_counts_subset.values,
        marker_color=['darkcyan', 'darkgreen'],
        text=[f'Total: {count}' for count in gene_counts_subset.values],
        hoverinfo='text'
    ))

    fig_gene_counts.update_layout(
        title='Gene Spot Counts',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='Spot Counts'),
        xaxis_tickangle=-45,
        height=400,  
        width=600   
    )

    fig_top_genes = go.Figure(go.Bar(
        x=gene_count_subset_top.index,
        y=gene_count_subset_top.values.flatten(),
        marker_color=convert_palette_to_plotly(custom_palette),
    ))
    fig_top_genes.update_layout(
        title='Top 25 Genes by % Total Spots',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='% Total Spots'),
        height=400, 
        width=600   
    )

    fig_bottom_genes = go.Figure(go.Bar(
        x=gene_count_subset_bottom.index,
        y=gene_count_subset_bottom.values.flatten(),
        marker_color=convert_palette_to_plotly(custom_palette),
    ))
    fig_bottom_genes.update_layout(
        title='Bottom 25 Genes by % Total Spots',
        xaxis=dict(title='Genes'),
        yaxis=dict(title='% Total Spots'),
        height=400,  
        width=600    
    )

    fig_empty_barcodes = go.Figure(go.Bar(
        y=df3.index,
        x=df3['Spot count'],
        orientation='h',
        marker_color='#FF7F50'
    ))
    fig_empty_barcodes.update_layout(
        title='Spot counts for Empty Barcodes',
        xaxis=dict(title='Spot count'),
        yaxis=dict(title='Empty barcodes'),
        height=400, 
        width=600    
    )

    current_dir = os.getcwd()

    html_content = '<html><head><title>Interactive Decoding Plots</title></head><body>'

    html_content += '<h1>Non-decoded PoSTcode spot counts</h1>'
    html_content += fig_non_decoded.to_html(full_html=False, include_plotlyjs='cdn')

    html_content += '<h1>Gene Spot Counts</h1>'
    html_content += fig_gene_counts.to_html(full_html=False, include_plotlyjs='cdn')

    html_content += '<h1>Top 25 Genes by % Total Spots</h1>'
    html_content += fig_top_genes.to_html(full_html=False, include_plotlyjs='cdn')

    html_content += '<h1>Bottom 25 Genes by % Total Spots</h1>'
    html_content += fig_bottom_genes.to_html(full_html=False, include_plotlyjs='cdn')

    html_content += '<h1>Spot counts for Empty Barcodes</h1>'
    html_content += fig_empty_barcodes.to_html(full_html=False, include_plotlyjs='cdn')

    html_content += '</body></html>'

    # Generate HTML file
    plot_folder = os.getcwd()
    plot_files = sorted(os.listdir(plot_folder))
    current_dir = os.getcwd()
    table_html = df_general.to_html(index=False)

    html_content += '<h1>Here is the summary of the postcode decoding</h1>'
    html_content += table_html
    for plot_file in plot_files:
        if plot_file.endswith('.png'):
            plot_name = os.path.splitext(plot_file)[0]
            html_content += f'<h1>{plot_name}</h1>'
            with open(os.path.join(plot_folder, plot_file), 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                html_content += f'<div class="plot-container"><img src="data:image/png;base64,{img_base64}"></div>'
    html_content += '</body></html>'

    html_file_path = os.path.join(current_dir, 'decoding_plots.html')
    with open(html_file_path, 'w') as f:
        f.write(html_content)
        
if __name__ == "__main__":

    csv_path = (sys.argv[1])
    decoder_qc(csv_path)