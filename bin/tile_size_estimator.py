import tifffile as tif
import fire

def estimate_tile_size(image_path: str):

    img = tif.memmap(image_path)
    image_shape = img.shape

    if min(image_shape) > 10000:
        max_size = 3000
        target_size = 2000
        l1 = 1500
        l2 = 3000
    else:
        max_size = 1000
        target_size = 500
        l1 = 150
        l2 = 500
        
    max_size = min(image_shape[0], image_shape[1], max_size)
    margin_size = {t: (image_shape[0] % t, image_shape[1] % t) for t in range(100, max_size, 100)}
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
    return selected_tileSize

if __name__ == "__main__":
    cli = {
        "run": estimate_tile_size
    }
    fir.Fire(cli)


