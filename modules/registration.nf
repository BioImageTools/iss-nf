pythonScript = "${workflow.projectDir}/bin/registration.py"

process LEARN_TRANSFORM {
    publishDir "Transformations", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(roundID), path(inputMovImagePath)
    //path(param_file)
    //tuple val(roundID), path(inputMovImagePath)

    output:
    tuple val(roundID), path("*.txt")

    // https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow/issues/7
    //conda '/g/cba/miniconda3/envs/bia'

    script:
    """
    python ${pythonScript} run_learn ${params.inputRefImagePath} ${inputMovImagePath} ${params.elastix_parameter_files}
    """
}

process APPLY_TRANSFORM {
    publishDir "Registered", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(roundID), path(transformPath), path(movingImagePath)

    output:
    tuple val(roundID), path("*.tif")

    script:
    """
    python ${pythonScript} run_apply $transformPath $movingImagePath
    """
}