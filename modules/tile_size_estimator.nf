pythonScript = "${workflow.projectDir}/bin/tile_size_estimator.py"

process TILE_SIZE_ESTIMATOR {

    label 'small'

    input:
    path(refImage)

    output:
    path("total_fovs.txt")
    path("*.json")
    path('*.html')

    script:
    """
    python ${pythonScript} run ${refImage}
    """
}
