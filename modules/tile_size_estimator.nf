process TILE_SIZE_ESTIMATOR {

    label 'small'
    container "nimavakili/tiling:latest"

    input:
    path(refImage)

    output:
    path("total_fovs.txt")
    path("*.json")
    path('*.html')

    script:
    """
    python /scripts/tile_size_estimator.py run ${refImage}
    """
}
