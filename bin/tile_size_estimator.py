import tifffile as tif
import fire

def estimate_tile_size(image_path: str, max_size: int = 10000) -> None:

    img = tif.memmap(image_path)
    image_shape = img.shape

    max_size = min(image_shape[0], image_shape[1], max_size)

    margin_size = {t: (image_shape[0] % t, image_shape[1] % t) for t in range(100, max_size, 100)}

    pairs = []
    for s, (r, c) in margin_size.items():
        if 1500 < r < 3000 and 1500 < c < 3000:
            pairs.append([r, c])

    min_difference = float('inf')
    selected_pair = None

    for pair in pairs:
        difference = abs(pair[0] - pair[1])

        if difference < min_difference or (difference == min_difference and selected_pair is not None):
            min_difference = difference
            selected_pair = pair

    print("Selected Pair:", selected_pair)

if __name__ == "__main__":
    cli = {
        "run": estimate_tile_size
    }
    fire.Fire(cli)
