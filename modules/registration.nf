pythonScript = "${workflow.projectDir}/bin/registration.py"

process LEARN_TRANSFORM {
    publishDir "Transformations", mode: 'copy', overwrite: true
    debug true

    input:
    tuple val(roundID), path(inputMovImagePath)
    //path(param_file)
    //tuple val(roundID), path(inputMovImagePath)

    output:
    path("*.txt")
    //tuple val(roundID), path("*.txt")

    // https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow/issues/7
    //conda '/g/cba/miniconda3/envs/bia'

    script:
    """
    python ${pythonScript} run ${params.inputRefImagePath} ${inputMovImagePath} ${params.elastix_parameter_files}
    """
}

workflow {
    ch = LEARN_TRANSFORM(params.elastix_parameter_files)
}