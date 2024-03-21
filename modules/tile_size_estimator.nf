pythonScript = "${workflow.projectDir}/bin/tile_size_estimator.py"

process TILE_SIZE_ESTIMATOR {
    //label 'minimal'
    label 'singleImage'

    input:
    path(refImage)

    output:
    path("*.txt")
    path("*.json")
    path('*.html')

    script:
    """
    python ${pythonScript} run ${refImage}
    """
}
