import pandas as pd
import fire
import sys

def concat_csv(
    csv_files
):           
    print(csv_files)
    sorted_starfish_decoded = sorted(csv_files)
    print(sorted_starfish_decoded)
    starfish_decoded_table = pd.DataFrame()

    for decoded_spots in sorted_starfish_decoded:
        fov_spot_table = pd.read_csv(decoded_spots)
        starfish_decoded_table = pd.concat([starfish_decoded_table, fov_spot_table])

    starfish_decoded_table.to_csv('starfish_result.csv', index=False)

if __name__ == "__main__":
   
    # cli = {
    #     "concat_csv": concat_csv
    # }
    # fire.Fire(cli)

    csv_path = sys.argv[1:]
    concat_csv(csv_path)