#!/usr/bin/env python3
""" Codebook converter when given in CSV format"""

import numpy as np
import pandas as pd
import fire
from starfish import Codebook


"""
Codebook CSV needs to have 'target' and 'barcode' as column names. Sequences are expected to start with 1, not 0.
"""

#------------------------------

def flatten_list(l: list):
    return [item for sublist in l for item in sublist]

def create_code(arr_rnd_ch: np.array):
    indices = [str(int(np.where(row == 1)[0]+1)) for row in arr_rnd_ch]
    return ','.join(indices)

def json2csv(json_file_path):
    codebook = Codebook()
    codebook = Codebook.open_json(json_file_path)
    with open('codebook_json2csv.csv', 'w+') as fh:
        fh.writelines('target,barcode\n')
        for gene_idx, gene in enumerate(list(codebook.coords['target'].data)):
            code_string = create_code(codebook.data[gene_idx])
            fh.writelines(','.join([gene, code_string]) + '\n')

def csv2json(csv: str):
    raw_codebook = pd.read_csv(csv)

    round_ch_list = list((str(raw_codebook.loc[:].barcode[i])) for i in range(len(raw_codebook)))
    #print('Number of rounds: {}'.format())
    channel_set = set(flatten_list(round_ch_list))
    #print(channel_set)
    
    # Get min value to set zero as first channel:
    min_ch = min([int(i) for i in channel_set])
    round_num = len(round_ch_list[0])
    print('Total number of rounds: {}'.format(round_num))
    ch_num = max([int(i) for i in channel_set])
    print('Number of channels: {}'.format(ch_num))
    # Map channels to numpy array:
    codebook_data = np.zeros((len(raw_codebook.target), round_num, ch_num)).astype(int)
    print('Shape of codebook: {}'.format(codebook_data.shape))

    for g in range(len(raw_codebook.target)):
        for r in range(round_num):
            index = int(round_ch_list[g][r]) - min_ch
            codebook_data[g, r, index] = 1
        #print(codebook_data[g])
    #data = np.zeros((len(raw_codebook), ))

    # Make codebook:
    cb = Codebook.from_numpy(list(raw_codebook.target), n_channel=len(channel_set), n_round = round_num, data=codebook_data)
    cb.to_json('codebook_csv2json.json')
    return None#[codebook_data]

def convert_codebook(codebook_path):
    if '.json' in codebook_path:
        json2csv(codebook_path)
    elif 'csv' in codebook_path:
        csv2json(codebook_path)
    else:
        print('WARNING: Codebook is not in proper format!!! Check documentation ;)')


#----------------------------------
if __name__ == '__main__':
    cli = {
        "run": convert_codebook
    }
    fire.Fire(cli)