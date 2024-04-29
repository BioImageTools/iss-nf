import numpy as np
import sys

def concat_npy(
    npy_files
):           
    sorted_spots = sorted(npy_files)
    spots_numpy = [np.load(spot_matrix) for spot_matrix in sorted_spots]
    spots_postcode_input = []
    for data_to_trace in spots_numpy:
        spots_postcode_input.append(np.swapaxes(data_to_trace.data, 1, 2))
    spots_postcode_input = np.concatenate(spots_postcode_input, axis=0)
    np.savez('spots_postcode_input.npz', spots_postcode_input)

if __name__ == "__main__":
   
    npy_path = sys.argv[1:]
    concat_npy(npy_path)