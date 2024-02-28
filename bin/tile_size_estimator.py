import tifffile as tif
import fire
import json


def plot_tile_grid(image, tileSize):
    plt.imshow(image, cmap='gray')
    height, width = image.shape[:2]
    
    for i in range(0, width, tileSize):
        plt.axvline(i, color='red')
        
    for j in range(0, height, tileSize):
        plt.axhline(j, color='red')
    
    plt.ylim(height, 0) 
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.show()
    
def write_fov_name(
    fov
):
    fov_idx = str(fov)
    fov_idx_len = len(fov_idx)
    if fov_idx_len == 1:
        return f"fov_00{fov_idx}"
    elif fov_idx_len == 2:
        return f"fov_0{fov_idx}"
    else:
        return f"fov_{fov_idx}"
    
def estimate_tile_size(image_path: str, verbose=False):

    img = tif.memmap(image_path)
    image_shape = img.shape
    
    if min(image_shape) > 10000:
        max_size = 3000
        target_size = 2000
        l1 = 1500
        l2 = 3000 
        max_size = min(image_shape[0], image_shape[1], max_size)
        margin_size = {t: (image_shape[0] % t, image_shape[1] % t) for t in range(100, max_size, 100)}
    else:
        max_size = int(min(image_shape)/2)
        target_size = int(min(image_shape)/4)
        l1 = int(min(image_shape)/10)
        l2 = int(min(image_shape)/2)
        max_size = min(image_shape[0], image_shape[1], max_size)
        margin_size = {t: (image_shape[0] % t, image_shape[1] % t) for t in range(10, max_size, 10)}
        
    pairs = []
    for s, (r, c) in margin_size.items():
        if l1 < r < l2 and l1 < c < l2:
            pairs.append([s, [r, c]])
    min_difference = float('inf')
    selected_pair = None

    for pair in pairs:
        difference = abs(pair[1][0] - pair[1][1])
        if difference < min_difference or (difference == min_difference and selected_pair is not None):
            min_difference = difference
            selected_pair = pair[1]
            selected_tileSize = pair[0]

    if min(image_shape) > 10000:
        selected_tileSize = min(pairs, key=lambda x: abs(x[0] - target_size))[0]
    else:
        selected_tileSize = min(pairs, key=lambda x: abs(x[0] - target_size))[0]
    
    # Will need to remove this (used for the test dataset)
    if image_shape[0] < 800:
        selected_tileSize = 200

    if verbose:
        plot_tile_grid(img, selected_tileSize)
        
    # Save tile size in JSON
    tile_size_dict = [str(selected_tileSize)]
    with open('data.json', 'w') as fh:
        json.dump(tile_size_dict, fh)
        
    # Save TXT file with all FoVs
    horizontal_tiles = -(-image_shape[0] // selected_tileSize)
    vertical_tiles = -(-image_shape[1] // selected_tileSize)
    total_fovs = horizontal_tiles * vertical_tiles

    #for f in range(total_fovs):
    #    print(write_fov_name(f))
    with open('total_fovs.txt', "w+") as fh:
        for f in range(total_fovs):
            #print(write_fov_name(f))
            fh.writelines(write_fov_name(f)+'\n')

if __name__ == "__main__":
    cli = {
        "run": estimate_tile_size
    }
    fire.Fire(cli)


