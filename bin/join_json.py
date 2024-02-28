import json
import fire


def join_json(*args):
    
    file_paths = args
    json_data = {
        "version": "5.0.0",
        "images": {
            "primary": file_paths[3],
            "anchor_dots": file_paths[2],
            "anchor_nuclei": file_paths[0],
            "nuclei": file_paths[1]
        },
        "extras": {},
        "codebook": "codebook.json"
    }

    with open('experiment.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

   
if __name__ == "__main__":
    
    cli = {
        "merge_json": join_json
    }
    
    fire.Fire(cli)
    
    
    