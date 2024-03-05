pythonScript = "${workflow.projectDir}/bin/tiler.py"

process TILING {
    //publishDir "Tiled", mode: 'copy', overwrite: true
    //debug true
    label 'infinitesimal'

    input:
    tuple val(sampleID), path(transformedImage), val(tile_size), path(experiment_metadata_json)

    output:
    tuple val(sampleID), path("*.tiff")
    tuple val(sampleID), path("*.csv")

    script:
    """
    python ${pythonScript} run_tiling $transformedImage $tile_size $experiment_metadata_json
    """
}
