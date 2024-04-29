import json
import fire

class ExpJsonParser:
    def __init__(self, exp_meta_json_path):
        self.meta = self._read_exp_json(exp_meta_json_path)
        
    def _read_exp_json(
        self,
        path2json
    ):
        with open(path2json, 'r') as fh:
            metadata = json.load(fh)
        return metadata

    def make_exp_json(
        self
    ):
        # Parse for type of images:
        img_meta = self.meta['aux_tilesets']['aux_names']
        img_types_dict = {img_type: img_type+'.json' for img_type in img_meta}
        img_types_dict = dict(**{"primary": "primary.json"}, **img_types_dict)
        # Create 'experiment.json' for StarFISH:
        intro_block = {"version": "5.0.0"}
        img_types_block = {"images": img_types_dict}
        codebook_block = {"extras": {}, "codebook": "codebook.json"}
        
        intro_img_block = dict(**intro_block, **img_types_block)
        whole_exp = dict(**intro_img_block, **codebook_block)
    
        #self.img_meta_write = whole_exp
        with open('experiment.json', 'w') as fh:
            json.dump(whole_exp, fh, indent=4)
            
def create_exp_json(
    exp_meta_path
):
    JsonParser = ExpJsonParser(exp_meta_path)
    JsonParser.make_exp_json()
            
if __name__ == "__main__":
    cli = {
        "make_exp_json": create_exp_json
    }
    fire.Fire(cli)
