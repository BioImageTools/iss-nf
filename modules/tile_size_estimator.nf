// modules/tile_size_estimator.nf

pythonScript = "${workflow.projectDir}/bin/tile_size_estimator.py" --image_path /path/to/image.tif

process TILE_SIZE_ESTIMATOR {

    output:
    path 'tile_size.txt'

    script:
    """
    python ${pythonScript} ${input} > tile_size.txt
    """
}
