import json
import os


#json_files = [path1, path2, path3] 

def merge_json(*args):
    
    images_combined = {}

    for file_path in args:
        with open(file_path, 'r') as file:
            data = json.load(file)

        images_combined.update(data['images'])

    first_file_path = json_files[0]

    with open(first_file_path, 'r') as file:
        data = json.load(file)

    data['images'] = images_combined

    with open(first_file_path, 'w') as file:
        json.dump(data, file, indent=4)

   
if __name__ == "__main__":
    
    cli = {
        "merge_json": merge_json
    }
    
    fire.Fire(cli)