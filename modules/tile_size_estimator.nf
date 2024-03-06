pythonScript = "${workflow.projectDir}/bin/tile_size_estimator.py"

process TILE_SIZE_ESTIMATOR {
    label 'minimal'
    
    input:
    path(refImage)

    output:
    //path("*.txt")
    val("total_fovs.txt")
    path("tile_size.txt")

    script:
    """
    python ${pythonScript} run ${refImage}
    """
}
