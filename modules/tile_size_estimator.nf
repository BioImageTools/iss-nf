pythonScript = "${workflow.projectDir}/bin/tile_size_estimator.py"

process TILE_SIZE_ESTIMATOR {
    label 'singleImage'
    
    input:
    path(refImage)

    output:
    //path("*.txt")
    val("total_fovs.txt")
    path("*.json")

    script:
    """
    python ${pythonScript} run ${refImage}
    """
}
