import os
import fire

def read_file_contents(
    file_path
):
    with open(file_path, 'r') as csv_fh:
        return csv_fh.readlines()
    

def join_coordinates(*args):
    """
    Function that takes 'coordinates*.csv' for the main image types 
    and concatenates these into a single coordinates file.
    """
    with open('coordinates.csv', 'w+') as fh:
        fh.write('fov,round,ch,zplane,xc_min,yc_min,zc_min,xc_max,yc_max,zc_max\n')
        for csv_file in args:
            csv_content = read_file_contents(csv_file)
            for line_idx, line in enumerate(csv_content):
                if line_idx != 0:
                    fh.write(line)

if __name__ == "__main__":
    cli = {
        "join": join_coordinates
    }
    fire.Fire(cli)
    