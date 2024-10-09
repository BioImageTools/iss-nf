process TILING {
    //publishDir "Tiled", mode: 'copy', overwrite: true
    //debug true
    label 'tiler'
    container "nimavakili/tiling:latest"

    input:
    tuple val(sampleID), path(transformedImage), val(tile_size), path(experiment_metadata_json)

    output:
    tuple val(sampleID), path("*.tif*")
    tuple val(sampleID), path("*.csv")

    script:
    """
    python /scripts/tiler.py run_tiling $transformedImage $tile_size $experiment_metadata_json
    """
}
